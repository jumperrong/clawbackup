---
name: wechat-article-writer
description: 微信公众号全自动内容助手 - AI 写文、配图、排版、发布草稿箱
homepage: https://github.com/openclaw/openclaw
metadata: {"clawdbot":{"emoji":"📝","requires":{"bins":["python3","node"],"env":["DEEPSEEK_API_KEY","DOUBAO_API_KEY","WECHAT_APPID","WECHAT_APPSECRET"]},"primaryEnv":"DEEPSEEK_API_KEY"}}
---

# 微信公众号智能内容助手

全自动公众号发文工作流：**AI 写文 → AI 配图 → 智能排版 → 发布草稿箱**

## 🎯 核心工作流（6 步全自动）

1. **AI 生成文章** - 调用 DeepSeek API 生成公众号文章
2. **AI 生成封面图** - 调用豆包 AI 生图接口生成封面
3. **智能配图** - 根据文章小标题自动插入配图
4. **图片压缩** - 压缩图片符合微信要求（封面<64KB）
5. **格式转换** - Markdown 转微信兼容 HTML
6. **发布草稿箱** - 推送至公众号草稿箱

## 📚 使用示例

```bash
# 基础用法 - 生成文章
node scripts/write_article.py --topic "春季减肥变美" --style "干货"

# 生成封面图
node scripts/generate_image.py --topic "春季减肥" --title "春季减肥变美指南"

# 完整工作流（推荐）
node scripts/run_full_workflow.js --topic "春季减肥变美" --style "干货" --layout "暖色"
```

### OpenClaw 对话示例

```
用户：利用 wechat-article-writer，参考 [对标文章多维表格] 里面对标文章的风格，写一篇春季减肥变美的文章，文章中要有配图，暖色排版风格

助手：✅ 已读取对标文章风格
✅ 文章生成完成（1500 字）
✅ 封面图已生成
✅ 已插入 3 张配图
✅ 图片已压缩优化
✅ 已转换为微信 HTML 格式
✅ 已发布至草稿箱

文章标题：《春季减肥变美全攻略：3 个习惯让你瘦一圈》
请前往公众号草稿箱审阅发布。
```

## 📁 项目结构

```
wechat-article-writer/
├── SKILL.md              # 本文件
├── scripts/
│   ├── write_article.py      # AI 写文章
│   ├── generate_image.py     # AI 生图
│   ├── add_article_images.py # 智能配图
│   ├── compress_image.py     # 图片压缩
│   ├── format_article.py     # 格式转换
│   ├── publish_draft.py      # 发布草稿
│   └── run_full_workflow.js  # 完整工作流（封装）
├── config.json           # API 配置
├── output/               # 输出目录
└── output/
    ├── articles/         # 生成的文章
    ├── images/           # 生成的图片
    └── html/             # 转换后的 HTML
```

## 🔑 配置说明

### config.json

```json
{
  "bailian_api_key": "sk-xxxx",
  "bailian_base_url": "https://coding.dashscope.aliyuncs.com/v1",
  "writing_model": "qwen3-max-2026-01-23",
  "image_model": "qwen3.5-plus",
  "fast_model": "glm-4.7",
  "agent_model": "glm-5",
  "doubao_api_key": "xxxx-xxxx-xxxx",
  "wechat_appid": "wx1234567890abcdef",
  "wechat_appsecret": "1234567890abcdef1234567890abcdef"
}
```

### 配置项说明

| 配置项 | 说明 | 获取方式 |
|--------|------|----------|
| `bailian_api_key` | 通义千问 API 密钥 | 阿里云百炼平台 |
| `writing_model` | 写作模型 | 默认 `qwen3-max-2026-01-23`（复杂任务最强） |
| `image_model` | 配图模型 | 默认 `qwen3.5-plus`（性能均衡） |
| `fast_model` | 快速任务模型 | 默认 `glm-4.7` |
| `agent_model` | Agent 编排模型 | 默认 `glm-5` |
| `doubao_api_key` | 豆包 API 密钥 | 豆包开放平台 |
| `wechat_appid` | 微信公众号 AppID | 微信公众平台 → 开发 → 基本配置 |
| `wechat_appsecret` | 微信公众号 AppSecret | 同上 |

### 模型调用原则

| 模型 | 适用场景 |
|------|----------|
| `qwen3.5-plus` | 通用任务，性能均衡 |
| `qwen3-max-2026-01-23` | 复杂任务，最强性能 ✨ |
| `qwen3-coder-next` | 代码生成专用 |
| `qwen3-coder-plus` | 代码理解增强 |
| `glm-5` | 复杂 Agent 任务 |
| `glm-4.7` | 快速响应任务 |
| `kimi-k2.5` | 长文本和推理 |

## 🎨 文章风格

支持 4 种写作风格：

| 风格 | 特点 | 适用场景 |
|------|------|----------|
| `干货` | 专业、信息密度高、实用 | 教程、指南、测评 |
| `情感` | 温暖、共情力、故事感 | 情感文、鸡汤文 |
| `资讯` | 简洁、客观、信息密集 | 新闻、行业动态 |
| `活泼` | 轻松、幽默、接地气 | 生活分享、种草 |

## 📝 输出示例

### 生成的 Markdown 文章

```markdown
# 春季减肥变美全攻略：3 个习惯让你瘦一圈

## 一、饮食调整：吃对才能瘦

春季是减肥的黄金期...

## 二、运动计划：动得巧瘦得快

...

## 三、作息优化：睡得好才能瘦

...
```

### 生成的 HTML（微信兼容）

```html
<section style="font-size: 16px; line-height: 1.6;">
  <h1 style="text-align: center; color: #ff6b6b;">春季减肥变美全攻略</h1>
  <section style="margin: 20px 0;">
    <img src="https://mmbiz.qpic.cn/xxx" style="width: 100%;"/>
  </section>
  ...
</section>
```

## ⚠️ 注意事项

1. **图片大小限制** - 封面图不能超过 64KB，脚本会自动压缩
2. **素材库上传** - 配图需要上传到微信永久素材库
3. **Access Token 缓存** - 脚本会自动缓存 token，避免频繁请求
4. **对标文章管理** - 建议使用飞书多维表格管理对标账号文章

## 🔗 相关资源

- [DeepSeek 开放平台](https://platform.deepseek.com/)
- [豆包 AI 开放平台](https://www.doubao.com/)
- [微信公众号开发文档](https://developers.weixin.qq.com/doc/offiaccount/Basic_Information/Overview.html)
