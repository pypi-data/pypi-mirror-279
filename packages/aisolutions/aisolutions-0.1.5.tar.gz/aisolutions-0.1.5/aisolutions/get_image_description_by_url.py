from dataclasses import dataclass
from dinjectorr import inject
from aisolutions.open_ai_client import OpenAIClient


class GetImageDescriptionByUrl:
    @dataclass(frozen=True)
    class Request:
        prompt: str
        url: str
        model: str = "gpt-4o"
        max_tokens: int = 300

    @dataclass(frozen=True)
    class Response:
        description: str

    @inject
    def __init__(
        self,
        open_ai_client: OpenAIClient,
    ) -> None:
        self._open_ai_client = open_ai_client

    def __call__(self, request: Request) -> Response:
        prompt = request.prompt
        url = request.url
        model = request.model
        max_tokens = request.max_tokens

        response = self._open_ai_client.chat.completions.create(
            model=model,
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": prompt},
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": url,
                            },
                        },
                    ],
                }
            ],
            max_tokens=max_tokens,
        )

        description = response.choices[0].message.content

        return self.Response(description=description)
