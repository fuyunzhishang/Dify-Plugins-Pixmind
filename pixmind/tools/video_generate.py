"""Pixmind Video Generation Tool."""

import time
from collections.abc import Generator
from typing import Any

import requests
from dify_plugin import Tool
from dify_plugin.entities.tool import ToolInvokeMessage, ToolParameter


class VideoGenerateTool(Tool):
    """Tool for generating videos using Pixmind API."""

    def _invoke(
        self,
        tool_parameters: dict[str, Any],
    ) -> Generator[ToolInvokeMessage, None, None]:
        """Generate a video using Pixmind API."""
        api_key = self.runtime.credentials.get("api_key")
        app_key = "app_7867c26ab713fb03aec0774ed28f5802"
        base_url = (
            self.runtime.credentials.get("base_url")
            or "https://aihub-admin.aimix.pro/open-api/v1"
        )

        prompt = tool_parameters.get("prompt", "")
        model = tool_parameters.get("model", "seedance-1.5-pro")
        image_url = tool_parameters.get("image_url", "")
        duration = tool_parameters.get("duration", 5)
        aspect_ratio = tool_parameters.get("aspect_ratio", "16:9")
        resolution = tool_parameters.get("resolution", "1080p")
        timeout = tool_parameters.get("timeout", 600)
        poll_interval = tool_parameters.get("poll_interval", 5)

        headers = {
            "X-API-KEY": api_key,
            "appKey": app_key,
            "Content-Type": "application/json",
        }

        # Step 1: Submit video generation task
        generate_url = f"{base_url}/video/generate"
        payload = {
            "prompt": prompt,
            "model": model,
            "duration": duration,
            "aspectRatio": aspect_ratio,
            "resolution": resolution,
        }

        # Add image URL for image-to-video generation
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
                yield self.create_text_message(
                    f"Error: Timeout after {timeout}s. Video generation may still be in progress."
                )
                return

            poll_response = requests.get(
                url=task_url,
                headers=headers,
                timeout=30,
            )
            poll_result = poll_response.json()

            task_data = poll_result.get("data", {})
            status = task_data.get("status", "").lower()

            if status in ("ready", "completed", "success", "succeeded", "done"):
                # Try to get video URL from response
                video_url = (
                    task_data.get("videoUrl")
                    or task_data.get("video_url")
                    or ""
                )
                cover_url = (
                    task_data.get("coverUrl")
                    or task_data.get("cover_url")
                    or ""
                )

                if video_url:
                    video_url = "".join(video_url.split())
                    yield self.create_text_message(f"![video]({video_url})")
                    # Download video and output as blob for inline preview
                    try:
                        video_resp = requests.get(video_url, headers=headers, timeout=120)
                        video_resp.raise_for_status()
                        yield self.create_blob_message(
                            video_resp.content,
                            meta={
                                "mime_type": "video/mp4",
                                "filename": f"pixmind-video-{task_id}.mp4",
                            },
                        )
                    except Exception:
                        # Fallback to link if download fails
                        yield self.create_link_message(video_url)
                else:
                    yield self.create_text_message(
                        f"Video generated (taskId: {task_id}) but no URL returned. "
                        f"Please check the Pixmind dashboard."
                    )
                return

            elif status in ("failed", "error", "cancelled", "canceled"):
                error_msg = task_data.get("errorMessage") or task_data.get("error") or "Unknown error"
                yield self.create_text_message(f"Error: Video generation failed - {error_msg}")
                return

            time.sleep(poll_interval)

    def get_parameters(self) -> list[ToolParameter]:
        """Return the tool parameters."""
        return [
            ToolParameter(
                name="prompt",
                label="Prompt",
                human_description="Text description of the video to generate",
                type=ToolParameter.ToolParameterType.STRING,
                required=True,
                form=ToolParameter.ToolParameterForm.LLM,
            ),
            ToolParameter(
                name="image_url",
                label="Image URL",
                human_description="Reference image URL for image-to-video generation (required for I2V models)",
                type=ToolParameter.ToolParameterType.STRING,
                required=False,
                form=ToolParameter.ToolParameterForm.LLM,
            ),
            ToolParameter(
                name="model",
                label="Model",
                human_description="The model to use for video generation",
                type=ToolParameter.ToolParameterType.SELECT,
                required=False,
                default="seedance-1.5-pro",
                options=[
                    # Sora
                    ToolParameter.ToolParameterOption(value="sora-2", label="Sora 2"),
                    ToolParameter.ToolParameterOption(value="sora-2-pro", label="Sora 2 Pro"),
                    # Veo
                    ToolParameter.ToolParameterOption(value="veo-3.1", label="Veo 3.1"),
                    ToolParameter.ToolParameterOption(value="veo-3.1-fast", label="Veo 3.1 Fast"),
                    ToolParameter.ToolParameterOption(value="veo-3.0", label="Veo 3.0"),
                    ToolParameter.ToolParameterOption(value="veo-3.1-eco", label="Veo 3.1 Eco"),
                    # Seedance
                    ToolParameter.ToolParameterOption(value="seedance-1.5-pro", label="Seedance 1.5 Pro"),
                    ToolParameter.ToolParameterOption(value="doubao-seedance-pro", label="Seedance 1.0 Pro"),
                    ToolParameter.ToolParameterOption(value="doubao-seedance-1.0-pro-fast", label="Seedance 1.0 Pro Fast"),
                    # PixVerse
                    ToolParameter.ToolParameterOption(value="pixverse-v5", label="PixVerse V5"),
                    ToolParameter.ToolParameterOption(value="pixverse-v5-fast", label="PixVerse V5 Fast"),
                    # Wan
                    ToolParameter.ToolParameterOption(value="wan2.6-t2v", label="Wan 2.6 T2V"),
                    ToolParameter.ToolParameterOption(value="wan2.6-i2v", label="Wan 2.6 I2V"),
                ],
                form=ToolParameter.ToolParameterForm.FORM,
            ),
            ToolParameter(
                name="duration",
                label="Duration",
                human_description="Video duration in seconds",
                type=ToolParameter.ToolParameterType.NUMBER,
                required=False,
                default=5,
                min=2,
                max=10,
                form=ToolParameter.ToolParameterForm.FORM,
            ),
            ToolParameter(
                name="aspect_ratio",
                label="Aspect Ratio",
                human_description="Aspect ratio of the generated video",
                type=ToolParameter.ToolParameterType.SELECT,
                required=False,
                default="16:9",
                options=[
                    ToolParameter.ToolParameterOption(value="16:9", label="16:9"),
                    ToolParameter.ToolParameterOption(value="9:16", label="9:16"),
                    ToolParameter.ToolParameterOption(value="1:1", label="1:1"),
                    ToolParameter.ToolParameterOption(value="4:3", label="4:3"),
                    ToolParameter.ToolParameterOption(value="3:4", label="3:4"),
                ],
                form=ToolParameter.ToolParameterForm.FORM,
            ),
            ToolParameter(
                name="resolution",
                label="Resolution",
                human_description="Video resolution",
                type=ToolParameter.ToolParameterType.SELECT,
                required=False,
                default="1080p",
                options=[
                    ToolParameter.ToolParameterOption(value="480p", label="480p"),
                    ToolParameter.ToolParameterOption(value="720p", label="720p"),
                    ToolParameter.ToolParameterOption(value="1080p", label="1080p"),
                    ToolParameter.ToolParameterOption(value="2K", label="2K"),
                    ToolParameter.ToolParameterOption(value="4K", label="4K"),
                ],
                form=ToolParameter.ToolParameterForm.FORM,
            ),
            ToolParameter(
                name="timeout",
                label="Timeout",
                human_description="Maximum time in seconds to wait for video generation",
                type=ToolParameter.ToolParameterType.NUMBER,
                required=False,
                default=600,
                min=60,
                max=1200,
                form=ToolParameter.ToolParameterForm.FORM,
            ),
            ToolParameter(
                name="poll_interval",
                label="Poll Interval",
                human_description="Interval in seconds between polling requests",
                type=ToolParameter.ToolParameterType.NUMBER,
                required=False,
                default=5,
                min=2,
                max=30,
                form=ToolParameter.ToolParameterForm.FORM,
            ),
        ]
