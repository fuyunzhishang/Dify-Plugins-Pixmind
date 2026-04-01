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
            # Validate credentials by making a test request to the API
            import requests

            api_key = cred.get("api_key")
            base_url = cred.get("base_url") or "https://aihub-admin.aimix.pro/open-api/v1"

            headers = {
                "X-API-KEY": api_key,
                "appKey": APP_KEY,
                "Content-Type": "application/json",
            }
            response = requests.post(
                url=f"{base_url}/image/generate",
                headers=headers,
                json={"prompt": "test", "model": "nano-banana-2-eco", "aspectRatio": "1:1"},
                timeout=10,
            )
            result = response.json()
            if result.get("code") == 401:
                raise ToolProviderCredentialValidationError("Invalid API key")
        except ToolProviderCredentialValidationError:
            raise
        except Exception as e:
            raise ToolProviderCredentialValidationError(str(e))
