# 微信公众号文章生成规则

> 📅 创建时间：2026-03-10 18:23  
> 🎯 用途：规范公众号文章生成流程，确保符合微信平台限制

---

## 📋 基本规则

### 1. 作者信息

**作者名：** `4S 运动康复小专家`

**限制：**
- ✅ **8 字以下**
- ✅ 使用全称：`4S 运动康复小专家`（8 字）
- ✅ 使用简称：`4S 运动康复`（7 字）

**代码示例：**
```python
data = {
    'articles': [{
        'title': title,
        'author': '4S 运动康复小专家',  # 8 字以下
        'digest': digest,
        'content': content,
        'thumb_media_id': thumb_media_id,
        'show_cover_pic': 1
    }]
}
```

---

### 2. 标题规则

**标题长度：** 25 字以下

**要求：**
- ✅ **25 字以下**（官方实际限制）
- ✅ 推荐：8-25 字
- ✅ 可以包含标点符号

**标题示例：**
- ✅ `徒步后膝盖外侧疼痛？可能是臀肌挛缩导致的髂胫束综合征`（26 字）→ 需缩短 1 字
- ✅ `徒步后膝外侧疼痛？臀肌挛缩与髂胫束综合征`（19 字）✅
- ✅ `徒步后膝盖外侧疼痛`（9 字）✅

**代码示例：**
```python
# 提取原标题
full_title = "徒步后膝盖外侧疼痛？可能是臀肌挛缩导致的髂胫束综合征"

# 确保 25 字以内
if len(full_title) > 25:
    short_title = full_title[:25]
else:
    short_title = full_title

# 发布时使用标题
data = {
    'articles': [{
        'title': short_title,  # 25 字以内
        'author': '4S 运动康复小专家',
        # ...
    }]
}
```

---

### 3. 摘要（digest）规则

**摘要长度：** 50 字以内

**推荐：** 4-8 字简短描述

**示例：**
- ✅ `康复指南`
- ✅ `臀肌挛缩科普`
- ✅ `膝盖疼痛解决方案`

---

### 4. 配图规则（重要！）

**配图数量：** 3-5 张智能配图

**配图位置：**
- 每个## 标题后插入 1 张配图
- 前 3 个章节必须配图

**配图要求：**
- ✅ AI 生成提示词（qwen3.5-plus）
- ✅ 豆包 Seedream 4.5 生图
- ✅ 自动添加标签便于复用
- ✅ 专业医疗风格

**⚠️ 关键步骤：图片必须上传到微信素材库**

```python
# 1. 提取文章中的图片路径
image_pattern = r'!\[.*?\]\((.*?)\)'
image_paths = re.findall(image_pattern, md_content)

# 2. 上传每张图片到微信素材库
upload_url = f'https://api.weixin.qq.com/cgi-bin/material/add_material?access_token={token}&type=image'

image_map = {}
for img_path in image_paths:
    with open(img_path, 'rb') as f:
        files = {'media': f}
        response = requests.post(upload_url, files=files, timeout=30)
        result = response.json()
    
    if 'url' in result:
        # 获取 CDN URL（去掉参数）
        cdn_url = result['url'].split('?')[0]
        image_map[img_path] = cdn_url

# 3. 转换 HTML 并替换图片路径
html_content = markdown.markdown(md_content, extensions=['extra', 'codehilite'])

for local_path, cdn_url in image_map.items():
    html_content = html_content.replace(local_path, cdn_url)
```

**原因：**
- ❌ 微信后台无法访问本地路径（`/Users/jumpermac/...`）
- ✅ 必须使用微信 CDN URL（`http://mmbiz.qpic.cn/...`）

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

**上传封面图：**

```python
# 上传封面图到素材库
upload_url = f'https://api.weixin.qq.com/cgi-bin/material/add_material?access_token={token}&type=image'

with open(cover_path, 'rb') as f:
    files = {'media': f}
    response = requests.post(upload_url, files=files, timeout=30)
    result = response.json()

thumb_media_id = result['media_id']
```

**注意：** media_id 会过期，每次发布前重新上传

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

### 步骤 4：发布到草稿箱（完整流程）

**关键：必须上传图片到微信素材库并替换 URL**

```python
import requests
import json
import markdown
import re

# 1. 获取 access_token
token = get_access_token()

# 2. 读取文章并提取图片
with open(article_path, 'r', encoding='utf-8') as f:
    md_content = f.read()

image_paths = re.findall(r'!\[.*?\]\((.*?)\)', md_content)

# 3. 上传所有图片到微信素材库
upload_url = f'https://api.weixin.qq.com/cgi-bin/material/add_material?access_token={token}&type=image'
image_map = {}

for img_path in image_paths:
    with open(img_path, 'rb') as f:
        files = {'media': f}
        response = requests.post(upload_url, files=files, timeout=30)
        result = response.json()
    
    if 'url' in result:
        cdn_url = result['url'].split('?')[0]
        image_map[img_path] = cdn_url

# 4. 转换 HTML 并替换图片 URL
html_content = markdown.markdown(md_content, extensions=['extra', 'codehilite'])
for local_path, cdn_url in image_map.items():
    html_content = html_content.replace(local_path, cdn_url)

# 5. 发布到草稿箱
draft_url = f'https://api.weixin.qq.com/cgi-bin/draft/add?access_token={token}'

data = {
    'articles': [{
        'title': short_title,  # 25 字以内
        'author': '运动康复小专家',  # 8 字以内
        'digest': '臀肌挛缩与髂胫束综合征科普',  # 50 字以内
        'content': html_content,  # 包含微信 CDN 图片 URL
        'thumb_media_id': thumb_media_id,
        'show_cover_pic': 1
    }]
}

response = requests.post(
    draft_url,
    data=json.dumps(data, ensure_ascii=False).encode('utf-8'),
    headers={'Content-Type': 'application/json; charset=utf-8'},
    timeout=30
)
```

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
| **标题** | 64 字 | 25 字 | 8-25 字 |
| **作者** | 20 字 | 8 字 | 4-8 字 |
| **摘要** | 120 字 | 50 字 | 4-8 字 |
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

## 📝 完整发布示例

### 标准文章结构

```markdown
# 徒步后膝盖外侧疼痛？可能是臀肌挛缩导致的髂胫束综合征

引言段落...

## 一、什么是髂胫束综合征（ITBS）？

![配图 1](/Users/jumpermac/.../section_xxx.jpg)

内容...

## 二、臀肌挛缩才是幕后推手

![配图 2](/Users/jumpermac/.../section_xxx.jpg)

内容...

## 三、四步解决方案

![配图 3](/Users/jumpermac/.../section_xxx.jpg)

内容...
```

### 发布前处理

**必须完成的步骤：**

1. ✅ 提取文章中的所有图片路径
2. ✅ 上传每张图片到微信素材库
3. ✅ 获取微信 CDN URL
4. ✅ 替换 HTML 中的本地路径为 CDN URL
5. ✅ 使用正确的编码发布

**关键代码：**

```python
# 替换图片路径
for local_path, cdn_url in image_map.items():
    html_content = html_content.replace(local_path, cdn_url)

# 使用 ensure_ascii=False
response = requests.post(
    draft_url,
    data=json.dumps(data, ensure_ascii=False).encode('utf-8'),
    headers={'Content-Type': 'application/json; charset=utf-8'}
)
```

---

## 🎯 最佳实践

### 1. 标题优化

**好的标题：**
- ✅ `膝外侧疼痛？臀肌挛缩`（9 字）
- ✅ `徒步后膝盖外侧疼痛`（8 字）
- ✅ `臀肌挛缩康复指南`（7 字）

**避免：**
- ❌ 过长标题（超过 25 字）
- ❌ 复杂标点符号
- ❌ 模糊不清的描述

### 2. 作者名统一

**统一使用：** `运动康复小专家`（7 字）

**原因：**
- ✅ 符合 8 字限制
- ✅ 专业性强
- ✅ 亲和力好

### 3. 配图质量

**高质量配图标准：**
- ✅ AI 生成提示词（专业、准确）
- ✅ 医学插图风格
- ✅ 色调温暖、明亮
- ✅ 自动标签便于复用

### 4. 图片上传（关键！）

**⚠️ 必须完成的步骤：**

1. ✅ 提取文章中的所有图片路径
2. ✅ 上传每张图片到微信素材库
3. ✅ 获取微信 CDN URL（`http://mmbiz.qpic.cn/...`）
4. ✅ 替换 HTML 中的本地路径
5. ✅ 验证替换后的 URL 格式

**❌ 错误做法：**
```python
# 直接使用本地路径发布
html_content = markdown.markdown(md_content)
# 发布 → 微信后台无法显示图片
```

**✅ 正确做法：**
```python
# 上传并替换为 CDN URL
for img_path in image_paths:
    cdn_url = upload_to_wechat(img_path)
    html_content = html_content.replace(img_path, cdn_url)
# 发布 → 微信后台可以正常显示
```

---

## 📊 错误代码处理

### 常见错误

| 错误码 | 错误信息 | 原因 | 解决方案 |
|--------|---------|------|---------|
| **45003** | title size out of limit | 标题超限 | 缩短到 25 字以内 |
| **45004** | description size out of limit | 摘要超限 | 缩短到 50 字以内 |
| **45110** | author size out of limit | 作者名超限 | 缩短到 8 字以内 |
| **40007** | invalid media_id | media_id 失效 | 重新上传图片 |
| **图片不显示** | 无错误 | 使用本地路径 | 上传到微信素材库并替换 URL |

### 发布检查清单

**发布前必须确认：**

- [ ] 标题 25 字以内
- [ ] 作者 8 字以内
- [ ] 摘要 50 字以内
- [ ] 3-5 张配图已生成
- [ ] **所有图片已上传到微信素材库**
- [ ] **HTML 中的图片路径已替换为 CDN URL**
- [ ] 封面图已上传并获取 media_id
- [ ] 使用 `ensure_ascii=False` 编码
- [ ] 设置 `Content-Type: application/json; charset=utf-8`

---

## 🔗 相关资源

- **微信公众平台：** https://mp.weixin.qq.com
- **开发文档：** https://developers.weixin.qq.com/doc/offiaccount/
- **草稿箱 API：** https://developers.weixin.qq.com/doc/offiaccount/Draft_Box/Add_draft.html

---

_文档生成时间：2026-03-10 18:23_  
_维护者：AI 助手_
