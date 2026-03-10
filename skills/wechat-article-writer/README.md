# 📝 微信公众号智能内容助手

## ⚡ 快速开始

### 1. 配置 API 密钥

编辑 `config.json`，填入你的 API 密钥：

```json
{
  "deepseek_api_key": "sk-your-key-here",
  "doubao_api_key": "your-key-here",
  "wechat_appid": "wx-your-appid",
  "wechat_appsecret": "your-appsecret"
}
```

### 2. 安装依赖

```bash
pip install openai pillow requests
```

### 3. 使用方式

#### 方式一：完整工作流（推荐）

```bash
cd /Users/jumpermac/.openclaw/workspace/skills/wechat-article-writer

node scripts/run_full_workflow.js \
  --topic "春季减肥变美" \
  --style "干货" \
  --layout "暖色"
```

#### 方式二：分步执行

```bash
# 1. 生成文章
python3 scripts/write_article.py --topic "春季减肥" --style "干货"

# 2. 生成封面图
python3 scripts/generate_image.py --topic "春季减肥" --style "干货"

# 3. 智能配图
python3 scripts/add_article_images.py --article output/articles/article_xxx.md --topic "春季减肥"

# 4. 压缩图片
python3 scripts/compress_image.py --input output/images/

# 5. 格式转换
python3 scripts/format_article.py --input output/articles/article_xxx.md

# 6. 发布草稿
python3 scripts/publish_draft.py --html output/articles/article_xxx.html --cover output/images/cover_xxx.jpg
```

#### 方式三：OpenClaw 对话

```
利用 wechat-article-writer，参考 [对标文章多维表格] 里面对标文章的风格，
写一篇春季减肥变美的文章，文章中要有配图，暖色排版风格
```

## 📁 目录结构

```
wechat-article-writer/
├── SKILL.md              # 技能说明
├── README.md             # 本文件
├── config.json           # 配置文件
├── scripts/              # 脚本目录
│   ├── write_article.py      # AI 写文章
│   ├── generate_image.py     # AI 生图
│   ├── add_article_images.py # 智能配图
│   ├── compress_image.py     # 图片压缩
│   ├── format_article.py     # 格式转换
│   ├── publish_draft.py      # 发布草稿
│   └── run_full_workflow.js  # 完整工作流
└── output/               # 输出目录
    ├── articles/         # 生成的文章
    ├── images/           # 生成的图片
    └── html/             # 转换后的 HTML
```

## 🎨 支持的风格

- `干货` - 专业、实用、信息密度高
- `情感` - 温暖、共情、故事感
- `资讯` - 简洁、客观、新闻体
- `活泼` - 轻松、幽默、接地气

## ⚠️ 注意事项

1. **图片大小** - 封面图自动压缩至 64KB 以下
2. **Access Token** - 自动缓存，避免频繁请求
3. **对标文章** - 建议使用飞书多维表格管理

## 🔗 相关资源

- [DeepSeek 开放平台](https://platform.deepseek.com/)
- [豆包 AI 开放平台](https://www.doubao.com/)
- [微信公众号开发文档](https://developers.weixin.qq.com/doc/)
