#!/bin/bash

# 所有插件统一更新脚本
# 一次性更新所有已安装的插件

set -e

LOG_FILE="/Users/jumpermac/.openclaw/workspace/logs/all-plugins-update.log"
TIMESTAMP=$(date "+%Y-%m-%d %H:%M:%S")

echo "[$TIMESTAMP] ========================================" | tee -a "$LOG_FILE"
echo "[$TIMESTAMP] 开始批量更新所有插件..." | tee -a "$LOG_FILE"
echo "[$TIMESTAMP] ========================================" | tee -a "$LOG_FILE"

# 1. 更新飞书官方插件
echo "" | tee -a "$LOG_FILE"
echo "[$TIMESTAMP] [1/2] 更新飞书插件..." | tee -a "$LOG_FILE"
npx -y @larksuite/openclaw-lark-tools update 2>&1 | tee -a "$LOG_FILE"

# 2. 更新 Memos Cloud 插件
echo "" | tee -a "$LOG_FILE"
echo "[$TIMESTAMP] [2/2] 更新 Memos Cloud 插件..." | tee -a "$LOG_FILE"
bash /Users/jumpermac/.openclaw/workspace/scripts/update-memos-plugin.sh 2>&1 | tee -a "$LOG_FILE"

# 3. 重启网关
echo "" | tee -a "$LOG_FILE"
echo "[$TIMESTAMP] 重启网关以应用更新..." | tee -a "$LOG_FILE"
openclaw gateway restart 2>&1 | tee -a "$LOG_FILE"

echo "" | tee -a "$LOG_FILE"
echo "[$TIMESTAMP] ========================================" | tee -a "$LOG_FILE"
echo "[$TIMESTAMP] ✅ 所有插件更新完成！" | tee -a "$LOG_FILE"
echo "[$TIMESTAMP] ========================================" | tee -a "$LOG_FILE"
