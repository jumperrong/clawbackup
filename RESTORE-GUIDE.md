# 🦞 OpenClaw 完全恢复指南

> 当你清空 workspace 或全新安装 OpenClaw 后，使用此指南恢复所有配置和记忆。

---

## 📋 前提条件

- GitHub 账号（有权限访问 `jumperrong/clawbackup` 仓库）
- 已安装 Node.js 和 npm
- 已安装 Git

---

## 🚀 快速恢复（5 分钟）

### 1️⃣ 安装 OpenClaw

```bash
# 安装 OpenClaw（如果还没安装）
npm install -g openclaw

# 验证安装
openclaw --version
```

### 2️⃣ 克隆备份仓库

```bash
# 进入 .openclaw 目录
cd ~/.openclaw

# 如果 workspace 已存在，先备份或删除
mv workspace workspace.old  # 或者直接 rm -rf workspace

# 克隆备份仓库作为新的 workspace
git clone git@github.com:jumperrong/clawbackup.git workspace

# 进入 workspace
cd workspace
```

### 3️⃣ 恢复备份文件

```bash
# 进入 workspace 目录
cd ~/.openclaw/workspace

# 解压最新备份
cd backups
tar -xzf agent_backup_*.tgz -C ../

# 返回上级
cd ..
```

### 4️⃣ 验证恢复

```bash
# 检查核心文件
ls -la *.md
# 应该看到：IDENTITY.md, SOUL.md, USER.md, MEMORY.md, TOOLS.md, AGENTS.md 等

# 检查 memory 目录
ls -la memory/
```

### 5️⃣ 启动 OpenClaw

```bash
# 重启 OpenClaw（如果已在运行）
openclaw restart

# 或者重新连接你的聊天客户端（飞书/微信等）
```

---

## ✅ 恢复完成检查清单

- [ ] `IDENTITY.md` 存在
- [ ] `SOUL.md` 存在
- [ ] `MEMORY.md` 存在（如果有长期记忆）
- [ ] `memory/` 目录存在
- [ ] `scripts/agent-backup.sh` 可执行
- [ ] 聊天客户端能正常收到消息

---

## 🔄 后续：更新备份

当你有了新的记忆或配置更改后，记得更新 GitHub 备份：

### 手动备份并推送

```bash
# 创建新备份
~/.openclaw/workspace/scripts/agent-backup.sh backup

# 复制备份到 workspace
cp ~/.openclaw/backups/agent_backup_*.tgz ~/.openclaw/workspace/backups/

# 提交并推送
cd ~/.openclaw/workspace
git add backups/
git commit -m "backup: $(date +%Y%m%d)"
git push origin main
```

### 设置自动备份（可选）

```bash
# 运行设置脚本
~/.openclaw/workspace/scripts/setup-cron.sh
```

---

## 📚 目录结构说明

```
~/.openclaw/workspace/
├── IDENTITY.md          # 你的身份定义
├── SOUL.md              # 核心人格和行为规范
├── USER.md              # 用户信息
├── MEMORY.md            # 长期记忆
├── TOOLS.md             # 工具配置
├── AGENTS.md            # Agent 工作规范
├── HEARTBEAT.md         # 心跳任务
├── memory/              # 日常记忆目录
├── docs/                # 文档
│   └── AGENT-BACKUP.md  # 备份使用说明
├── scripts/             # 脚本
│   ├── agent-backup.sh  # 备份/恢复脚本
│   └── setup-cron.sh    # Cron 设置脚本
├── backups/             # 备份文件目录（Git 跟踪）
│   ├── README.md        # 备份说明
│   └── agent_backup_*.tgz
└── skills/              # 技能目录
    ├── find-skills/
    ├── proactive-agent/
    └── tavily-search/
```

---

## ⚠️ 故障排查

### 问题：克隆后无法启动 OpenClaw

**解决：**
```bash
# 检查文件权限
chmod +x ~/.openclaw/workspace/scripts/*.sh

# 检查核心文件是否存在
ls ~/.openclaw/workspace/*.md
```

### 问题：备份文件解压失败

**解决：**
```bash
# 检查备份文件是否完整
cd ~/.openclaw/workspace/backups
ls -lh agent_backup_*.tgz

# 尝试手动解压
tar -tvf agent_backup_YYYYMMDD_HHMMSS.tgz  # 查看内容
tar -xzf agent_backup_YYYYMMDD_HHMMSS.tgz -C ~/.openclaw/workspace/
```

### 问题：Git 推送失败

**解决：**
```bash
# 检查 Git 配置
git config user.name
git config user.email

# 如果需要，设置 Git 用户
git config --global user.name "Your Name"
git config --global user.email "your@email.com"

# 重新推送
git push origin main
```

---

## 🔐 安全提醒

1. **私有仓库** - 确保 `clawbackup` 仓库是私有的，包含个人记忆和配置
2. **定期更新** - 每次重要对话或配置更改后更新备份
3. **多重备份** - 可以考虑同时备份到多个位置（本地 + GitHub + 云盘）

---

## 📞 需要帮助？

- **OpenClaw 文档**: https://docs.openclaw.ai
- **社区**: https://discord.com/invite/clawd
- **技能市场**: https://clawhub.com

---

*最后更新：2026-03-04*
*备份仓库：https://github.com/jumperrong/clawbackup*
