# Pixmind Plugin for Dify

[中文](#中文) | [English](#English)

---

## 中文

### 产品介绍

Pixmind 是一款由 Aimix 开发的 AI 图像生成平台，提供高性能、低成本的图像生成服务。支持多种模型和画面比例，适用于工作流自动化、批量内容创作等场景。

- 官网：[https://www.pixmind.io](https://www.pixmind.io)
- 产品文档：[Pixmind Documentation](https://www.pixmind.io/docs)

### 功能特性

- **图片生成** — 通过文字描述生成高质量图片，支持文生图和图生图，支持自动轮询任务状态
- **视频生成** — 通过文字描述生成视频，支持多种视频模型和分辨率
- **多模型支持** — 支持以下模型：
  - **Pixmind (z-image)** — 图像生成模型，支持文生图
  - **Nano Banana Pro / Eco** — Gemini 高质量图像生成，支持 4K 分辨率、图生图
  - **Nano Banana 2 / Eco** — 高速图像生成，支持文生图、图生图
  - **Seedream 5.0 / 4.5 / 4.0** — 火山引擎图像生成，支持 2K/3K/4K 分辨率、图生图
  - **GPT Image 4o / 1.5** — OpenAI 图像生成模型，支持图生图
  - **Midjourney V7 / V6.1 / Niji 6** — Midjourney 系列模型，支持图生图、动漫风格
  - **Imagen 4 Standard** — Google 高质量图像生成
  - **Wan 2.6 Image** — 阿里云百炼通义万相，支持图像编辑
  - **Qwen Image Max / Plus** — 通义千问图像生成模型
  - **Qwen Image Edit Max / Plus** — 通义千问图像编辑模型（图生图）
- **灵活比例** — 支持 1:1、16:9、9:16、4:3、3:4、3:2、2:3 等画面比例
- **分辨率选择** — 支持 1K、2K、3K、4K 等多种分辨率
- **可配置参数** — 超时时间、轮询间隔均可自定义

### 配置说明

安装插件后，需要在插件设置中配置以下凭证：

| 参数 | 说明 |
|------|------|
| API Key | Pixmind API 密钥（X-API-KEY 请求头） |
| Base URL | API 基础地址（默认：`https://aihub-admin.aimix.pro/open-api/v1`） |

从 [Pixmind 官网](https://www.pixmind.io/) 获取 API Key。

### 使用方式

1. 在 Dify 插件市场安装 Pixmind 插件
2. 配置 API Key
3. 在工作流中添加 **图片生成** 工具，输入提示词即可生成图片
4. 选择支持图生图的模型时，可传入参考图片 URL 实现图生图
5. 在工作流中添加 **视频生成** 工具，输入提示词即可生成视频

### 支持

联系邮箱：support@pixmind.io

---

## English

### About

Pixmind is an AI image generation platform developed by Aimix, offering high-performance and cost-effective image generation services. It supports multiple models and aspect ratios, suitable for workflow automation, batch content creation, and more.

- Website: [https://www.pixmind.io](https://www.pixmind.io)
- Documentation: [Pixmind Documentation](https://www.pixmind.io/docs)

### Features

- **Image Generation** — Generate high-quality images from text prompts, support text-to-image and image-to-image with automatic task polling
- **Video Generation** — Generate videos from text prompts, support multiple video models and resolutions
- **Multiple Models** — Support for the following models:
  - **Pixmind (z-image)** — Image generation model, text-to-image
  - **Nano Banana Pro / Eco** — Gemini high-quality image generation, 4K resolution, image-to-image
  - **Nano Banana 2 / Eco** — High-speed image generation, text-to-image and image-to-image
  - **Seedream 5.0 / 4.5 / 4.0** — Volcengine image generation, 2K/3K/4K resolution, image-to-image
  - **GPT Image 4o / 1.5** — OpenAI image generation, image-to-image support
  - **Midjourney V7 / V6.1 / Niji 6** — Midjourney series, image-to-image, anime style
  - **Imagen 4 Standard** — Google high-quality image generation
  - **Wan 2.6 Image** — Alibaba Cloud image generation with editing support
  - **Qwen Image Max / Plus** — Qwen image generation models
  - **Qwen Image Edit Max / Plus** — Qwen image editing models (image-to-image)
- **Flexible Aspect Ratios** — 1:1, 16:9, 9:16, 4:3, 3:4, 3:2, 2:3
- **Resolution Options** — 1K, 2K, 3K, 4K
- **Configurable** — Customizable timeout and polling interval

### Configuration

After installing the plugin, configure the following credentials in the plugin settings:

| Parameter | Description |
|-----------|-------------|
| API Key | Pixmind API key (X-API-KEY header) |
| Base URL | API base URL (default: `https://aihub-admin.aimix.pro/open-api/v1`) |

Get your API Key from [Pixmind](https://www.pixmind.io/).

### Usage

1. Install the Pixmind plugin from the Dify marketplace
2. Configure your API Key
3. Add the **Image Generate** tool to your workflow and enter a prompt to generate images
4. When using a model that supports image-to-image, provide a reference image URL
5. Add the **Video Generate** tool to your workflow and enter a prompt to generate videos

### Support

Contact: support@pixmind.io
