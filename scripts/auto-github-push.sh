#!/bin/bash

# GitHub 自动推送脚本
# 用于将工作区更改推送到 GitHub 仓库

set -e

LOG_FILE="/Users/jumpermac/.openclaw/workspace/logs/github-push.log"
TIMESTAMP=$(date "+%Y-%m-%d %H:%M:%S")
WORKSPACE="/Users/jumpermac/.openclaw/workspace"
# 使用本地已配置的 remote origin（SSH 方式），不硬编码 URL
REMOTE_ORIGIN=$(git config --get remote.origin.url)

echo "[$TIMESTAMP] ================================" | tee -a "$LOG_FILE"
echo "[$TIMESTAMP] 开始 GitHub 推送检查..." | tee -a "$LOG_FILE"
echo "[$TIMESTAMP] Remote: $REMOTE_ORIGIN" | tee -a "$LOG_FILE"

cd "$WORKSPACE"

# 1. 检查是否有 Git 仓库
if [ ! -d ".git" ]; then
    echo "[$TIMESTAMP] ❌ 错误：工作区不是 Git 仓库" | tee -a "$LOG_FILE"
    exit 1
fi

# 2. 检查是否有更改
CHANGES=$(git status --porcelain 2>/dev/null | wc -l | tr -d ' ')

if [ "$CHANGES" -eq 0 ]; then
    echo "[$TIMESTAMP] ✅ 没有更改，无需推送" | tee -a "$LOG_FILE"
    exit 0
fi

echo "[$TIMESTAMP] 发现 $CHANGES 个文件更改" | tee -a "$LOG_FILE"

# 3. 添加更改
echo "[$TIMESTAMP] 添加文件..." | tee -a "$LOG_FILE"
git add -A 2>&1 | tee -a "$LOG_FILE"

# 4. 提交更改
COMMIT_MSG="Auto-commit: $(date '+%Y-%m-%d %H:%M:%S') - 自动保存工作区更改"
echo "[$TIMESTAMP] 提交更改..." | tee -a "$LOG_FILE"
git commit -m "$COMMIT_MSG" 2>&1 | tee -a "$LOG_FILE" || {
    echo "[$TIMESTAMP] ⚠️ 提交失败（可能没有实际更改）" | tee -a "$LOG_FILE"
    exit 0
}

# 5. 推送到 GitHub
echo "[$TIMESTAMP] 推送到 GitHub..." | tee -a "$LOG_FILE"
git push origin main 2>&1 | tee -a "$LOG_FILE"

PUSH_STATUS=$?

# 通过 pending-notify.txt 发送钉钉通知
send_dingtalk_notification() {
    local status="$1"
    local message="$2"
    echo "[$TIMESTAMP] 📬 准备发送钉钉通知：[$status] $message" | tee -a "$LOG_FILE"
    
    # 写入 pending 通知文件，由 heartbeat 检查时通过钉钉发送
    local NOTIFY_FILE="/Users/jumpermac/.openclaw/workspace/pending-notify.txt"
    echo "$status - $message" >> "$NOTIFY_FILE"
    echo "[$TIMESTAMP] 📝 通知已写入 $NOTIFY_FILE" | tee -a "$LOG_FILE"
}

if [ $PUSH_STATUS -eq 0 ]; then
    echo "[$TIMESTAMP] ✅ 推送成功！" | tee -a "$LOG_FILE"
    send_dingtalk_notification "✅ GitHub 推送成功" "提交已推送到 github.com:jumperrong/clawbackup.git"
else
    echo "[$TIMESTAMP] ❌ 推送失败，请检查网络连接和仓库权限" | tee -a "$LOG_FILE"
    send_dingtalk_notification "❌ GitHub 推送失败" "请检查网络或权限配置"
    exit 1
fi

echo "[$TIMESTAMP] ================================" | tee -a "$LOG_FILE"
