#!/bin/bash
# smart-model-router.sh - 智能模型路由
# 根据输入内容自动选择最优模型

INPUT="$*"

# 默认模型
DEFAULT_MODEL="qwen3.5-plus"

# 判断逻辑（按优先级排序）
if echo "$INPUT" | grep -q "封面\|配图\|插图\|图片\|图像\|绘图\|绘画"; then
    MODEL="doubao-seedream-4-5"
    REASON="生图任务"
elif echo "$INPUT" | grep -q "代码\|编程\|python\|js\|javascript\|typescript\|java\|golang\|rust\|函数\|class\|def\|接口\|算法\|调试\|bug\|error"; then
    MODEL="qwen3-coder-next"
    REASON="代码任务"
elif echo "$INPUT" | grep -q "分析\|推理\|复杂\|深入\|详细\|全面\|系统\|专业\|研究\|探讨\|为什么\|原理\|机制"; then
    MODEL="qwen3-max-2026-01-23"
    REASON="复杂推理"
elif echo "$INPUT" | grep -q "长文\|报告\|论文\|书籍\|小说\|剧本\|万字\|完整\|全文"; then
    MODEL="kimi-k2.5"
    REASON="长文本"
elif echo "$INPUT" | grep -q "代理\|任务\|工作流\|自动化\|编排\|多步\|计划"; then
    MODEL="glm-5"
    REASON="Agent 任务"
elif echo "$INPUT" | grep -q "简单\|简短\|概要\|总结\|列表\|翻译\|快速\|快"; then
    MODEL="glm-4.7"
    REASON="快速响应"
else
    MODEL="$DEFAULT_MODEL"
    REASON="通用任务"
fi

# 输出结果
echo "$MODEL"

# 日志记录（可选）
LOG_FILE="/Users/jumpermac/.openclaw/workspace/logs/model-router.log"
if [ -d "$(dirname "$LOG_FILE")" ]; then
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] 输入：${INPUT:0:100}... => 模型：$MODEL ($REASON)" >> "$LOG_FILE"
fi
