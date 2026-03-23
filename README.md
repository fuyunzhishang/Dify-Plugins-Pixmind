# Dify Plugins

Dify 插件开发仓库。

## 插件列表

| 插件 | 版本 | 说明 |
|------|------|------|
| [pixmind](./pixmind/) | 0.0.19 | AI 图片/视频生成平台插件 |

## 开发

### 构建

```bash
# 构建指定插件（自动从 manifest.yaml 读取版本号）
./scripts/build.sh pixmind

# 指定版本号
./scripts/build.sh pixmind 0.0.19
```

### 安装

在 Dify 控制台 → 插件管理 → 上传 `.difypkg` 文件。

### 目录结构

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
