"""Pixmind Image Generation Tool."""

import base64
import mimetypes
import time
from collections.abc import Generator
from typing import Any

import requests
from dify_plugin import Tool
from dify_plugin.entities.tool import ToolInvokeMessage, ToolParameter


class ImageGenerateTool(Tool):
    """Tool for generating images using Pixmind API."""

    def _invoke(
        self,
        tool_parameters: dict[str, Any],
    ) -> Generator[ToolInvokeMessage, None, None]:
        """Generate an image using Pixmind API.

        Args:
            tool_parameters: Dictionary containing:
                - prompt: Text description of the image
                - model: Model to use (default: nano-banana-2-eco)
                - aspect_ratio: Image aspect ratio (default: 1:1)
                - timeout: Maximum wait time in seconds (default: 60)
                - poll_interval: Polling interval in seconds (default: 2)

        Yields:
            ToolInvokeMessage containing a persisted image file and a text payload that
            downstream workflow nodes can consume directly.
        """
        # Get credentials
        api_key = self.runtime.credentials.get("api_key")
        app_key = "app_7867c26ab713fb03aec0774ed28f5802"
        base_url = (
            self.runtime.credentials.get("base_url")
            or "https://aihub-admin.aimix.pro/open-api/v1"
        )

        # Debug: Log credential status (not values for security)
        print(f"[Pixmind] API Key present: {bool(api_key)}, length: {len(api_key) if api_key else 0}")
        print(f"[Pixmind] App Key present: {bool(app_key)}, length: {len(app_key) if app_key else 0}")
        print(f"[Pixmind] Base URL: {base_url}")

        # Get parameters
        prompt = tool_parameters.get("prompt", "")
        model = tool_parameters.get("model", "nano-banana-2-eco")
        aspect_ratio = tool_parameters.get("aspect_ratio", "1:1")
        resolution = tool_parameters.get("resolution", "1K")
        image_url = tool_parameters.get("image_url", "")
        timeout = tool_parameters.get("timeout", 180)
        poll_interval = tool_parameters.get("poll_interval", 2)

        # Prepare headers
        headers = {
            "X-API-KEY": api_key,
            "appKey": app_key,
            "Content-Type": "application/json",
        }

        # Step 1: Submit image generation task
        generate_url = f"{base_url}/image/generate"
        payload = {
            "prompt": prompt,
            "model": model,
            "aspectRatio": aspect_ratio,
        }

        # Add resolution if specified
        if resolution:
            payload["resolution"] = resolution

        # Add image URL for image-to-image generation
        if image_url:
            payload["imageUrl"] = image_url

        response = requests.post(
            url=generate_url,
            headers=headers,
            json=payload,
            timeout=30,
        )
        result = response.json()

        if result.get("code") != 1000:
            error_msg = result.get("message", "Unknown error")
            yield self.create_text_message(f"Error: {error_msg}")
            return

        task_id = result.get("data", {}).get("taskId")
        if not task_id:
            yield self.create_text_message("Error: No task ID returned")
            return

        # Step 2: Poll for task status
        task_url = f"{base_url}/task/{task_id}"
        start_time = time.time()

        while True:
            elapsed = time.time() - start_time
            if elapsed >= timeout:
                yield self.create_text_message(f"Error: Timeout after {timeout} seconds")
                return

            poll_response = requests.get(
                url=task_url,
                headers=headers,
                timeout=30,
            )
            poll_result = poll_response.json()

            task_data = poll_result.get("data", {})
            status = task_data.get("status", "").lower()

            if status in ("completed", "success", "succeeded", "done", "ready"):
                images = task_data.get("images", [])
                if images:
                    # Clean up URL - remove newlines and extra whitespace
                    result_url = "".join(images[0].split())

                    blob_message = self._create_image_blob_message(
                        image_url=result_url,
                        headers=headers,
                        task_id=task_id,
                    )

                    if blob_message:
                        yield blob_message
                    else:
                        yield self.create_image_message(result_url)

                    yield self.create_text_message(f"![image]({result_url})")
                    yield self.create_variable_message("image_url", result_url)
                else:
                    yield self.create_text_message("Error: Task completed but no images found")
                return

            elif status in ("failed", "error", "cancelled", "canceled"):
                error_msg = task_data.get("error", "Unknown error")
                yield self.create_text_message(f"Error: Task failed - {error_msg}")
                return

            time.sleep(poll_interval)

    def get_parameters(self) -> list[ToolParameter]:
        """Return the tool parameters."""
        return [
            ToolParameter(
                name="prompt",
                label="Prompt",
                human_description="Text description of the image to generate",
                type=ToolParameter.ToolParameterType.STRING,
                required=True,
                form=ToolParameter.ToolParameterForm.LLM,
            ),
            ToolParameter(
                name="model",
                label="Model",
                human_description="The model to use for image generation",
                type=ToolParameter.ToolParameterType.SELECT,
                required=False,
                default="nano-banana-2-eco",
                options=[
                    ToolParameter.ToolParameterOption(value="z-image", label="Pixmind"),
                    ToolParameter.ToolParameterOption(value="nano-banana-pro", label="Nano Banana Pro (文生图/图生图)"),
                    ToolParameter.ToolParameterOption(value="nano-banana-pro-lite", label="Nano Banana Pro Eco (文生图/图生图)"),
                    ToolParameter.ToolParameterOption(value="nano-banana-2", label="Nano Banana 2 (文生图/图生图)"),
                    ToolParameter.ToolParameterOption(value="nano-banana-2-eco", label="Nano Banana 2 Eco (文生图/图生图)"),
                    ToolParameter.ToolParameterOption(value="nano-banana", label="Nano Banana (文生图/图生图)"),
                    ToolParameter.ToolParameterOption(value="seedream-5.0", label="Seedream 5.0 (文生图/图生图)"),
                    ToolParameter.ToolParameterOption(value="seedream-4.5", label="Seedream 4.5 (文生图/图生图)"),
                    ToolParameter.ToolParameterOption(value="seedream-4.0", label="Seedream 4.0 (文生图/图生图)"),
                    ToolParameter.ToolParameterOption(value="gpt-image-4o", label="GPT Image 4o (文生图/图生图)"),
                    ToolParameter.ToolParameterOption(value="gpt-image-1.5", label="GPT Image 1.5 (文生图/图生图)"),
                    ToolParameter.ToolParameterOption(value="mj-v7", label="Midjourney V7 (文生图/图生图)"),
                    ToolParameter.ToolParameterOption(value="mj-v6.1", label="Midjourney V6.1 (文生图/图生图)"),
                    ToolParameter.ToolParameterOption(value="mj-niji6", label="Midjourney Niji 6 (文生图/图生图)"),
                    ToolParameter.ToolParameterOption(value="imagen-4-standard", label="Imagen 4 Standard (文生图)"),
                    ToolParameter.ToolParameterOption(value="wan2.6-image", label="Wan 2.6 Image (文生图/图生图)"),
                    ToolParameter.ToolParameterOption(value="qwen-image-max", label="Qwen Image Max (文生图)"),
                    ToolParameter.ToolParameterOption(value="qwen-image-plus", label="Qwen Image Plus (文生图)"),
                    ToolParameter.ToolParameterOption(value="qwen-image-edit-max", label="Qwen Image Edit Max (图生图)"),
                    ToolParameter.ToolParameterOption(value="qwen-image-edit-plus", label="Qwen Image Edit Plus (图生图)"),
                ],
                form=ToolParameter.ToolParameterForm.FORM,
            ),
            ToolParameter(
                name="image_url",
                label="Image URL",
                human_description="Reference image URL for image-to-image generation (required for i2i models)",
                type=ToolParameter.ToolParameterType.STRING,
                required=False,
                form=ToolParameter.ToolParameterForm.LLM,
            ),
            ToolParameter(
                name="aspect_ratio",
                label="Aspect Ratio",
                human_description="Aspect ratio of the generated image",
                type=ToolParameter.ToolParameterType.SELECT,
                required=False,
                default="1:1",
                options=[
                    ToolParameter.ToolParameterOption(value="1:1", label="1:1"),
                    ToolParameter.ToolParameterOption(value="16:9", label="16:9"),
                    ToolParameter.ToolParameterOption(value="9:16", label="9:16"),
                    ToolParameter.ToolParameterOption(value="4:3", label="4:3"),
                    ToolParameter.ToolParameterOption(value="3:4", label="3:4"),
                    ToolParameter.ToolParameterOption(value="3:2", label="3:2"),
                    ToolParameter.ToolParameterOption(value="2:3", label="2:3"),
                ],
                form=ToolParameter.ToolParameterForm.FORM,
            ),
            ToolParameter(
                name="resolution",
                label="Resolution",
                human_description="Image resolution",
                type=ToolParameter.ToolParameterType.SELECT,
                required=False,
                default="1K",
                options=[
                    ToolParameter.ToolParameterOption(value="1K", label="1K"),
                    ToolParameter.ToolParameterOption(value="2K", label="2K"),
                    ToolParameter.ToolParameterOption(value="3K", label="3K"),
                    ToolParameter.ToolParameterOption(value="4K", label="4K"),
                ],
                form=ToolParameter.ToolParameterForm.FORM,
            ),
            ToolParameter(
                name="timeout",
                label="Timeout",
                human_description="Maximum time in seconds to wait for image generation",
                type=ToolParameter.ToolParameterType.NUMBER,
                required=False,
                default=180,
                min=30,
                max=600,
                form=ToolParameter.ToolParameterForm.FORM,
            ),
            ToolParameter(
                name="poll_interval",
                label="Poll Interval",
                human_description="Interval in seconds between polling requests",
                type=ToolParameter.ToolParameterType.NUMBER,
                required=False,
                default=2,
                min=1,
                max=10,
                form=ToolParameter.ToolParameterForm.FORM,
            ),
        ]

    def _create_image_blob_message(
        self,
        *,
        image_url: str,
        headers: dict[str, str],
        task_id: str | int,
    ) -> ToolInvokeMessage | None:
        """Download the Pixmind image and return a blob message.

        Some Pixmind responses contain private or short-lived URLs that the Dify
        backend cannot fetch directly. Converting the payload to a blob ensures the
        workflow UI receives a persisted tool file.
        """

        try:
            if image_url.startswith("data:"):
                image_bytes, mime_type = self._decode_data_uri(image_url)
            else:
                response = requests.get(image_url, headers=headers, timeout=60)
                response.raise_for_status()
                image_bytes = response.content
                mime_type = (
                    response.headers.get("Content-Type", "").split(";")[0].strip()
                    or mimetypes.guess_type(image_url)[0]
                    or "image/png"
                )
        except Exception as exc:  # noqa: BLE001 - surface fallback to caller
            print(f"[Pixmind] Failed to download image {image_url}: {exc}")
            return None

        filename = self._build_filename(task_id, mime_type)
        meta: dict[str, str] = {"mime_type": mime_type}
        if filename:
            meta["filename"] = filename

        return self.create_blob_message(image_bytes, meta=meta)

    @staticmethod
    def _decode_data_uri(data_uri: str) -> tuple[bytes, str]:
        """Decode a data URI and return the bytes + mime type."""

        header, _, payload = data_uri.partition(",")
        mime_type = "image/png"
        if header.startswith("data:"):
            mime_type = header[5:].split(";")[0] or mime_type
        return base64.b64decode(payload), mime_type

    @staticmethod
    def _build_filename(task_id: str | int, mime_type: str) -> str:
        """Generate a best-effort filename for the stored blob."""

        extension = mimetypes.guess_extension(mime_type) or ".png"
        safe_task_id = str(task_id).replace("/", "-")[:32]
        return f"pixmind-{safe_task_id}{extension}"
