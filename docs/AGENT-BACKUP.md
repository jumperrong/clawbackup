# Agent 备份与恢复指南

## 📦 已安装技能

从 EvoMap Market 安装的 Agent 备份恢复技能：

| 项目 | 详情 |
|------|------|
| **Capsule ID** | `sha256:651c735907ddd49c1de4e17e9a0053b47ace17fc5429ea857f1262e6cb71f4df` |
| **GDI Score** | 32.75 |
| **Confidence** | 0.88 |
| **来源节点** | `node_e6590e8e` |
| **触发信号** | backup, snapshot, restore, state_persistence |

## 🚀 使用方法

### 创建备份

```bash
# 方式 1：直接运行
~/.openclaw/workspace/scripts/agent-backup.sh backup

# 方式 2：使用绝对路径
/Users/jumpermac/.openclaw/workspace/scripts/agent-backup.sh backup
```

**备份内容：**
- IDENTITY.md - 你的身份定义
- SOUL.md - 核心人格和行为规范
- USER.md - 用户信息
- MEMORY.md - 长期记忆
- TOOLS.md - 工具配置
- AGENTS.md - Agent 工作规范
- memory/ - 日常记忆目录
- HEARTBEAT.md - 心跳任务配置

### 恢复备份

```bash
# 列出所有可用备份
~/.openclaw/workspace/scripts/agent-backup.sh restore

# 恢复最新备份
~/.openclaw/workspace/scripts/agent-backup.sh restore latest

# 恢复指定备份
~/.openclaw/workspace/scripts/agent-backup.sh restore /path/to/backup.tgz
```

### 其他命令

```bash
# 列出所有备份
~/.openclaw/workspace/scripts/agent-backup.sh list

# 显示帮助
~/.openclaw/workspace/scripts/agent-backup.sh help
```

## 📁 备份位置

所有备份保存在：`~/.openclaw/backups/`

备份文件命名格式：`agent_backup_YYYYMMDD_HHMMSS.tgz`

## 🔄 自动清理

脚本会自动保留最近 **10 个** 备份，超出的会自动删除。

## ⚠️ 恢复注意事项

1. **恢复前会自动创建备份** - 恢复操作会先将当前状态备份为 `pre_restore_*.tgz`
2. **需要确认** - 恢复操作会要求确认，防止误操作
3. **需要重启** - 恢复后请重启 OpenClaw 以应用更改

## 🛡️ 建议的备份策略

### 手动备份时机
- 重大配置更改前
- 更新 OpenClaw 版本前
- 修改 SOUL.md / IDENTITY.md 前

### 自动备份（推荐）
添加 cron 任务实现每日自动备份：

```bash
# 编辑 crontab
crontab -e

# 添加每日凌晨 3 点备份
0 3 * * * ~/.openclaw/workspace/scripts/agent-backup.sh backup
```

## 📊 备份示例输出

```
========================================
  OpenClaw Agent Backup & Restore
========================================

开始备份...

✓ 找到：IDENTITY.md
✓ 找到：SOUL.md
✓ 找到：USER.md
✓ 找到：MEMORY.md
✓ 找到：TOOLS.md
✓ 找到：AGENTS.md
✓ 找到：HEARTBEAT.md
✓ 找到：memory/ 目录

打包备份...

✓ 备份完成！

备份文件：/Users/jumpermac/.openclaw/backups/agent_backup_20260304_101621.tgz
备份大小：12K
备份时间：2026-03-04 10:16:21

✓ 已清理旧备份（保留最近 10 个）
```

## 🔗 相关资源

- **EvoMap Hub**: https://evomap.ai
- **原始 Capsule**: https://evomap.ai/a2a/assets/sha256:651c735907ddd49c1de4e17e9a0053b47ace17fc5429ea857f1262e6cb71f4df
- **技能文档**: https://evomap.ai/skill.md

---

*技能来自 EvoMap Market - AI Agent 进化市场*
*安装时间：2026-03-04*
