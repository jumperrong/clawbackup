# OpenClaw Agent 备份与恢复

这个目录包含 OpenClaw Agent 的完整状态备份，用于在清空 workspace 或全新安装后恢复。

## 📦 备份内容

- `agent_backup_*.tgz` - Agent 状态压缩包

包含以下核心文件：
- `IDENTITY.md` - 身份定义
- `SOUL.md` - 核心人格和行为规范
- `USER.md` - 用户信息
- `MEMORY.md` - 长期记忆
- `TOOLS.md` - 工具配置
- `AGENTS.md` - Agent 工作规范
- `HEARTBEAT.md` - 心跳任务配置
- `memory/` - 日常记忆目录

## 🚀 全新安装后恢复步骤

### 步骤 1：克隆备份仓库

```bash
# 克隆备份仓库到临时目录
git clone git@github.com:jumperrong/clawbackup.git /tmp/claw-backup
```

### 步骤 2：安装 OpenClaw（如果还没安装）

```bash
# 安装 OpenClaw
npm install -g openclaw

# 初始化 workspace（会创建 ~/.openclaw/workspace）
openclaw
```

### 步骤 3：恢复备份

```bash
# 进入 workspace 目录
cd ~/.openclaw/workspace

# 复制备份文件
cp /tmp/claw-backup/backups/agent_backup_*.tgz .

# 解压恢复
tar -xzf agent_backup_*.tgz

# 清理临时文件
rm agent_backup_*.tgz
rm -rf /tmp/claw-backup
```

### 步骤 4：验证恢复

```bash
# 检查核心文件是否存在
ls -la ~/.openclaw/workspace/*.md
ls -la ~/.openclaw/workspace/memory/
```

### 步骤 5：重启 OpenClaw

```bash
# 重启 OpenClaw 服务
openclaw restart

# 或者重新连接你的聊天客户端
```

---

## 🛠️ 备份脚本（可选）

如果你想在本地继续创建新备份，可以使用备份脚本：

```bash
# 运行备份
~/.openclaw/workspace/scripts/agent-backup.sh backup

# 查看备份列表
~/.openclaw/workspace/scripts/agent-backup.sh list

# 恢复备份
~/.openclaw/workspace/scripts/agent-backup.sh restore latest
```

---

## 📅 更新 GitHub 备份

当你创建了新的备份后，推送到 GitHub：

```bash
cd ~/.openclaw/workspace

# 添加新备份文件
git add backups/

# 提交
git commit -m "backup: add agent state backup $(date +%Y%m%d)"

# 推送
git push origin main
```

---

## ⚠️ 注意事项

1. **备份频率** - 建议每次重大更改后都创建新备份并推送
2. **隐私** - 备份包含你的个人记忆和配置，确保仓库是私有的
3. **版本管理** - 保留多个备份版本，不要删除旧备份（除非确定不需要）
4. **自动备份** - 可以设置 cron 任务自动备份并推送

---

## 🔗 相关资源

- **OpenClaw 文档**: https://docs.openclaw.ai
- **EvoMap 技能市场**: https://evomap.ai

---

*最后更新：2026-03-04*
