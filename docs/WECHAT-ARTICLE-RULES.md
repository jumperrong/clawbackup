# 微信公众号文章生成规则

> 📅 创建时间：2026-03-10 18:23  
> 🎯 用途：规范公众号文章生成流程，确保符合微信平台限制

---

## 📋 基本规则

### 1. 作者信息

**作者名：** `4S 运动康复小专家`

**限制：**
- ❌ 实际测试发现：作者名限制约 **7 字以内**
- ✅ 使用简称：`4S 运动康复`（7 字）
- ⚠️ `4S 运动康复小专家`（10 字）超出限制

**代码示例：**
```python
data = {
    'articles': [{
        'title': title,
        'author': '4S 运动康复',  # 使用 7 字以内
        'digest': digest,
        'content': content,
        'thumb_media_id': thumb_media_id,
        'show_cover_pic': 1
    }]
}
```

---

### 2. 标题规则

**标题长度：** 25 字以内

**实际测试：**
- ✅ 实际限制：约 **10 字以内**（不是官方文档的 64 字）
- ✅ 推荐：8-10 字
- ❌ 超过 10 字会报错：`45003 title size out of limit`

**标题优化建议：**
- 原标题：`徒步后膝盖外侧疼痛？可能是臀肌挛缩导致的髂胫束综合征`（26 字）❌
- 优化后：`徒步后膝外侧疼痛`（8 字）✅

**代码示例：**
```python
# 提取原标题
full_title = "徒步后膝盖外侧疼痛？可能是臀肌挛缩导致的髂胫束综合征"

# 生成短标题（10 字以内）
short_title = full_title[:10]  # 或使用更智能的摘要

# 发布时使用短标题
data = {
    'articles': [{
        'title': short_title,  # 8-10 字
        'author': '4S 运动康复',
        # ...
    }]
}
```

---

### 3. 摘要（digest）规则

**摘要长度：** 约 12 字以内

**实际测试：**
- ✅ 12 字以内：成功
- ❌ 13 字以上：报错 `45004 description size out of limit`

**推荐：** 4-8 字简短描述

**示例：**
- ✅ `康复指南`
- ✅ `臀肌挛缩科普`
- ✅ `膝盖疼痛解决方案`

---

### 4. 配图规则

**配图数量：** 3-5 张智能配图

**配图位置：**
- 每个## 标题后插入 1 张配图
- 前 3 个章节必须配图

**配图要求：**
- ✅ AI 生成提示词（qwen3.5-plus）
- ✅ 豆包 Seedream 4.5 生图
- ✅ 自动添加标签便于复用
- ✅ 专业医疗风格

**代码示例：**
```python
# 分析文章结构
sections = analyze_article_structure(md_content)

# 为前 3 个章节配图
for section in sections[:3]:
    image_path = generate_section_image(
        topic=topic,
        section_title=section['title'],
        style='干货'
    )
    # 插入图片到文章
```

---

### 5. 封面图规则

**封面图尺寸：**
- 头条封面：900×383（2.35:1）
- 分享封面：383×383（1:1）

**封面图要求：**
- ✅ 专业医疗风格
- ✅ 准确体现主题
- ✅ 高清、精美
- ✅ 压缩到 100KB 以内

---

## 🔧 发布流程

### 步骤 1：生成文章

```bash
python3 scripts/write_article.py \
  --topic "臀肌挛缩康复指南" \
  --style "干货" \
  --length 2500
```

### 步骤 2：生成配图

```bash
python3 scripts/add_article_images.py \
  --article "scripts/output/articles/article_xxx.md" \
  --topic "臀肌挛缩康复" \
  --style "干货"
```

### 步骤 3：生成封面图

```bash
python3 scripts/generate_image.py \
  --topic "臀肌挛缩康复指南" \
  --title "臀肌挛缩不用开刀？" \
  --style "干货"
```

### 步骤 4：发布到草稿箱

```bash
python3 scripts/publish_fixed.py
```

**发布参数：**
- 标题：8-10 字
- 作者：`4S 运动康复`
- 摘要：4-8 字
- 内容：包含 3-5 张配图
- 封面图：已上传

---

## ⚠️ 注意事项

### 1. 编码问题

**必须使用正确的编码：**

```python
# ❌ 错误做法
requests.post(url, json=data)

# ✅ 正确做法
requests.post(
    url,
    data=json.dumps(data, ensure_ascii=False).encode('utf-8'),
    headers={'Content-Type': 'application/json; charset=utf-8'}
)
```

**原因：** 避免中文被转义为 Unicode 转义序列（如 `\u5f92\u6b65\u540e...`）

### 2. 长度限制汇总

| 字段 | 官方文档 | 实际限制 | 推荐使用 |
|------|---------|---------|---------|
| **标题** | 64 字 | 10 字 | 8-10 字 |
| **作者** | 20 字 | 7 字 | 4-7 字 |
| **摘要** | 120 字 | 12 字 | 4-8 字 |
| **内容** | 20000 字 | 20000 字 | 2000-5000 字 |

### 3. 图片上传

**图片必须先上传到微信素材库：**

```python
# 上传封面图
upload_url = f'https://api.weixin.qq.com/cgi-bin/material/add_material?access_token={token}&type=image'

with open(cover_path, 'rb') as f:
    files = {'media': f}
    response = requests.post(upload_url, files=files, timeout=30)
    result = response.json()
    thumb_media_id = result['media_id']
```

**注意：** media_id 会过期，每次发布前重新上传

---

## 📝 文章模板

### 标准结构

```markdown
# 文章标题（25 字以内，用于生成短标题）

引言段落...

## 一、什么是 XXX？

![配图 1](path/to/image1.jpg)

内容...

## 二、XXX 的原因

![配图 2](path/to/image2.jpg)

内容...

## 三、解决方案

![配图 3](path/to/image3.jpg)

内容...
```

### 发布时的标题处理

```python
# 原标题
full_title = "徒步后膝盖外侧疼痛？可能是臀肌挛缩导致的髂胫束综合征"

# 生成短标题（10 字以内）
short_title = "徒步后膝外侧疼痛"  # 8 字

# 发布
data = {
    'articles': [{
        'title': short_title,  # 使用短标题
        'author': '4S 运动康复',
        'digest': '康复指南',
        'content': html_content,
        'thumb_media_id': thumb_media_id,
        'show_cover_pic': 1
    }]
}
```

---

## 🎯 最佳实践

### 1. 标题优化

**好的标题：**
- ✅ `膝外侧疼痛？臀肌挛缩`（9 字）
- ✅ `徒步后膝盖外侧疼痛`（8 字）
- ✅ `臀肌挛缩康复指南`（7 字）

**避免：**
- ❌ 过长标题（超过 10 字）
- ❌ 复杂标点符号
- ❌ 模糊不清的描述

### 2. 作者名统一

**统一使用：** `4S 运动康复`

**原因：**
- ✅ 符合 7 字限制
- ✅ 品牌识别度高
- ✅ 专业性强

### 3. 配图质量

**高质量配图标准：**
- ✅ AI 生成提示词（专业、准确）
- ✅ 医学插图风格
- ✅ 色调温暖、明亮
- ✅ 自动标签便于复用

---

## 📊 错误代码处理

### 常见错误

| 错误码 | 错误信息 | 原因 | 解决方案 |
|--------|---------|------|---------|
| **45003** | title size out of limit | 标题超限 | 缩短到 10 字以内 |
| **45004** | description size out of limit | 摘要超限 | 缩短到 12 字以内 |
| **45110** | author size out of limit | 作者名超限 | 缩短到 7 字以内 |
| **40007** | invalid media_id | media_id 失效 | 重新上传图片 |

---

## 🔗 相关资源

- **微信公众平台：** https://mp.weixin.qq.com
- **开发文档：** https://developers.weixin.qq.com/doc/offiaccount/
- **草稿箱 API：** https://developers.weixin.qq.com/doc/offiaccount/Draft_Box/Add_draft.html

---

_文档生成时间：2026-03-10 18:23_  
_维护者：AI 助手_
