#!/bin/bash
# 检查并发送待处理的通知

NOTIFY_FILE="$HOME/.openclaw/workspace/logs/pending-notify.txt"

if [ -f "$NOTIFY_FILE" ]; then
    MESSAGE=$(cat "$NOTIFY_FILE")
    echo "发现待发送通知：$MESSAGE"
    
    # 通过 openclaw 发送消息到当前会话
    # 使用 sessions_send 需要会话 key，我们尝试发送到 label
    if command -v openclaw &> /dev/null; then
        # 尝试使用 openclaw 的内部命令
        # 由于无法直接获取会话上下文，我们使用一个变通方法
        echo "尝试发送通知..."
        
        # 方法 1: 使用 openclaw message (需要 target)
        # openclaw message send --channel feishu --target "user:ou_9c3d0910ce7c8f8529dcaa2287401515" --message "$MESSAGE"
        
        # 方法 2: 使用 node 脚本调用 openclaw API
        node -e "
const { execSync } = require('child_process');
const message = \`\`\`$MESSAGE\`\`\`;
try {
    // 写入一个临时文件，让主会话读取
    const fs = require('fs');
    const path = require('path');
    const sendFile = path.join(process.env.HOME, '.openclaw/workspace/logs/pending-send.txt');
    fs.writeFileSync(sendFile, message);
    console.log('通知已写入待发送队列：' + sendFile);
} catch(e) {
    console.error('失败:', e.message);
    process.exit(1);
}
"
        
        if [ $? -eq 0 ]; then
            echo "通知已排队等待发送"
            rm "$NOTIFY_FILE"
        else
            echo "通知发送失败，保留通知文件"
        fi
    fi
else
    echo "无待处理通知"
fi
