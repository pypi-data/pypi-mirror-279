from dataclasses import dataclass
from dinjectorr import inject
from aisolutions.open_ai_client import OpenAIClient


class GetImageDescription:
    @dataclass(frozen=True)
    class Request:
        image_url_or_base64: str
        prompt: str = "What is on the image?"
        model: str = "gpt-4o"
        max_tokens: int = 300
        is_base64: bool = False
        image_format: str | None = None

    @dataclass(frozen=True)
    class Response:
        description: str

    class Error(Exception):
        """Base error class for GetImageDescription."""

    class ImageFormatWasNotProvided(Error):
        """Image format was not provided."""

    @inject
    def __init__(
        self,
        open_ai_client: OpenAIClient,
    ) -> None:
        self._open_ai_client = open_ai_client

    def __call__(self, request: Request) -> Response:
        prompt = request.prompt
        image_url_or_base64 = request.image_url_or_base64
        model = request.model
        max_tokens = request.max_tokens
        is_base64 = request.is_base64
        image_format = request.image_format

        if is_base64:
            if not image_format:
                raise self.ImageFormatWasNotProvided(
                    "Image format must be provided when image is in base64 format."
                )
            url = f"data:image/{image_format};base64,{image_url_or_base64}"
        else:
            url = image_url_or_base64

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
