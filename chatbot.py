from google import genai
from logging import getLogger
import os
from dotenv import load_dotenv

load_dotenv()

logger = getLogger(__name__)

DEFAULT_API_KEY = os.environ.get("API_KEY")
DEFAULT_MODEL = "gemini-3.5-flash"
DEFAULT_TEMPERATURE = 0.7
DEFAULT_MAX_OUTPUT_TOKENS = 512
DEFAULT_TOKEN_BUDGET = 4096


class Chatbot:
    def __init__(
        self,
        model=None,
        api_key=None,
        temperature: float = 0.7,
        max_output_tokens=None,
        token_budget=None,
    ):
        self.model = model if model else DEFAULT_MODEL
        self.api_key = api_key if api_key else DEFAULT_API_KEY
        self.temperature = temperature if temperature else DEFAULT_TEMPERATURE
        self.max_output_tokens = (
            max_output_tokens if max_output_tokens else DEFAULT_MAX_OUTPUT_TOKENS
        )
        self.token_budget = token_budget if token_budget else DEFAULT_TOKEN_BUDGET

        self.client = genai.Client()

    def send_message(self, prompt: str) -> str:
        response = self.chat.send_message(
            prompt,
            config={
                "temperature": self.temperature,
                "max_output_tokens": self.max_output_tokens,
                "token_budget": self.token_budget,
            },
        )
        reply = response.text

        # Track usage
        usage = response.usage_metadata
        self.token_log.append(
            {
                "prompt": usage.prompt_token_count,
                "output": usage.candidates_token_count,
                "total": usage.total_token_count,
            }
        )
        self.request_count += 1
        return reply

    def get_token_summary(self):
        return sum(log["total"] for log in self.token_log)

    def get_tokens_left(self):
        # Remaining budget = token_budget - last turn total
        if not self.token_log:
            return self.token_budget
        last_turn = self.token_log[-1]["total"]
        return max(self.token_budget - last_turn, 0)

    @temperature.setter
    def temperature(self, value: float):
        if value < 0 or value > 2:
            err_msg = "Temperature should be between 0 and 2"
            logger.error(err_msg)
            raise ValueError(err_msg)
        self.temperature = value

    @max_output_tokens.setter
    def max_output_tokens(self, value: int):
        if value < 0:
            err_msg = "Max output tokens should be greater than 0"
            logger.error(err_msg)
            raise ValueError(err_msg)
        self.max_output_tokens = value

    @token_budget.setter
    def token_budget(self, value: int):
        if value < 0:
            err_msg = "Max output tokens should be greater than 0"
            logger.error(err_msg)
            raise ValueError(err_msg)
        self.token_budget = value

    def switch_model(self, new_model: str):
        # Start a new chat session with preserved history
        self.model = new_model
        self.chat = self.client.chat.start(model=new_model, history=self.history)