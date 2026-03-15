#!/bin/bash
# stop_preview_server.sh - 停止预览服务器

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PID_FILE="$SCRIPT_DIR/.preview_server.pid"

if [ ! -f "$PID_FILE" ]; then
    echo "ℹ️  预览服务器未运行"
    exit 0
fi

PID=$(cat "$PID_FILE")

if ps -p $PID > /dev/null 2>&1; then
    echo "🛑 停止预览服务器 (PID: $PID)..."
    kill $PID
    sleep 1
    
    if ps -p $PID > /dev/null 2>&1; then
        echo "⚠️  强制终止进程..."
        kill -9 $PID
    fi
    
    rm -f "$PID_FILE"
    echo "✅ 服务器已停止"
else
    echo "ℹ️  进程不存在，清理 PID 文件"
    rm -f "$PID_FILE"
fi
