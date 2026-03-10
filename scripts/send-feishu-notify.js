#!/usr/bin/env node
// 发送 OpenClaw 更新通知到飞书

const message = process.argv.slice(2).join(' ');

if (!message) {
    console.error('请提供消息内容');
    process.exit(1);
}

// 通过 openclaw message 发送
const { execSync } = require('child_process');

try {
    // 使用 feishu-doc skill 的方式发送消息
    // 由于无法直接调用 tool，我们使用一个变通方法：
    // 创建一个临时文件，包含要发送的消息
    const fs = require('fs');
    const path = require('path');
    
    const notifyPath = path.join(process.env.HOME, '.openclaw/workspace/logs/last-update-notify.txt');
    fs.writeFileSync(notifyPath, message);
    
    console.log('通知已记录到：' + notifyPath);
    console.log('消息内容：' + message);
    
    // 尝试通过 openclaw 发送（需要会话上下文）
    console.log('\n提示：由于脚本运行在独立环境中，无法直接发送飞书消息。');
    console.log('建议在 OpenClaw 主会话中配置 webhook 或使用其他方式通知。');
    
} catch (error) {
    console.error('发送失败:', error.message);
    process.exit(1);
}
