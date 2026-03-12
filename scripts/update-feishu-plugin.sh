#!/bin/bash

# 飞书官方插件更新脚本
# 建议每周执行一次（如周四凌晨 3 点）

set -e

LOG_FILE="/Users/jumpermac/.openclaw/workspace/logs/feishu-plugin-update.log"
TIMESTAMP=$(date "+%Y-%m-%d %H:%M:%S")

echo "[$TIMESTAMP] 开始更新飞书插件..." | tee -a "$LOG_FILE"

# 1. 更新插件
echo "[$TIMESTAMP] 执行更新命令..." | tee -a "$LOG_FILE"
npx -y @larksuite/openclaw-lark-tools update 2>&1 | tee -a "$LOG_FILE"

# 2. 检查更新结果
if [ $? -eq 0 ]; then
    echo "[$TIMESTAMP] ✅ 插件更新成功" | tee -a "$LOG_FILE"
    
    # 3. 重启网关以应用更新
    echo "[$TIMESTAMP] 重启网关..." | tee -a "$LOG_FILE"
    openclaw gateway restart 2>&1 | tee -a "$LOG_FILE"
    
    if [ $? -eq 0 ]; then
        echo "[$TIMESTAMP] ✅ 网关重启成功" | tee -a "$LOG_FILE"
    else
        echo "[$TIMESTAMP] ❌ 网关重启失败" | tee -a "$LOG_FILE"
        exit 1
    fi
else
    echo "[$TIMESTAMP] ❌ 插件更新失败" | tee -a "$LOG_FILE"
    exit 1
fi

echo "[$TIMESTAMP] ================================" | tee -a "$LOG_FILE"
