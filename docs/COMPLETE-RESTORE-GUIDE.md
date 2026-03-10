# OpenClaw 完整恢复指南

> 📅 最后更新：2026-03-10 10:00  
> 📦 备份版本：af7ea6f  
> 🔗 GitHub: https://github.com/jumperrong/clawbackup

---

## 📋 目录

1. [快速恢复（推荐）](#快速恢复推荐)
2. [完整恢复步骤](#完整恢复步骤)
3. [配置文件说明](#配置文件说明)
4. [技能恢复](#技能恢复)
5. [记忆系统恢复](#记忆系统恢复)
6. [自动化配置](#自动化配置)
7. [故障排查](#故障排查)

---

## 🚀 快速恢复（推荐）

### 前提条件

- ✅ macOS 系统
- ✅ Node.js 22+ (`node -v`)
- ✅ npm 已安装 (`npm -v`)
- ✅ Git 已配置

### 一键恢复脚本

```bash
# 1. 克隆备份仓库
git clone git@github.com:jumperrong/clawbackup.git ~/openclaw-workspace

# 2. 进入目录
cd ~/openclaw-workspace

# 3. 安装 OpenClaw（如果未安装）
npm install -g openclaw@latest

# 4. 复制配置文件到正确位置
cp -r ~/openclaw-workspace ~/.openclaw/workspace

# 5. 重启 OpenClaw
openclaw gateway restart
```

---

## 📖 完整恢复步骤

### 步骤 1：安装 OpenClaw

```bash
# 安装最新版
npm install -g openclaw@latest

# 验证安装
openclaw --version
```

### 步骤 2：恢复配置文件

```bash
# 创建配置目录
mkdir -p ~/.openclaw

# 恢复主配置
cp ~/openclaw-workspace/openclaw.json ~/.openclaw/workspace/

# 恢复环境变量（如果有）
cp ~/openclaw-workspace/.env ~/.openclaw/ 2>/dev/null || echo "无 .env 文件"
```

### 步骤 3：恢复记忆系统

```bash
# 恢复长期记忆
cp ~/openclaw-workspace/MEMORY.md ~/.openclaw/workspace/

# 恢复 daily notes
cp -r ~/openclaw-workspace/memory/ ~/.openclaw/workspace/

# 恢复行为协议文件
cp ~/openclaw-workspace/{AGENTS.md,SOUL.md,USER.md,TOOLS.md,HEARTBEAT.md} ~/.openclaw/workspace/
```

### 步骤 4：恢复技能

```bash
# 恢复所有技能
cp -r ~/openclaw-workspace/skills/* ~/.openclaw/workspace/skills/

# 验证技能
ls -la ~/.openclaw/workspace/skills/
```

### 步骤 5：恢复自动化配置

```bash
# 恢复 LaunchAgent 配置
cp ~/openclaw-workspace/com.openclaw.*.plist ~/Library/LaunchAgents/

# 加载 LaunchAgent
launchctl load ~/Library/LaunchAgents/com.openclaw.daily-update-check.plist

# 恢复定时脚本
cp -r ~/openclaw-workspace/scripts/ ~/.openclaw/workspace/
```

### 步骤 6：验证恢复

```bash
# 检查网关状态
openclaw gateway status

# 检查记忆系统
openclaw memory status

# 检查技能列表
ls ~/.openclaw/workspace/skills/
```

---

## 📁 配置文件说明

### 核心配置

| 文件 | 路径 | 用途 | 备份状态 |
|------|------|------|---------|
| **openclaw.json** | `~/.openclaw/workspace/` | 主配置文件 | ✅ 已备份 |
| **.env** | `~/.openclaw/` | 环境变量（API Keys） | ⚠️ 需手动配置 |
| **HEARTBEAT.md** | `~/.openclaw/workspace/` | 心跳任务配置 | ✅ 已备份 |

### 记忆系统

| 文件 | 路径 | 用途 | 备份状态 |
|------|------|------|---------|
| **MEMORY.md** | `~/.openclaw/workspace/` | 长期记忆 | ✅ 已备份 |
| **memory/*.md** | `~/.openclaw/workspace/memory/` | Daily notes | ✅ 已备份 |
| **AGENTS.md** | `~/.openclaw/workspace/` | Agent 行为规范 | ✅ 已备份 |
| **SOUL.md** | `~/.openclaw/workspace/` | Agent 人格定义 | ✅ 已备份 |
| **USER.md** | `~/.openclaw/workspace/` | 用户信息 | ✅ 已备份 |
| **TOOLS.md** | `~/.openclaw/workspace/` | 工具使用笔记 | ✅ 已备份 |
| **IDENTITY.md** | `~/.openclaw/workspace/` | Agent 身份 | ✅ 已备份 |

### 技能配置

| 技能 | 路径 | 用途 | 备份状态 |
|------|------|------|---------|
| **wechat-article-writer** | `skills/` | 微信公众号自动生成 | ✅ 已备份 |
| **find-skills** | `skills/` | 技能发现工具 | ✅ 已备份 |
| **proactive-agent** | `skills/` | 主动 Agent 模式 | ✅ 已备份 |
| **tavily-search** | `skills/` | Tavily 搜索 | ✅ 已备份 |

---

## 🛠️ 技能恢复

### 微信公众号技能

```bash
# 1. 恢复技能文件
cp -r ~/openclaw-workspace/skills/wechat-article-writer \
      ~/.openclaw/workspace/skills/

# 2. 配置 API Keys（编辑 config.json）
cd ~/.openclaw/workspace/skills/wechat-article-writer
nano config.json

# 3. 测试技能
python3 scripts/generate_image.py --topic "测试" --style 干货
```

**需要的 API Keys：**
- ✅ Bailian API Key（通义千问）- 已配置
- ✅ 豆包 API Key（生图）- 已配置
- ⚠️ 微信公众号 AppID/Secret - 需手动配置

### 搜索技能

```bash
# 恢复 Tavily 搜索
cp -r ~/openclaw-workspace/skills/tavily-search \
      ~/.openclaw/workspace/skills/

# Tavily API Key 已在配置中
```

---

## 🧠 记忆系统恢复

### 恢复长期记忆

```bash
# 复制 MEMORY.md
cp ~/openclaw-workspace/MEMORY.md ~/.openclaw/workspace/

# 验证内容
cat ~/.openclaw/workspace/MEMORY.md | head -20
```

### 恢复 Daily Notes

```bash
# 复制所有 daily notes
cp -r ~/openclaw-workspace/memory/ ~/.openclaw/workspace/

# 查看 daily notes
ls -la ~/.openclaw/workspace/memory/
```

### 验证记忆系统

```bash
# 检查记忆状态
openclaw memory status

# 应该显示：
# - Indexed: 2/2 files
# - FTS: ready
```

---

## ⚙️ 自动化配置

### LaunchAgent 配置

```bash
# 1. 复制 LaunchAgent 配置
cp ~/openclaw-workspace/com.openclaw.*.plist ~/Library/LaunchAgents/

# 2. 加载配置
launchctl load ~/Library/LaunchAgents/com.openclaw.daily-update-check.plist

# 3. 验证状态
launchctl list | grep openclaw
```

### 定时任务说明

**com.openclaw.daily-update-check.plist**
- ⏰ 执行时间：每天 09:00
- 📝 功能：检查 OpenClaw 更新
- 📬 通知：通过飞书发送

**脚本位置：**
- `scripts/daily-update-check.sh` - 检查更新
- `scripts/send-feishu-notify.js` - 发送飞书通知

---

## 🔧 故障排查

### 问题 1：网关无法启动

```bash
# 检查配置
openclaw gateway status

# 重启网关
openclaw gateway restart

# 查看日志
tail -f ~/.openclaw/logs/gateway.log
```

### 问题 2：技能不显示

```bash
# 检查技能目录
ls -la ~/.openclaw/workspace/skills/

# 重新加载技能
openclaw skills reload

# 重启网关
openclaw gateway restart
```

### 问题 3：记忆系统不可用

```bash
# 检查记忆状态
openclaw memory status

# 重新索引
openclaw memory index --force

# 验证文件
cat ~/.openclaw/workspace/MEMORY.md
```

### 问题 4：Git 推送失败

```bash
# 检查 SSH key
ssh -T git@github.com

# 如果没有配置，重新生成
ssh-keygen -t ed25519 -C "your_email@example.com"

# 添加到 GitHub
# https://github.com/settings/keys
```

### 问题 5：API Keys 丢失

```bash
# 检查配置文件
cat ~/.openclaw/workspace/skills/wechat-article-writer/config.json

# 重新配置 API Keys
nano ~/.openclaw/workspace/skills/wechat-article-writer/config.json

# 重启网关
openclaw gateway restart
```

---

## 📊 备份清单

### ✅ 已备份内容

**配置文件：**
- [x] openclaw.json
- [x] HEARTBEAT.md
- [x] MEMORY.md
- [x] AGENTS.md
- [x] SOUL.md
- [x] USER.md
- [x] TOOLS.md
- [x] IDENTITY.md
- [x] MODELS.md

**技能：**
- [x] wechat-article-writer（微信公众号）
- [x] find-skills（技能发现）
- [x] proactive-agent（主动 Agent）
- [x] tavily-search（搜索）

**脚本：**
- [x] daily-update-check.sh（每日检查）
- [x] send-feishu-notify.js（飞书通知）
- [x] check-and-send-notify.sh（检查并通知）

**自动化：**
- [x] com.openclaw.daily-update-check.plist（LaunchAgent）

**记忆：**
- [x] memory/2026-03-02.md（Daily note）

### ⚠️ 需手动配置

**敏感信息（不在 Git 中）：**
- [ ] API Keys（Bailian, 豆包，Tavily）
- [ ] 微信公众号 AppID/Secret
- [ ] 飞书 AppID/Secret
- [ ] SSH Keys
- [ ] GitHub Token

**配置方法：**
```bash
# 编辑 config.json
nano ~/.openclaw/workspace/skills/wechat-article-writer/config.json

# 添加 API Keys
{
  "bailian_api_key": "sk-xxx",
  "doubao_api_key": "xxx",
  "wechat_appid": "xxx",
  "wechat_appsecret": "xxx"
}
```

---

## 🔗 相关资源

- **GitHub 仓库**: https://github.com/jumperrong/clawbackup
- **OpenClaw 文档**: https://docs.openclaw.ai
- **最新 Commit**: af7ea6f - feat: 添加微信公众号自动生成技能 + 记忆系统更新

---

## 📝 恢复检查清单

恢复完成后，请检查以下项目：

- [ ] OpenClaw 网关正常运行
- [ ] 所有技能已加载
- [ ] 记忆系统可访问
- [ ] LaunchAgent 已配置
- [ ] API Keys 已配置
- [ ] 可以正常对话
- [ ] 心跳检查正常

---

_最后更新：2026-03-10 10:00_  
_备份版本：af7ea6f_  
_维护者：Jumpermac_
