#!/bin/bash

# 记忆能力状态检查脚本
# 检测记忆系统状态，降级时发送钉钉通知

LOG_FILE="/Users/jumpermac/.openclaw/workspace/logs/memory-status.log"
TIMESTAMP=$(date "+%Y-%m-%d %H:%M:%S")
MEMORY_DIR="/Users/jumpermac/.openclaw/workspace/memory"
MEMOS_CONFIG="/Users/jumpermac/.openclaw/extensions/memos-cloud-openclaw-plugin/config.json"

echo "[$TIMESTAMP] ================================" | tee -a "$LOG_FILE"
echo "[$TIMESTAMP] 开始记忆能力检查..." | tee -a "$LOG_FILE"

# 1. 检查本地记忆文件
LOCAL_FILES=$(ls -1 "$MEMORY_DIR"/*.md 2>/dev/null | wc -l | tr -d ' ')
echo "[$TIMESTAMP] 本地记忆文件：$LOCAL_FILES 个" | tee -a "$LOG_FILE"

# 2. 检查索引文件
if [ -f "$MEMORY_DIR/chunks.json" ] && [ -f "$MEMORY_DIR/meta.json" ]; then
    echo "[$TIMESTAMP] ✅ 索引文件存在" | tee -a "$LOG_FILE"
    INDEX_STATUS="OK"
else
    echo "[$TIMESTAMP] ❌ 索引文件缺失" | tee -a "$LOG_FILE"
    INDEX_STATUS="DEGRADED"
fi

# 3. 检查 MemOS Cloud 配置
if [ -f "$MEMOS_CONFIG" ]; then
    RECALL_ENABLED=$(cat "$MEMOS_CONFIG" | grep -o '"recallEnabled": *true' | wc -l | tr -d ' ')
    if [ "$RECALL_ENABLED" -gt 0 ]; then
        echo "[$TIMESTAMP] ✅ MemOS Cloud 已启用" | tee -a "$LOG_FILE"
        CLOUD_STATUS="OK"
    else
        echo "[$TIMESTAMP] ⚠️ MemOS Cloud 已禁用" | tee -a "$LOG_FILE"
        CLOUD_STATUS="DEGRADED"
    fi
else
    echo "[$TIMESTAMP] ❌ MemOS 配置文件不存在" | tee -a "$LOG_FILE"
    CLOUD_STATUS="DEGRADED"
fi

# 4. 判断是否降级
if [ "$INDEX_STATUS" = "DEGRADED" ] || [ "$CLOUD_STATUS" = "DEGRADED" ]; then
    echo "[$TIMESTAMP] 🚨 记忆能力降级！" | tee -a "$LOG_FILE"
    
    # 发送钉钉通知
    local MESSAGE="🚨 记忆能力降级通告\n\n本地索引：$INDEX_STATUS\n云端记忆：$CLOUD_STATUS\n本地文件：$LOCAL_FILES 个\n\n请及时检查修复！"
    node /Users/jumpermac/.openclaw/workspace/scripts/send-dingtalk-notify.js "$MESSAGE" >> "$LOG_FILE" 2>&1
    
    echo "[$TIMESTAMP] 📬 已发送钉钉通知" | tee -a "$LOG_FILE"
else
    echo "[$TIMESTAMP] ✅ 记忆能力正常" | tee -a "$LOG_FILE"
fi

echo "[$TIMESTAMP] ================================" | tee -a "$LOG_FILE"
