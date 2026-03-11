# 微信公众号写作技能 - 用户使用指南

_零基础也能上手，像聊天一样写公众号文章_

---

## 📖 目录

1. [新手入门](#新手入门)
2. [第一次使用](#第一次使用)
3. [常用场景](#常用场景)
4. [高级技巧](#高级技巧)
5. [常见问题](#常见问题)
6. [故障排除](#故障排除)

---

## 新手入门

### 这是什么？

这是一个**微信公众号写作助手**，帮你：
- 🎨 自动推荐文章主题（排版风格）
- 🖼️ 自动生成封面图片提示词
- ✅ 验证文章内容的准确性
- 📱 实时预览文章效果

### 我需要什么基础？

**零编程基础！** 只需要：
- ✅ 会用微信
- ✅ 会打字
- ✅ 会复制粘贴

### 有什么好处？

**传统方式：**
- ❌ 手动挑选主题（耗时）
- ❌ 手动设计封面（困难）
- ❌ 人工检查内容（易错）
- ❌ 反复调整预览（麻烦）

**使用本技能：**
- ✅ AI 自动推荐（1 秒）
- ✅ AI 生成封面提示词（5 秒）
- ✅ 自动验证内容（准确）
- ✅ 实时预览效果（方便）

---

## 第一次使用

### 步骤 1：打开终端

**Mac 用户：**
1. 按 `Cmd + 空格`
2. 搜索 "终端"
3. 打开"终端"应用

**Windows 用户：**
1. 按 `Win + R`
2. 输入 "cmd"
3. 按回车

### 步骤 2：进入技能目录

在终端中输入：

```bash
cd /Users/jumpermac/.openclaw/workspace/skills/wechat-article-writer/scripts
```

### 步骤 3：测试功能

输入：

```bash
python3 ai_assistant.py "帮助"
```

你会看到所有可用功能的列表。

### 步骤 4：尝试第一个功能

输入：

```bash
python3 ai_assistant.py "有哪些主题？"
```

你会看到 25 个主题的列表。

---

## 常用场景

### 场景 1：写完文章，不知道用什么主题

**你的需求：** 写了一篇康复文章，不知道选什么排版主题。

**操作步骤：**

1. 在终端输入：
   ```bash
   python3 ai_assistant.py "分析这篇文章：臀肌挛缩康复指南"
   ```

2. AI 会输出：
   ```
   📊 文章分析报告
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
   🏷️  关键词:
      1. 康复
      2. 训练
      3. 医疗
   
   🎨 推荐主题：warm_artistic (温暖文艺)
      - 适合康复健康类内容
   ```

3. 使用推荐的主题导出文章即可。

**效果：** AI 推荐了"温暖文艺"主题，适合康复科普文章。

---

### 场景 2：需要生成封面图片

**你的需求：** 文章写好了，需要一张封面图。

**操作步骤：**

1. 在终端输入：
   ```bash
   python3 ai_assistant.py "生成封面：康复训练指南，医疗风格"
   ```

2. AI 会输出：
   ```
   🖼️  封面提示词生成
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
   📝 主提示词:
      微信公众号封面图，医疗专业风格，
      主题元素：简洁，专业，可信赖，清爽
      色调：绿色、蓝色、白色为主
      ...
   
   📐 尺寸:
      头条封面：900×383
      分享封面：383×383
   ```

3. 复制"主提示词"，打开豆包 AI（或其他 AI 绘画工具）
4. 粘贴提示词，生成图片
5. 下载图片，用于公众号封面

**效果：** 获得了专业的封面图片提示词，AI 绘画工具可以生成精美封面。

---

### 场景 3：想看看所有主题再决定

**你的需求：** 想看看有哪些主题可以选择。

**操作步骤：**

1. 在终端输入：
   ```bash
   python3 ai_assistant.py "有哪些主题？"
   ```

2. AI 会输出 25 个主题的列表：
   ```
   🎨 主题列表
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
   📚 经典主题:
      • warm_artistic           - 温暖文艺
      • tech_modern             - 科技现代
      • minimal_business        - 极简商务
      ...
   
   🍬 马卡龙主题:
      • macaron_pink            - 马卡龙粉
      • macaron_blue            - 马卡龙蓝
      ...
   ```

3. 选择一个喜欢的主题

**效果：** 了解了所有可选主题，可以做出更好的选择。

---

### 场景 4：文章中有数据，怕不准确

**你的需求：** 文章中有"90% 的患者有效"这样的数据，想验证准确性。

**操作步骤：**

1. 在终端输入：
   ```bash
   python3 ai_assistant.py "验证这篇文章的内容"
   ```

2. AI 会输出：
   ```
   ✅ 内容验证
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
   ⚠️  发现 3 个需要验证的事实:
      - 90% 的患者 (percentage)
      - 研究显示 (citation)
      - 2025 年统计 (time)
   
   🔍 Tavily 验证结果:
      ✅ 90% 的患者
         来源：https://example.com/study1
   ```

3. 查看验证结果，确认数据准确性

**效果：** 发现了需要验证的数据，并找到了相关来源。

---

### 场景 5：想预览文章效果

**你的需求：** 想看看文章排版后的实际效果。

**操作步骤：**

1. 在终端输入：
   ```bash
   python3 ai_assistant.py "打开预览页面"
   ```

2. 浏览器会自动打开预览页面

3. 在预览页面：
   - 选择文章
   - 切换不同主题（25 个可选）
   - 查看实际效果

**效果：** 实时看到文章在不同主题下的排版效果。

---

## 高级技巧

### 技巧 1：创建快捷命令

**问题：** 每次都要输入很长的路径，太麻烦。

**解决方案：** 创建快捷命令。

**操作步骤：**

1. 打开终端配置文件：
   ```bash
   nano ~/.zshrc
   ```

2. 在文件末尾添加：
   ```bash
   alias wechat-ai="cd /Users/jumpermac/.openclaw/workspace/skills/wechat-article-writer/scripts && python3 ai_assistant.py"
   ```

3. 保存并退出（按 `Ctrl+O`，回车，`Ctrl+X`）

4. 重新加载配置：
   ```bash
   source ~/.zshrc
   ```

**之后就可以在任何地方直接使用：**
```bash
wechat-ai "分析文章：康复指南"
wechat-ai "生成封面：AI 发展"
wechat-ai "有哪些主题？"
```

---

### 技巧 2：批量分析多篇文章

**问题：** 有多篇文章需要分析，一篇篇太慢。

**解决方案：** 使用批量处理。

**操作步骤：**

创建一个脚本 `batch_analyze.sh`：

```bash
#!/bin/bash

articles=(
    "article_1.md"
    "article_2.md"
    "article_3.md"
)

for article in "${articles[@]}"; do
    echo "分析：$article"
    python3 ai_assistant.py "分析这篇文章：$article"
done
```

运行：
```bash
bash batch_analyze.sh
```

**效果：** 一次性分析多篇文章。

---

### 技巧 3：自定义主题配置

**问题：** 现有主题不太满意，想自己调整。

**解决方案：** 复制并修改现有主题。

**操作步骤：**

1. 复制现有主题：
   ```bash
   cd /Users/jumpermac/.openclaw/workspace/skills/wechat-article-writer/themes/classic
   cp warm_artistic.yaml my_theme.yaml
   ```

2. 编辑 `my_theme.yaml`：
   ```yaml
   name: 我的主题
   description: 自定义描述
   keywords:
     - 康复
     - 健康
     - 医疗
   colors:
     primary: "#07c160"  # 主色调
     accent: "#34c759"   # 强调色
   ```

3. 使用自定义主题：
   ```bash
   python3 ai_assistant.py "分析文章：xxx"
   # 然后手动选择 my_theme
   ```

**效果：** 拥有了个性化的主题配置。

---

## 常见问题

### Q1: 终端打不开怎么办？

**解决方案：**
- Mac：按 `Cmd + 空格`，搜索"终端"
- Windows：按 `Win + R`，输入"cmd"
- 如果还是不行，重启电脑再试

---

### Q2: 提示"command not found"怎么办？

**原因：** Python 未安装或路径不对。

**解决方案：**

1. 检查 Python 是否安装：
   ```bash
   python3 --version
   ```

2. 如果未安装，下载安装：
   - 访问 https://www.python.org/downloads/
   - 下载并安装 Python 3.8+

3. 重新尝试运行命令

---

### Q3: AI 推荐的主题不喜欢怎么办？

**解决方案：**

1. 查看所有主题：
   ```bash
   python3 ai_assistant.py "有哪些主题？"
   ```

2. 手动选择一个喜欢的主题

3. 或者告诉 AI 你的偏好：
   ```bash
   python3 ai_assistant.py "我想要更活泼的主题"
   ```

---

### Q4: 封面图片如何生成？

**解决方案：**

1. 生成提示词：
   ```bash
   python3 ai_assistant.py "生成封面：文章标题，医疗风格"
   ```

2. 复制"主提示词"

3. 打开 AI 绘画工具：
   - 豆包 AI：https://www.doubao.com/
   - 文心一格：https://yige.baidu.com/
   - Midjourney（需要 Discord）

4. 粘贴提示词，生成图片

5. 下载图片，用于公众号

---

### Q5: 内容验证收费吗？

**答案：**

- Tavily 有**免费额度**（通常每月 1000 次搜索）
- 超出后需要付费（约 $0.01/次）
- 个人使用通常免费额度就够了

**查看使用量：**
- 登录 Tavily 官网查看
- 或运行 `python3 ai_assistant.py "检查配置"`

---

### Q6: 可以不用终端吗？

**答案：** 目前需要终端，但未来会开发图形界面。

**替代方案：**
- 使用 macOS 的"自动操作"创建快捷方式
- 使用第三方工具（如 Alfred）创建快捷命令

---

## 故障排除

### 问题 1：命令运行后没反应

**可能原因：**
- 路径不对
- Python 版本太低
- 依赖未安装

**解决方案：**

1. 确认路径正确：
   ```bash
   pwd
   # 应该显示：/Users/jumpermac/.openclaw/workspace/skills/wechat-article-writer/scripts
   ```

2. 检查 Python 版本：
   ```bash
   python3 --version
   # 应该是 3.8 或更高
   ```

3. 安装依赖：
   ```bash
   pip3 install pyyaml python-dotenv
   ```

---

### 问题 2：提示"ModuleNotFoundError"

**原因：** 缺少 Python 依赖包。

**解决方案：**

```bash
pip3 install pyyaml python-dotenv tavily-python
```

---

### 问题 3：预览页面打不开

**可能原因：**
- 文件不存在
- 浏览器问题

**解决方案：**

1. 检查文件是否存在：
   ```bash
   ls ../preview_enhanced.html
   ```

2. 手动打开：
   - 打开 Finder
   - 进入目录
   - 双击 `preview_enhanced.html`

---

### 问题 4：主题推荐不准确

**可能原因：**
- 文章标题太短
- 关键词不明确

**解决方案：**

1. 提供更详细的标题：
   ```bash
   python3 ai_assistant.py "分析这篇文章：膝盖康复训练指南，针对髂胫束综合征"
   ```

2. 或者手动选择主题：
   ```bash
   python3 ai_assistant.py "有哪些主题？"
   ```

---

## 获取帮助

### 方式 1：查看帮助文档

```bash
python3 ai_assistant.py "帮助"
```

### 方式 2：阅读详细文档

- **快速入门：** `QUICKSTART.md`
- **自然语言指令：** `NATURAL_LANGUAGE_GUIDE.md`
- **功能详解：** `ENHANCED_FEATURES.md`

### 方式 3：联系支持

- GitHub Issues: https://github.com/jumperrong/clawbackup/issues
- 邮件支持：[你的邮箱]

---

## 总结

**使用本技能的步骤：**

1. ✅ 打开终端
2. ✅ 进入技能目录
3. ✅ 用自然语言描述需求
4. ✅ 复制 AI 的输出结果
5. ✅ 完成文章发布

**记住这 5 个常用指令：**

```bash
# 1. 分析文章
python3 ai_assistant.py "分析这篇文章：xxx"

# 2. 生成封面
python3 ai_assistant.py "生成封面：xxx"

# 3. 查看主题
python3 ai_assistant.py "有哪些主题？"

# 4. 验证内容
python3 ai_assistant.py "验证这篇文章的内容"

# 5. 获取帮助
python3 ai_assistant.py "帮助"
```

**你只需要：**
- 说人话
- 复制结果
- 完成发布

**剩下的交给我！** 🦞

---

_最后更新：2026-03-11_  
_版本：v1.0.0_  
_作者：AI Assistant_
