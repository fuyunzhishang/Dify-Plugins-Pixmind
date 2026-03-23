from dify_plugin import ToolProvider
from dify_plugin.errors.tool import ToolProviderCredentialValidationError

from tools.image_generate import ImageGenerateTool

APP_KEY = "app_7867c26ab713fb03aec0774ed28f5802"


class PixmindProvider(ToolProvider):
    """Provider for Pixmind image generation tools."""

    def _validate_credentials(self, cred: dict) -> None:
        """Validate the provided credentials by making a test request.

        Args:
            cred: Dictionary containing api_key.

        Raises:
            ToolProviderCredentialValidationError: If credentials are invalid.
        """
        try:
            # Inject app_key into credentials for validation
            cred_with_app = {**cred, "app_key": APP_KEY}
            # Try to invoke the image generate tool with a simple test
            for _ in ImageGenerateTool.from_credentials(credentials=cred_with_app).invoke(
                tool_parameters={
                    "prompt": "test",
                    "model": "nano-banana-2-eco",
                    "aspect_ratio": "1:1",
                    "timeout": 10,
                    "poll_interval": 2,
                },
            ):
                pass
        except Exception as e:
            raise ToolProviderCredentialValidationError(str(e))
