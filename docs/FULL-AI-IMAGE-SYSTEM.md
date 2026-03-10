# 完全 AI 化配图系统 - 使用指南

> 📅 创建时间：2026-03-10 13:45  
> 🎯 特点：所有提示词用 AI 生成 + 图片标签化便于复用

---

## 📊 系统架构

### 工作流程

```
1. 文章生成完成
   ↓
2. AI 分析文章内容和标题
   ↓
3. AI 生成提示词（qwen3.5-plus）
   ↓
4. AI 生成图片（豆包 Seedream 4.5）
   ↓
5. 保存图片和元数据（含标签）
   ↓
6. 可搜索和复用
```

### 核心改进

**之前：**
- ❌ 模板生成提示词
- ❌ 无标签，难复用
- ❌ 元数据不完整

**现在：**
- ✅ AI 生成提示词（更专业）
- ✅ 自动添加标签（便于搜索）
- ✅ 完整元数据（JSON 格式）
- ✅ 支持搜索和复用

---

## 🔧 工具说明

### 1. 封面图生成

**脚本：** `scripts/generate_image.py`

**功能：**
- ✅ AI 生成提示词（默认）
- ✅ 自动添加标签
- ✅ 保存完整元数据
- ✅ 支持自定义标签

**使用方法：**

```bash
# 基本用法（AI 生成提示词 + 自动标签）
python3 scripts/generate_image.py \
  --topic "臀肌挛缩康复指南" \
  --title "臀肌挛缩不用开刀？" \
  --style "干货"

# 带文章内容（更准确的提示词）
python3 scripts/generate_image.py \
  --topic "臀肌挛缩康复指南" \
  --title "臀肌挛缩不用开刀？" \
  --style "干货" \
  --content "article_content.md"

# 自定义标签
python3 scripts/generate_image.py \
  --topic "臀肌挛缩康复指南" \
  --title "臀肌挛缩不用开刀？" \
  --style "干货" \
  --tags "医疗" "康复" "科普" "健身"

# 不使用 AI 生成提示词（备用）
python3 scripts/generate_image.py \
  --topic "臀肌挛缩康复指南" \
  --style "干货" \
  --no-ai
```

**输出：**
- 图片文件：`cover_医疗_康复_20260310_134500.jpg`
- 元数据：`cover_医疗_康复_20260310_134500.jpg.meta.json`

---

### 2. 章节配图

**脚本：** `scripts/add_article_images.py`

**功能：**
- ✅ AI 分析文章结构
- ✅ 为前 3 个## 标题配图
- ✅ AI 生成提示词
- ✅ 自动添加标签
- ✅ 保存标签到文件

**使用方法：**

```bash
# 基本用法
python3 scripts/add_article_images.py \
  --article "scripts/output/articles/article_xxx.md" \
  --topic "臀肌挛缩康复指南" \
  --style "干货"
```

**输出：**
- 更新后的文章（含图片 Markdown）
- 图片文件：`section_臀肌_康复_20260310_134500.jpg`
- 标签文件：`image_tags.json`

---

### 3. 图片搜索和复用

**脚本：** `scripts/search_images.py`

**功能：**
- ✅ 按关键词搜索
- ✅ 按主题搜索
- ✅ 按风格搜索
- ✅ 按标签搜索
- ✅ 列出所有标签
- ✅ 导出标签到文件

**使用方法：**

```bash
# 按关键词搜索
python3 scripts/search_images.py \
  --search "康复训练"

# 按主题搜索
python3 scripts/search_images.py \
  --topic "臀肌挛缩"

# 按风格搜索
python3 scripts/search_images.py \
  --style "干货"

# 按标签搜索
python3 scripts/search_images.py \
  --tags "医疗" "康复"

# 组合搜索
python3 scripts/search_images.py \
  --topic "臀肌挛缩" \
  --style "干货" \
  --tags "康复" \
  --limit 5

# 列出所有标签
python3 scripts/search_images.py --list-tags

# 导出标签到文件
python3 scripts/search_images.py \
  --export "all_image_tags.json"
```

**输出示例：**
```
✅ 找到 5 张匹配的图片：

1. section_臀肌_康复_20260310_134500.jpg
   主题：臀肌挛缩康复指南 | 风格：干货
   标签：臀肌挛缩，康复训练，干货，健康科普，医学插图
   评分：15

2. cover_医疗_康复_20260310_134500.jpg
   主题：臀肌挛缩康复指南 | 风格：干货
   标签：医疗，康复，干货，健康科普
   评分：13
```

---

## 📝 元数据格式

### 封面图元数据

```json
{
  "filepath": "/path/to/cover_xxx.jpg",
  "url": "https://...",
  "prompt": "AI 生成的提示词",
  "size": "900x383",
  "cover_type": "header",
  "file_size_kb": 85.5,
  "created_at": "2026-03-10T13:45:00",
  "topic": "臀肌挛缩康复指南",
  "title": "臀肌挛缩不用开刀？",
  "style": "干货",
  "tags": ["医疗", "康复", "干货", "健康科普"],
  "use_ai_prompt": true
}
```

### 章节配图元数据

```json
{
  "filepath": "/path/to/section_xxx.jpg",
  "url": "https://...",
  "prompt": "AI 生成的提示词",
  "size": "16:9",
  "created_at": "2026-03-10T13:45:00",
  "topic": "臀肌挛缩康复指南",
  "section_title": "什么是臀肌挛缩？",
  "style": "干货",
  "tags": ["臀肌挛缩", "康复训练", "干货", "健康科普", "医学插图"],
  "use_ai_prompt": true
}
```

---

## 🎯 标签系统

### 自动生成标签

**封面图标签：**
- 主题关键词（前 10 字）
- 标题关键词（前 10 字）
- 文章风格
- "健康科普"
- "医学插图"

**章节配图标签：**
- 主题关键词
- 章节标题关键词
- 文章风格
- "健康科普"
- "医学插图"

### 标签复用策略

**场景 1：同类文章复用**

```bash
# 搜索所有"康复"相关的图片
python3 scripts/search_images.py --tags "康复"

# 找到后可以直接使用 filepath
```

**场景 2：同风格复用**

```bash
# 搜索所有"干货"风格的图片
python3 scripts/search_images.py --style "干货"
```

**场景 3：主题复用**

```bash
# 搜索所有"臀肌挛缩"相关的图片
python3 scripts/search_images.py --topic "臀肌挛缩"
```

---

## 📊 性能数据

| 指标 | 数值 | 说明 |
|------|------|------|
| **提示词生成** | qwen3.5-plus | 1-2 秒 |
| **图片生成** | doubao-seedream-4.5 | 5-10 秒 |
| **提示词成本** | ¥0.002/次 | 约 200 tokens |
| **图片成本** | ¥0.1-0.2/张 | 高清图片 |
| **单张总成本** | ¥0.102-0.202 | 含提示词 |
| **搜索速度** | <100ms | 本地搜索 |

---

## 💡 最佳实践

### 标签命名规范

**推荐：**
- ✅ 简洁明了（2-8 字）
- ✅ 使用下划线分隔
- ✅ 避免特殊字符
- ✅ 统一中文或英文

**示例：**
```
✅ 医疗，康复训练，健康科普
❌ 医疗/康复，health-care
```

### 复用策略

**高复用价值标签：**
- 通用主题：`健康科普`, `医学插图`, `康复训练`
- 常见风格：`干货`, `情感`, `资讯`
- 热门领域：`健身`, `营养`, `心理`

**低复用价值标签：**
- 过于具体：`20260310_134500`
- 时间相关：`春季`, `2026 年`
- 个人化：`我的文章`

### 批量处理

**批量生成 + 标签：**

```python
# 伪代码示例
articles = [
    {"topic": "臀肌挛缩", "style": "干货"},
    {"topic": "髂胫束", "style": "干货"},
    {"topic": "膝盖疼痛", "style": "干货"}
]

for article in articles:
    # 生成封面图（带通用标签）
    generate_cover_image(
        topic=article["topic"],
        style=article["style"],
        tags=["健康科普", "医学插图", article["style"]]
    )
```

---

## 🔧 配置参数

### config.json

```json
{
  "bailian_api_key": "sk-sp-10f48e26ce354c59b083cbe9d711d5af",
  "doubao_api_key": "ed9137d1-b82e-4ca9-b6ee-a1bd32fa9cd2",
  "writing_model": "qwen3-max-2026-01-23",
  "image_model": "qwen3.5-plus",
  "optimize_model": "qwen3.5-plus"
}
```

### 环境变量（可选）

```bash
export BAILIAN_API_KEY="sk-sp-xxx"
export DASHSCOPE_API_KEY="sk-sp-xxx"
```

---

## 📋 完整流程示例

### 示例：臀肌挛缩康复指南

**步骤 1：生成文章**

```bash
python3 scripts/write_article.py \
  --topic "臀肌挛缩康复指南" \
  --style "干货" \
  --length 2500
```

**步骤 2：生成封面图**

```bash
python3 scripts/generate_image.py \
  --topic "臀肌挛缩康复指南" \
  --title "臀肌挛缩不用开刀？" \
  --style "干货" \
  --tags "医疗" "康复" "科普"
```

**步骤 3：生成章节配图**

```bash
python3 scripts/add_article_images.py \
  --article "scripts/output/articles/article_xxx.md" \
  --topic "臀肌挛缩康复指南" \
  --style "干货"
```

**步骤 4：搜索和复用**

```bash
# 搜索所有康复相关图片
python3 scripts/search_images.py \
  --tags "康复" "医疗" \
  --limit 10
```

---

## 🎯 总结

### 核心价值

**完全 AI 化：**
- ✅ 提示词 AI 生成（更专业）
- ✅ 图片 AI 生成（更精美）
- ✅ 标签 AI 提取（更准确）

**便于复用：**
- ✅ 完整元数据
- ✅ 标签化搜索
- ✅ 快速定位

**系统化管理：**
- ✅ 统一格式
- ✅ 易于维护
- ✅ 可扩展

---

_文档生成时间：2026-03-10 13:45_  
_作者：AI 助手_
