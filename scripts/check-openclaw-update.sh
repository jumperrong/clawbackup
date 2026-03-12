#!/bin/bash
# OpenClaw 更新检查脚本（钉钉通知版）

LOG_FILE="$HOME/.openclaw/workspace/logs/openclaw-update-check.log"

echo "==========================================" >> "$LOG_FILE"
echo "检查时间：$(date)" >> "$LOG_FILE"
echo "==========================================" >> "$LOG_FILE"

# 检查当前安装的 OpenClaw 版本
CURRENT_VERSION=$(npm list -g openclaw 2>/dev/null | grep openclaw | awk -F'@' '{print $2}' | tail -1)
echo "当前 OpenClaw 版本：$CURRENT_VERSION" >> "$LOG_FILE"

# 检查 npm 上最新版本
LATEST_VERSION=$(npm view openclaw version 2>/dev/null)
echo "最新 OpenClaw 版本：$LATEST_VERSION" >> "$LOG_FILE"

# 比较版本
CURRENT_TRIMMED=$(echo "$CURRENT_VERSION" | tr -d '[:space:]')
LATEST_TRIMMED=$(echo "$LATEST_VERSION" | tr -d '[:space:]')

if [ "$CURRENT_TRIMMED" != "$LATEST_TRIMMED" ] && [ -n "$LATEST_TRIMMED" ]; then
    echo "发现新版本！" >> "$LOG_FILE"
    
    # 通过钉钉发送更新提示
    cat << EOF
🎯 OpenClaw 有新版本可用！

当前版本：$CURRENT_TRIMMED
最新版本：$LATEST_TRIMMED

更新命令：
\`\`\`bash
npm install -g openclaw@latest
\`\`\`

更新后重启网关：
\`\`\`bash
openclaw gateway restart
\`\`\`

⚠️ 注意：更新后需要完全重启网关才能生效。
EOF
    
    echo "已发送更新提示" >> "$LOG_FILE"
else
    echo "OpenClaw 已是最新版本 ($CURRENT_TRIMMED)" >> "$LOG_FILE"
    echo "✅ 无需更新"
fi

echo "" >> "$LOG_FILE"
