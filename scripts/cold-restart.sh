#!/bin/bash

# OpenClaw 冷启动脚本
# 流程：停止 → 等待 30 秒 → 安装 → 启动

set -e

echo "🦞 OpenClaw 冷启动脚本"
echo "========================"

# 1. 停止网关
echo "📴 步骤 1/4: 停止网关..."
openclaw gateway stop 2>&1 || echo "⚠️  网关可能未运行"

# 2. 等待 30 秒
echo "⏳ 步骤 2/4: 等待 30 秒（让进程完全退出）..."
for i in {30..1}; do
    printf "\r   剩余 %2d 秒..." $i
    sleep 1
done
echo " ✅"

# 3. 重新安装（确保最新）
echo "📦 步骤 3/4: 执行 gateway install..."
openclaw gateway install

# 4. 启动网关
echo "🚀 步骤 4/4: 启动网关..."
openclaw gateway start

# 5. 检查状态
echo ""
echo "✅ 冷启动完成！检查状态："
echo "========================"
openclaw gateway status

echo ""
echo "📋 提示："
echo "   - 查看日志：openclaw logs --follow"
echo "   - 查看进程：ps aux | grep openclaw"
