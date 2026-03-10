#!/bin/bash
# OpenClaw IP 监控脚本
# 每 5 分钟检查一次公网 IP 变化

echo "=========================================="
echo "🌐 OpenClaw IP 监控"
echo "检查时间：$(date)"
echo "=========================================="

cd /Users/jumpermac/.openclaw/workspace

# 运行 IP 监控脚本
python3 scripts/monitor_ip.py

# 检查是否有通知文件
if [ -f "logs/pending-notify.txt" ]; then
    echo ""
    echo "📬 检测到 IP 变化通知，将通过飞书发送..."
    # heartbeat 会自动处理通知
fi

echo ""
echo "✅ IP 监控完成"
echo ""
