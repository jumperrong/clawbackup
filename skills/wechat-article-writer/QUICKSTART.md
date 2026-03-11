# 快速入门指南

_5 分钟上手，开始使用增强版微信公众号写作系统_

---

## 🚀 第一步：安装依赖

```bash
cd /Users/jumpermac/.openclaw/workspace/skills/wechat-article-writer

# 安装必需依赖
pip install pyyaml python-dotenv

# 安装可选依赖（内容验证）
pip install tavily-python
```

---

## 🎨 第二步：测试主题系统

```bash
cd scripts

# 测试主题加载
python3 theme_loader.py

# 输出示例：
# 📚 已加载主题：
#   总数：25
#   经典主题：13
#   马卡龙主题：12
```

---

## 📝 第三步：分析文章并推荐主题

### 方式一：快速分析（只有标题）

```bash
python3 enhanced_workflow.py "臀肌挛缩不用开刀？这份非手术康复指南"
```

**输出：**
```
📊 文章分析报告
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🏷️  关键词:
   1. 康复
   2. 训练
   3. 医疗

🎨 推荐主题: warm_artistic (温暖文艺)
   - 适合康复健康类内容

🖼️  封面提示词:
   - 风格：医疗专业
   - 标签：cover_medical, title_xxxxx

✅ 无需特别验证
```

### 方式二：完整分析（标题 + 内容）

```bash
python3 enhanced_workflow.py "文章标题" article.md
```

**输出：** 包含 Tavily 验证结果（如果配置了 API Key）

---

## 🔧 第四步：配置 API Keys（可选）

### 方法一：使用环境变量（推荐）

```bash
# 添加到 ~/.zshrc 或 ~/.bashrc
export BAILIAN_API_KEY="sk-xxx"
export DOUBAO_API_KEY="ed9137d1-xxx"
export TAVILY_API_KEY="tvly-xxx"
export WECHAT_APP_ID="wxa49xxx"
export WECHAT_APP_SECRET="833xxx"

# 重新加载
source ~/.zshrc
```

### 方法二：编辑 config.json

```bash
# 复制模板
cp config.json.example config.json

# 编辑 config.json，填入你的 API Keys
```

### 检查配置状态

```bash
python3 config_loader.py

# 输出：
# 🔧 配置检查
# 📋 API Key 状态:
#   ✅ bailian: 已配置
#   ✅ doubao: 已配置
#   ✅ wechat: 已配置
#   ✅ tavily: 已配置
```

---

## 🖼️ 第五步：生成封面提示词

```bash
python3 -c "
from cover_prompt_generator import CoverPromptGenerator
generator = CoverPromptGenerator()

result = generator.generate_prompt(
    title='臀肌挛缩康复指南',
    theme='medical'
)

print('提示词:', result['prompt'])
print('标签:', result['tags'])
print('尺寸:', result['dimensions'])
"
```

---

## 📱 第六步：预览文章

### 打开增强预览页面

```bash
open preview_enhanced.html
```

**功能：**
- ✅ 选择文章
- ✅ 切换 25 个主题
- ✅ 实时预览效果
- ✅ 查看文章信息

---

## 🎯 完整工作流示例

### 场景：写一篇新的康复文章

```bash
# 1. 分析文章，获取推荐
python3 enhanced_workflow.py "髂胫束综合征自救全攻略" article.md

# 输出推荐主题：warm_artistic

# 2. 使用推荐主题导出
python3 export_wechat.py --input article.md --theme warm_artistic

# 3. 生成封面（使用自动提示词）
python3 generate_image.py --title "髂胫束综合征自救全攻略" --style medical

# 4. 预览效果
open preview_enhanced.html

# 5. 推送到微信（需要配置）
python3 publish_draft.py --article article.md
```

---

## 📊 主题选择建议

### 康复健康类文章
- **首选：** `warm_artistic`（温暖文艺）
- **备选：** `nature_fresh`（自然清新）、`macaron_mint`（马卡龙薄荷）

### 科技 AI 类文章
- **首选：** `tech_modern`（科技现代）
- **备选：** `geek_tech`（极客科技）、`data_analytics`（数据洞察）

### 商业管理类文章
- **首选：** `minimal_business`（极简商务）
- **备选：** `academic_professional`（学术专业）

### 生活旅行类文章
- **首选：** `fresh_lively`（活泼清新）
- **备选：** `cozy_lifestyle`（舒适生活）、`macaron_peach`（马卡龙蜜桃）

---

## 🧪 测试命令

```bash
# 测试所有模块
python3 theme_loader.py && \
python3 cover_prompt_generator.py && \
python3 config_loader.py && \
python3 enhanced_workflow.py "测试文章"

# 全部通过后，系统正常工作
```

---

## 📁 文件结构

```
skills/wechat-article-writer/
├── themes/                    # 25 个主题配置
│   ├── classic/              # 13 个经典主题
│   └── macaron/              # 12 个马卡龙主题
│
├── scripts/
│   ├── theme_loader.py       # 主题加载器
│   ├── cover_prompt_generator.py  # 封面提示词生成
│   ├── content_validator.py  # 内容验证
│   ├── enhanced_workflow.py  # 整合工作流
│   └── config_loader.py      # 配置管理
│
├── preview_enhanced.html     # 增强预览页面
├── ENHANCED_FEATURES.md      # 功能详细说明
├── TEST_REPORT.md            # 测试报告
└── QUICKSTART.md             # 本文件
```

---

## ❓ 常见问题

### Q: 主题推荐不准确怎么办？
A: 检查文章标题是否包含关键词。医疗内容应包含"康复"、"训练"、"疼痛"等词。

### Q: Tavily 验证失败？
A: 检查 API Key 是否正确配置。可以跳过此功能，不影响其他功能。

### Q: 预览页面打不开？
A: 确保在正确的目录执行 `open preview_enhanced.html`。

### Q: 如何自定义主题？
A: 复制 `themes/classic/warm_artistic.yaml`，修改后重命名。

---

## 🎓 进阶使用

### 批量分析多篇文章

```bash
for file in scripts/output/articles/*.md; do
    python3 enhanced_workflow.py "文章标题" "$file"
done
```

### 导出所有主题预览

```bash
for theme in warm_artistic tech_modern minimal_business; do
    python3 export_wechat.py --input article.md --theme $theme
done
```

---

## 📞 获取帮助

- **功能文档：** `ENHANCED_FEATURES.md`
- **测试报告：** `TEST_REPORT.md`
- **GitHub 仓库：** https://github.com/jumperrong/clawbackup

---

_最后更新：2026-03-11_
