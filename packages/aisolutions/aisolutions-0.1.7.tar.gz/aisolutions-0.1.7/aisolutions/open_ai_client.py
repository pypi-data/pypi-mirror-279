from dinjectorr import inject, Injector
from openai import OpenAI
from aisolutions.config import OPENAI_API_KEY


class OpenAIClient(OpenAI):
    @inject
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)


Injector.register(OpenAIClient, api_key=OPENAI_API_KEY)
