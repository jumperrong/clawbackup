#!/bin/bash

# Memos Cloud 插件更新脚本
# Memos Cloud 是本地路径安装的插件，需要手动检查更新

set -e

LOG_FILE="/Users/jumpermac/.openclaw/workspace/logs/memos-plugin-update.log"
TIMESTAMP=$(date "+%Y-%m-%d %H:%M:%S")
PLUGIN_PATH="/Users/jumpermac/.openclaw/extensions/memos-cloud-openclaw-plugin"

echo "[$TIMESTAMP] ================================" | tee -a "$LOG_FILE"
echo "[$TIMESTAMP] 开始检查 Memos Cloud 插件..." | tee -a "$LOG_FILE"

# 1. 检查插件是否存在
if [ ! -d "$PLUGIN_PATH" ]; then
    echo "[$TIMESTAMP] ❌ 错误：插件目录不存在" | tee -a "$LOG_FILE"
    exit 1
fi

# 2. 读取当前版本
if [ -f "$PLUGIN_PATH/package.json" ]; then
    CURRENT_VERSION=$(grep '"version"' "$PLUGIN_PATH/package.json" | head -1 | awk -F'"' '{print $4}')
    echo "[$TIMESTAMP] 当前版本：$CURRENT_VERSION" | tee -a "$LOG_FILE"
else
    echo "[$TIMESTAMP] ⚠️ 无法读取版本信息" | tee -a "$LOG_FILE"
    CURRENT_VERSION="unknown"
fi

# 3. 检查是否有 git 仓库（用于检查更新）
if [ -d "$PLUGIN_PATH/.git" ]; then
    echo "[$TIMESTAMP] 检查远程更新..." | tee -a "$LOG_FILE"
    cd "$PLUGIN_PATH"
    
    # 获取最新提交
    git fetch origin 2>&1 | tee -a "$LOG_FILE"
    
    # 比较本地和远程
    LOCAL=$(git rev-parse HEAD)
    REMOTE=$(git rev-parse origin/main 2>/dev/null || git rev-parse origin/master 2>/dev/null || echo "")
    
    if [ -n "$REMOTE" ] && [ "$LOCAL" != "$REMOTE" ]; then
        echo "[$TIMESTAMP] 发现新版本，正在更新..." | tee -a "$LOG_FILE"
        git pull origin $(git rev-parse --abbrev-ref HEAD) 2>&1 | tee -a "$LOG_FILE"
        
        # 重新安装依赖
        echo "[$TIMESTAMP] 安装依赖..." | tee -a "$LOG_FILE"
        npm install --production 2>&1 | tee -a "$LOG_FILE"
        
        NEW_VERSION=$(grep '"version"' "$PLUGIN_PATH/package.json" | head -1 | awk -F'"' '{print $4}')
        echo "[$TIMESTAMP] ✅ 更新成功！版本：$CURRENT_VERSION → $NEW_VERSION" | tee -a "$LOG_FILE"
        
        # 写入通知
        cat > "/Users/jumpermac/.openclaw/workspace/logs/pending-notify.txt" << EOF
🎉 Memos Cloud 插件更新完成！

已从 \`$CURRENT_VERSION\` 更新到 \`$NEW_VERSION\`
更新时间：$(date '+%Y-%m-%d %H:%M:%S')
EOF
    else
        echo "[$TIMESTAMP] ✅ Memos Cloud 插件已是最新版本" | tee -a "$LOG_FILE"
    fi
else
    echo "[$TIMESTAMP] ⚠️ 插件不是 git 仓库，跳过自动更新" | tee -a "$LOG_FILE"
    echo "[$TIMESTAMP] 提示：本地路径安装的插件需要手动更新" | tee -a "$LOG_FILE"
fi

echo "[$TIMESTAMP] ================================" | tee -a "$LOG_FILE"
