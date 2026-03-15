# 📚 微信公众号技能 - 命令使用指南

本指南用**自然语言**描述所有可用功能，无需记忆复杂命令。

---

## 🚀 快速开始

### 启动预览服务器

**我想预览文章**
```bash
bash scripts/start_preview_server.sh
```

**预览服务器已经启动了，怎么看？**
- 浏览器打开：http://localhost:8080/preview.html
- 查看状态：服务器在后台运行，不依赖 Terminal

**我想关闭预览服务器**
```bash
bash scripts/stop_preview_server.sh
```

---

## 📝 文章生成

### 创建新文章

**帮我写一篇文章**
```bash
python3 scripts/write_article.py --topic "你的主题" --style "干货"
```

**完整参数说明：**
- `--topic`：文章主题（必填）
- `--style`：写作风格（干货/情感/资讯/活泼，默认：干货）
- `--keywords`：关键词（可选）
- `--length`：文章字数（默认：1500）
- `--title-hint`：标题提示（可选）

**示例：**
```bash
# 写一篇关于运动康复的干货文章
python3 scripts/write_article.py --topic "运动康复" --style "干货" --length 2000

# 写一篇温暖的情感文
python3 scripts/write_article.py --topic "坚持的力量" --style "情感"
```

---

## 🖼️ 智能配图

### 为文章添加配图

**帮这篇文章配上合适的图片**
```bash
python3 scripts/smart_image_inserter.py --article-id "文章 ID"
```

**说明：**
- 自动分析文章段落内容
- 智能匹配最相关的图片
- 插入到合适的章节位置

---

## 📋 文章管理

### 查看所有文章

**现在有哪些文章？**
```bash
python3 scripts/manage_article_status.py status
```

**输出示例：**
```
============================================================
📚 文章状态列表
============================================================

🔒 [READY     ] 为什么 90% 的运动损伤本可避免？ (2026-03-14)
📝 [DRAFT    ] 新的文章草稿 (2026-03-15)
✅ [PUBLISHED] 已发布的文章 (2026-03-13)
```

**状态图标说明：**
- 📝 **草稿** - 正在创作中，还未审核
- 👀 **审核中** - 已提交审核，等待确认
- 🔒 **已锁定** - 审核通过，内容已固定
- ✅ **已发布** - 已发布到微信公众号

---

### 锁定文章（审核通过）

**这篇文章我审核通过了，可以锁定**
```bash
python3 scripts/manage_article_status.py lock --article-id "文章 ID"
```

**做了什么：**
- ✅ 将文章从草稿移动到正式目录
- ✅ 更新索引文件
- ✅ 预览页面显示为"已完成"

**示例：**
```bash
python3 scripts/manage_article_status.py lock --article-id 2026-03-14_200126
```

---

### 发布文章

**把这篇文章发布到公众号**
```bash
python3 scripts/manage_article_status.py publish --article-id "文章 ID"
```

**说明：**
- 标记文章为已发布状态
- 记录发布时间
- 可关联微信公众号文章 ID

---

## 🔄 索引管理

### 更新文章索引

**更新一下文章列表**
```bash
python3 scripts/update_index.py
```

**什么时候需要运行：**
- ✅ 生成新文章后
- ✅ 锁定文章后
- ✅ 删除文章后

**可选参数：**
```bash
# 完全重建索引（不保留已有记录）
python3 scripts/update_index.py --full
```

---

### 更新草稿列表

**更新草稿列表**
```bash
python3 scripts/update_previews.py
```

**什么时候需要运行：**
- ✅ 创建新草稿后
- ✅ 修改草稿内容后
- ✅ 删除草稿后

---

## 🎨 主题切换

### 导出不同主题版本

**把这篇文章导出成不同风格的主题**
```bash
python3 scripts/theme_loader.py --article-id "文章 ID" --theme medical
```

**可用主题：**
- `medical` - 医疗专业风格（绿色系）
- `tech` - 科技风格（蓝色系）
- `classic` - 经典风格（红色系）
- `minimal` - 极简风格（黑白灰）

---

## 📊 状态检查

### 查看系统状态

**现在系统运行正常吗？**
```bash
# 检查预览服务器
bash scripts/stop_preview_server.sh  # 如果显示"未运行"说明没启动

# 查看文章索引
cat scripts/output/index.json | python3 -m json.tool

# 查看草稿列表
cat scripts/output/previews/list.json | python3 -m json.tool
```

---

## 🔧 实用场景

### 场景 1：完成一篇文章的完整流程

**我想从头到尾完成一篇文章**

```bash
# 1. 生成文章
python3 scripts/write_article.py --topic "你的主题" --style "干货"

# 2. 智能配图（如果有图片生成功能）
python3 scripts/smart_image_inserter.py --article-id "文章 ID"

# 3. 启动预览服务器查看效果
bash scripts/start_preview_server.sh
# 浏览器打开：http://localhost:8080/preview.html

# 4. 审核通过后锁定
python3 scripts/manage_article_status.py lock --article-id "文章 ID"

# 5. 更新索引
python3 scripts/update_index.py

# 6. 发布到公众号（如需要）
python3 scripts/manage_article_status.py publish --article-id "文章 ID"
```

---

### 场景 2：批量管理文章

**我想看看所有草稿**
```bash
python3 scripts/manage_article_status.py status | grep DRAFT
```

**我想看看所有已完成的文章**
```bash
python3 scripts/manage_article_status.py status | grep READY
```

**我想看看所有已发布的文章**
```bash
python3 scripts/manage_article_status.py status | grep PUBLISHED
```

---

### 场景 3：日常维护

**每天早上检查系统**
```bash
# 1. 检查预览服务器
bash scripts/stop_preview_server.sh

# 2. 查看文章状态
python3 scripts/manage_article_status.py status

# 3. 更新索引（如有需要）
python3 scripts/update_index.py
```

---

## 📖 文件结构说明

```
skills/wechat-article-writer/
├── scripts/                      # 脚本目录
│   ├── write_article.py         # 生成文章
│   ├── smart_image_inserter.py  # 智能配图
│   ├── update_index.py          # 更新索引
│   ├── update_previews.py       # 更新草稿
│   ├── manage_article_status.py # 文章状态管理
│   ├── start_preview_server.sh  # 启动预览
│   └── stop_preview_server.sh   # 停止预览
├── scripts/output/              # 输出目录
│   ├── articles/                # 已完成文章
│   ├── previews/                # 草稿文章
│   ├── images/                  # 图片资源
│   ├── index.json               # 文章索引
│   └── preview.html             # 预览页面
└── config.json                  # 配置文件
```

---

## 💡 常见问题

### Q: 预览页面打不开？
**A:** 先启动预览服务器：
```bash
bash scripts/start_preview_server.sh
```

### Q: 新文章没有出现在预览页面？
**A:** 更新索引：
```bash
python3 scripts/update_index.py
```
然后刷新浏览器（Cmd+Shift+R）

### Q: 如何删除一篇文章？
**A:** 手动删除文件：
```bash
# 删除 Markdown 文件
rm scripts/output/articles/article_xxx.md

# 删除图片目录
rm -rf scripts/output/images/xxx

# 更新索引
python3 scripts/update_index.py
```

### Q: 如何修改已锁定的文章？
**A:** 已锁定的文章不建议修改。如必须修改：
1. 复制文章到草稿目录
2. 修改草稿
3. 重新提交审核
4. 锁定新版本

---

## 🎯 最佳实践

1. **每次生成文章后** → 运行 `update_index.py`
2. **每天开始工作前** → 检查预览服务器状态
3. **审核通过文章** → 立即锁定并更新索引
4. **定期清理** → 删除不需要的草稿和中间版本

---

**需要更多帮助？** 查看各脚本的 `--help` 参数：
```bash
python3 scripts/write_article.py --help
python3 scripts/manage_article_status.py --help
```
