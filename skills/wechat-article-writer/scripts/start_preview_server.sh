#!/bin/bash
# start_preview_server.sh - 启动预览服务器（后台运行）

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
OUTPUT_DIR="$SCRIPT_DIR/output"
PID_FILE="$SCRIPT_DIR/.preview_server.pid"
LOG_FILE="$SCRIPT_DIR/.preview_server.log"

# 检查是否已经在运行
if [ -f "$PID_FILE" ]; then
    OLD_PID=$(cat "$PID_FILE")
    if ps -p $OLD_PID > /dev/null 2>&1; then
        echo "⚠️  预览服务器已在运行 (PID: $OLD_PID)"
        echo "📍 访问地址：http://localhost:8080/preview.html"
        echo ""
        echo "停止服务器：bash $SCRIPT_DIR/stop_preview_server.sh"
        exit 0
    else
        echo "🧹 清理过期的 PID 文件"
        rm -f "$PID_FILE"
    fi
fi

# 启动服务器
echo "🚀 启动预览服务器..."
cd "$OUTPUT_DIR"
nohup python3 -m http.server 8080 > "$LOG_FILE" 2>&1 &
NEW_PID=$!

# 保存 PID
echo $NEW_PID > "$PID_FILE"

# 等待服务器启动
sleep 2

# 检查是否启动成功
if ps -p $NEW_PID > /dev/null 2>&1; then
    echo "✅ 预览服务器启动成功！"
    echo ""
    echo "📍 访问地址：http://localhost:8080/preview.html"
    echo "📊 进程 PID: $NEW_PID"
    echo "📄 日志文件：$LOG_FILE"
    echo ""
    echo "停止服务器：bash $SCRIPT_DIR/stop_preview_server.sh"
    echo "查看日志：tail -f $LOG_FILE"
else
    echo "❌ 服务器启动失败，请检查日志：$LOG_FILE"
    rm -f "$PID_FILE"
    exit 1
fi
