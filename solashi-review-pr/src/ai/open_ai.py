from .abs_base_ai import BaseAiHandler
import openai
from openai import APIError, RateLimitError, Timeout
from retry import retry

from ..lib.log import get_logger

OPENAI_RETRIES = 5
OPENAI_KEY = ""


class OpenAIHandler(BaseAiHandler):
    def __init__(self, api_key:str, base_url:str):
        # Initialize OpenAIHandler specific attributes here
        try:
            super().__init__()
            openai.api_key = api_key
            openai.base_url= base_url 
        except AttributeError as e:
            raise ValueError("OpenAI key is required") from e

    @property
    def deployment_id(self):
        """
        Returns the deployment ID for the OpenAI API.
        """
        return "DEPLOYMENT_ID" ###VALUE###

    @retry(exceptions=(APIError, Timeout, AttributeError, RateLimitError),
           tries=OPENAI_RETRIES, delay=2, backoff=2, jitter=(1, 3))
    async def chat_completion(self, model: str, system: str, user: str, messages:str, temperature: float = 0.2):
        try:
            deployment_id = self.deployment_id
            get_logger().info("System: ", system)
            get_logger().info("User: ", user)
            # messages = [{"role": "system", "content": system}, {"role": "user", "content": user}]

            chat_completion = await openai.chat.completions.create(
                model=model,
                deployment_id=deployment_id,
                messages=messages,
                temperature=temperature,
            )
            resp = chat_completion["choices"][0]['message']['content']
            finish_reason = chat_completion["choices"][0]["finish_reason"]
            usage = chat_completion.get("usage")
            get_logger().info("AI response", response=resp, messages=messages, finish_reason=finish_reason,
                              model=model, usage=usage)
            return resp, finish_reason
        except (APIError, Timeout) as e:
            get_logger().error("Error during OpenAI inference: ", e)
            raise
        except (RateLimitError) as e:
            get_logger().error("Rate limit error during OpenAI inference: ", e)
            raise
        except (Exception) as e:
            get_logger().error("Unknown error during OpenAI inference: ", e)
