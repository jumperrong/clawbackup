#!/bin/bash
# OpenClaw 每日更新检查脚本

LOG_FILE="$HOME/.openclaw/workspace/logs/daily-update.log"
NOTIFY_FILE="$HOME/.openclaw/workspace/logs/pending-notify.txt"
SESSIONS_FILE="$HOME/.openclaw/workspace/logs/last-session-key.txt"

echo "=========================================="
echo "检查时间：$(date)"
echo "=========================================="

# 检查当前安装的 OpenClaw 版本
CURRENT_VERSION=$(npm list -g openclaw 2>/dev/null | grep openclaw | awk -F'@' '{print $2}' | tail -1)
echo "当前 OpenClaw 版本：$CURRENT_VERSION"

# 检查 npm 上最新版本
LATEST_VERSION=$(npm view openclaw version 2>/dev/null)
echo "最新 OpenClaw 版本：$LATEST_VERSION"

# 比较版本（去除可能的空格和换行）
CURRENT_TRIMMED=$(echo "$CURRENT_VERSION" | tr -d '[:space:]')
LATEST_TRIMMED=$(echo "$LATEST_VERSION" | tr -d '[:space:]')

if [ "$CURRENT_TRIMMED" != "$LATEST_TRIMMED" ] && [ -n "$LATEST_TRIMMED" ]; then
    echo "发现新版本！正在更新..."
    
    # 执行更新
    UPDATE_OUTPUT=$(npm install -g openclaw@latest 2>&1)
    UPDATE_CODE=$?
    
    if [ $UPDATE_CODE -eq 0 ]; then
        NEW_VERSION=$(npm list -g openclaw 2>/dev/null | grep openclaw | awk -F'@' '{print $2}' | tail -1)
        echo "更新成功！已更新到版本：$NEW_VERSION"
        
        # 写入通知文件
        cat > "$NOTIFY_FILE" << EOF
🎉 OpenClaw 更新完成！

已从 \`$CURRENT_TRIMMED\` 更新到 \`$NEW_VERSION\`
更新时间：$(date '+%Y-%m-%d %H:%M:%S')
EOF
        echo "通知已写入：$NOTIFY_FILE"
    else
        echo "更新失败：$UPDATE_OUTPUT"
        # 写入失败通知
        cat > "$NOTIFY_FILE" << EOF
⚠️ OpenClaw 更新失败

当前版本：$CURRENT_TRIMMED
目标版本：$LATEST_TRIMMED
错误信息：$UPDATE_OUTPUT
更新时间：$(date '+%Y-%m-%d %H:%M:%S')
EOF
        echo "失败通知已写入：$NOTIFY_FILE"
    fi
else
    echo "OpenClaw 已是最新版本，无需更新。"
fi

echo ""
