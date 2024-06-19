import datetime
import json
import uuid
import time
import logging
import traceback
from typing import Any, List, Mapping, Optional
import os
from amazon_sagemaker_jupyter_ai_q_developer.request_logger import flush_metrics, get_new_metrics_context
from botocore import UNSIGNED

from botocore.exceptions import ClientError
from langchain_core.callbacks.manager import CallbackManagerForLLMRun
from langchain_core.language_models.llms import LLM
from langchain.prompts import (
    PromptTemplate
)
import boto3
from pathlib import Path
from botocore import UNSIGNED
from botocore.client import Config
from typing import Coroutine
from jupyter_ai_magics.providers import AwsAuthStrategy, BaseProvider
from jupyter_ai_magics import Persona

from amazon_sagemaker_jupyter_ai_q_developer.file_cache_manager import FileCacheManager
from amazon_sagemaker_jupyter_ai_q_developer.exceptions import ServerExtensionException
from amazon_sagemaker_jupyter_ai_q_developer.environment import Environment
from amazon_sagemaker_jupyter_ai_q_developer.constants import CW_PROD_ENDPT

logging.basicConfig(format="%(levelname)s: %(message)s")

SESSION_FOLDER = f"{Path(__file__).parent}/service_models"

class AmazonQLLM(LLM):
    UNSUBSCRIBED_MESSAGE = (
        "You are not subscribed to AmazonQ. Please request your Studio domain admin to subscribe you. "
        "<a href='https://docs.aws.amazon.com/amazonq/latest/qdeveloper-ug/q-admin-setup-subscribe-general.html'>"
        "Please refer link.</a>"
    )
    Q_NOT_ENABLED_MESSAGE = "Your admin has not enabled Q-Developer. Please reach out to your admin."

    model_id: str
    """Required in the constructor. Allowed values: ('Q-Developer')"""

    _client: Optional[Any] = None
    """boto3 client object."""

    _conversation_id: Optional[str] = None
    """The conversation ID included with the first response from Amazon Q."""

    _client_id: Optional[str] = uuid.uuid4()
    """The client ID included with the first response from Amazon Q."""

    file_cache_manager = FileCacheManager()

    def _add_header(self, request, **kwargs):
        request.headers.add_header("Authorization", f"Bearer {self.__get_bearer_token()}")
        request.headers.add_header("Content-Type", "application/json")
        request.headers.add_header("Content-Encoding", "amz-1.0")

    @property
    def _llm_type(self) -> str:
        return "custom"

    def _call(
        self,
        prompt: str,
        stop: Optional[List[str]] = None,
        run_manager: Optional[CallbackManagerForLLMRun] = None,
        **kwargs: Any,
    ) -> str:
        #TODO: extract to wrapper based metrics collection mechanism, debug issue with wrapper function
        metrics = get_new_metrics_context("AmazonQLLM_call")
        start_time = datetime.datetime.now()
        try:
            if self.model_id != "Q-Developer":
                raise ValueError("Only 'Q-Developer' is supported by this model provider.")

            if not self._client:
                self._init_client()

            data = {
                "currentMessage": {
                    "userInputMessage": { "content":f"{prompt}"}
                },
                "chatTriggerType":"MANUAL",
            }
            if self._conversation_id and len(self._conversation_id):
                data["conversationId"] = self._conversation_id

            try:
                q_dev_profile_arn = self.__get_q_dev_profile_arn()
            except FileNotFoundError:
                metrics.set_property("QDevProfileArnFile", traceback.format_exc())
                # If q_dev_profile.json is not found then we can assume that domain is not Q enabled
                return self.Q_NOT_ENABLED_MESSAGE

            generate_start_time = datetime.datetime.now()
            try:
                response = self._client.generate_assistant_response(conversationState=data, profileArn=q_dev_profile_arn)
            except ClientError as e:
                metrics.set_property("GenerateAssistantException", traceback.format_exc())
                if e.response['Error']['Code'] == 'AccessDeniedException':
                    return self.UNSUBSCRIBED_MESSAGE
                else:
                    raise
            finally:
                generate_elapsed_time = datetime.datetime.now() - generate_start_time
                metrics.put_metric("GenerateAssistantLatency", int(generate_elapsed_time.total_seconds() * 1000), "Milliseconds")

            conversation_id = response.get("conversationId", None)

            parent_product = Environment.get_environment()
            ide_category = 'JUPYTER_SM'
            if parent_product is Environment.MD:
                ide_category = "JUPYTER_MD"

            t_event = {
                "chatAddMessageEvent": {
                    "conversationId": conversation_id,
                    "messageId": response.get("ResponseMetadata", None).get("RequestId", "")
                },
            }
            user_context = {
                "ideCategory": ide_category,
                "operatingSystem": "LINUX",
                "product": "QChat"
            }
            telemetry_start_time = datetime.datetime.now()
            try:
                self._telemetry_client.send_telemetry_event(telemetryEvent=t_event, userContext=user_context, profileArn=q_dev_profile_arn)
            except Exception as e:
                # Get the request ID from the exception metadata
                metrics.set_property("SendTelemetryException", traceback.format_exc())
                logging.error(traceback.format_exc())
            finally:
                telemtery_elapsed_time = datetime.datetime.now() - telemetry_start_time
                metrics.put_metric("TelemetryLatency", int(telemtery_elapsed_time.total_seconds() * 1000), "Milliseconds")

            if self._conversation_id is None and conversation_id:
                print(f"[Amazon Q]: Assigned conversation ID '{conversation_id}'.")
                self._conversation_id = conversation_id

            event_stream = response["generateAssistantResponseResponse"]

            reply = ""
            for event in event_stream:
                if "assistantResponseEvent" in event:
                    reply += event["assistantResponseEvent"]["content"]

            return reply
        except Exception as e:
            # log the exception for debugging
            metrics.set_property("StackTrace", traceback.format_exc())
            raise e
        finally:
            elapsed = datetime.datetime.now() - start_time
            metrics.put_metric("Latency", int(elapsed.total_seconds() * 1000), "Milliseconds")
            flush_metrics(metrics)

    def _init_client(self):
        client = self.__get_client('bearer', CW_PROD_ENDPT, '2023-11-27')
        client.meta.events.register("before-sign.*.*", self._add_header)
        self._client = client

        telemetry_client = self.__get_client('bearer', CW_PROD_ENDPT, '2022-11-11')
        telemetry_client.meta.events.register("before-sign.*.*", self._add_header)
        self._telemetry_client = telemetry_client

    def __get_client(self, service_name, endpoint_url, api_version):
        session = boto3.Session()
        session._loader.search_paths.extend([SESSION_FOLDER])
        return session.client(
            service_name=service_name,
            endpoint_url=endpoint_url,
            region_name=endpoint_url.split('.')[1],
            config=Config(connect_timeout=60, signature_version=UNSIGNED),
            api_version=api_version
        )

    def __get_bearer_token(self):
        return self.__extractor("~/.aws/sso/idc_access_token.json",
                                lambda d: d["idc_access_token"])

    def __get_q_dev_profile_arn(self):
        return self.__extractor("~/.aws/amazon_q/q_dev_profile.json",
                                lambda d: d["q_dev_profile_arn"])

    def __extractor(self, file_path=None, value_extractor=None):
        content = json.loads(self.file_cache_manager.get_cached_file_content(os.path.expanduser(file_path)))
        val = value_extractor(content)
        if val is None or not val.strip():
            raise ServerExtensionException(f"No value found in {file_path}.")
        return value_extractor(content)

    @property
    def _identifying_params(self) -> Mapping[str, Any]:
        """Get the identifying parameters."""
        return {}


AMAZON_Q_AVATAR_ROUTE = "api/ai/static/q.svg"
AmazonQPersona = Persona(name="Amazon Q", avatar_route=AMAZON_Q_AVATAR_ROUTE)


class AmazonQProvider(BaseProvider, AmazonQLLM):
    id = "amazon-q"
    name = "Amazon Q"
    models = [
        "Q-Developer",
    ]
    model_id_key = "model_id"
    pypi_package_deps = ["boto3"]
    auth_strategy = AwsAuthStrategy()

    persona = AmazonQPersona
    unsupported_slash_commands = {"/learn", "/ask", "/generate"}
    manages_history = True

    @property
    def allows_concurrency(self):
        return False

    def get_chat_prompt_template(self) -> PromptTemplate:
        """
        Produce a prompt template optimised for chat conversation.
        This overrides the default prompt template, as Amazon Q expects just the
        raw user prompt without any additional templating.
        """
        return PromptTemplate.from_template(
            template="{input}"
        )

    async def _acall(self, *args, **kwargs) -> Coroutine[Any, Any, str]:
        return await self._call_in_executor(*args, **kwargs)