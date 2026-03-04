#!/bin/bash
# 设置 Agent 每日自动备份 cron 任务

CRON_ENTRY="0 3 * * * /Users/jumpermac/.openclaw/workspace/scripts/agent-backup.sh backup >> /Users/jumpermac/.openclaw/backups/backup.log 2>&1"

echo "🦞 OpenClaw Agent 自动备份设置"
echo "================================"
echo
echo "即将添加以下 cron 任务："
echo "  $CRON_ENTRY"
echo
echo "这将在每天凌晨 3 点自动备份你的 Agent 状态"
echo

# 检查现有 crontab
echo "当前的 crontab 任务："
crontab -l 2>/dev/null || echo "  (暂无任务)"
echo

# 添加新任务
(crontab -l 2>/dev/null | grep -v "agent-backup.sh"; echo "$CRON_ENTRY") | crontab -

echo
echo "✓ 设置完成！"
echo
echo "新的 crontab 任务："
crontab -l
echo
echo "💡 提示："
echo "  - 查看备份日志：cat ~/.openclaw/backups/backup.log"
echo "  - 编辑 crontab:  crontab -e"
echo "  - 删除此任务：  crontab -e 然后删除对应行"
