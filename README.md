# Dify Plugins

[中文](#中文) | [English](#English)

---

## 中文

### 简介

Dify 插件开发仓库。

### 插件列表

| 插件 | 版本 | 说明 |
|------|------|------|
| [pixmind](./pixmind/) | 0.0.19 | AI 图片/视频生成平台插件 |

### 开发

#### 构建

```bash
# 构建指定插件（自动从 manifest.yaml 读取版本号）
./scripts/build.sh pixmind

# 指定版本号
./scripts/build.sh pixmind 0.0.19
```

#### 安装

在 Dify 控制台 → 插件管理 → 上传 `.difypkg` 文件。

#### 目录结构

```
pixmind/
├── _assets/icon.svg        # 插件图标
├── provider/               # 凭证配置 + Provider 逻辑
│   ├── pixmind.yaml        # 凭证定义
│   └── pixmind.py          # Provider 实现
├── tools/                  # 工具定义
│   ├── image_generate.*    # 图片生成
│   └── video_generate.*    # 视频生成
├── manifest.yaml           # 插件元信息
├── main.py                 # 入口
├── requirements.txt        # Python 依赖
└── README.md
```

---

## English

### About

Dify plugin development repository.

### Plugins

| Plugin | Version | Description |
|--------|---------|-------------|
| [pixmind](./pixmind/) | 0.0.19 | AI image/video generation platform plugin |

### Development

#### Build

```bash
# Build a specific plugin (reads version from manifest.yaml automatically)
./scripts/build.sh pixmind

# Specify a version
./scripts/build.sh pixmind 0.0.19
```

#### Installation

Upload the `.difypkg` file in Dify Console → Plugin Management.

#### Directory Structure

```
pixmind/
├── _assets/icon.svg        # Plugin icon
├── provider/               # Credential config + Provider logic
│   ├── pixmind.yaml        # Credential definitions
│   └── pixmind.py          # Provider implementation
├── tools/                  # Tool definitions
│   ├── image_generate.*    # Image generation
│   └── video_generate.*    # Video generation
├── manifest.yaml           # Plugin metadata
├── main.py                 # Entry point
├── requirements.txt        # Python dependencies
└── README.md
```
