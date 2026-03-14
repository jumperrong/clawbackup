#!/bin/bash
# check-openclaw-version.sh - 检查 OpenClaw 版本并通知（不自主更新）

WORKSPACE="/Users/jumpermac/.openclaw/workspace"
LOG_FILE="$WORKSPACE/logs/version-check.log"

# 获取当前版本
CURRENT_VERSION=$(openclaw --version 2>&1 | grep -oE '[0-9]+\.[0-9]+\.[0-9]+' | head -1)

# 获取最新版本（通过 GitHub API）
LATEST_VERSION=$(curl -s --connect-timeout 5 https://api.github.com/repos/openclaw/openclaw/releases/latest 2>/dev/null | grep '"tag_name"' | grep -oE '[0-9]+\.[0-9]+\.[0-9]+')

# 记录日志
mkdir -p "$(dirname "$LOG_FILE")"
echo "[$(date '+%Y-%m-%d %H:%M:%S')] 当前版本：$CURRENT_VERSION" >> "$LOG_FILE"

if [ -n "$LATEST_VERSION" ]; then
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] 最新版本：$LATEST_VERSION" >> "$LOG_FILE"
    
    # 比较版本
    if [ "$CURRENT_VERSION" != "$LATEST_VERSION" ]; then
        # 版本不同，发送钉钉通知
        MESSAGE="🔔 OpenClaw 版本更新提醒

📦 当前版本：$CURRENT_VERSION
🆕 最新版本：$LATEST_VERSION

⚠️ 检测到新版本，但是不会自动更新。

如需更新，请运行：
openclaw update"
        
        echo "$MESSAGE" >> "$LOG_FILE"
        echo "[$(date '+%Y-%m-%d %H:%M:%S')] ✅ 发现新版本：$LATEST_VERSION，请查看钉钉通知" >> "$LOG_FILE"
        
        # 输出消息（由 heartbeat 处理发送）
        echo "$MESSAGE"
    else
        echo "[$(date '+%Y-%m-%d %H:%M:%S')] ✅ 已是最新版本" >> "$LOG_FILE"
    fi
else
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] ❌ 无法获取最新版本" >> "$LOG_FILE"
fi
