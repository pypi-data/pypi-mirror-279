import os
from dinjectorr import inject, Injector
from openai import OpenAI


class OpenAIClient(OpenAI):
    @inject
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)


Injector.register(OpenAIClient, api_key=os.getenv("OPENAI_API_KEY"))
