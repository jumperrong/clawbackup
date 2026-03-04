#!/bin/bash
# OpenClaw Agent Backup & Restore Script
# 备份/恢复 AI 智能体核心状态文件

set -e

WORKSPACE="${HOME}/.openclaw/workspace"
BACKUP_DIR="${HOME}/.openclaw/backups"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)

# 核心文件列表
CORE_FILES=(
    "IDENTITY.md"
    "SOUL.md"
    "USER.md"
    "MEMORY.md"
    "TOOLS.md"
    "AGENTS.md"
    "BOOTSTRAP.md"
    "HEARTBEAT.md"
)

# 颜色输出
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

print_header() {
    echo -e "${BLUE}========================================${NC}"
    echo -e "${BLUE}  OpenClaw Agent Backup & Restore${NC}"
    echo -e "${BLUE}========================================${NC}"
    echo
}

print_success() {
    echo -e "${GREEN}✓${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}⚠${NC} $1"
}

print_error() {
    echo -e "${RED}✗${NC} $1"
}

# 备份函数
do_backup() {
    print_header
    echo -e "${YELLOW}开始备份...${NC}"
    echo
    
    # 创建备份目录
    mkdir -p "$BACKUP_DIR"
    
    # 备份文件名
    BACKUP_FILE="${BACKUP_DIR}/agent_backup_${TIMESTAMP}.tgz"
    
    # 检查哪些文件存在
    EXISTING_FILES=()
    for file in "${CORE_FILES[@]}"; do
        if [ -f "${WORKSPACE}/${file}" ]; then
            EXISTING_FILES+=("$file")
            print_success "找到：$file"
        fi
    done
    
    # 备份 memory 目录
    if [ -d "${WORKSPACE}/memory" ]; then
        print_success "找到：memory/ 目录"
        EXISTING_FILES+=("memory")
    fi
    
    echo
    echo -e "${YELLOW}打包备份...${NC}"
    
    # 创建压缩包
    cd "$WORKSPACE"
    tar -czf "$BACKUP_FILE" "${EXISTING_FILES[@]}" 2>/dev/null
    
    # 显示备份信息
    BACKUP_SIZE=$(du -h "$BACKUP_FILE" | cut -f1)
    echo
    print_success "备份完成！"
    echo
    echo -e "${BLUE}备份文件:${NC} $BACKUP_FILE"
    echo -e "${BLUE}备份大小:${NC} $BACKUP_SIZE"
    echo -e "${BLUE}备份时间:${NC} $(date '+%Y-%m-%d %H:%M:%S')"
    echo
    
    # 保留最近 10 个备份
    cd "$BACKUP_DIR"
    ls -t agent_backup_*.tgz 2>/dev/null | tail -n +11 | xargs -r rm
    
    print_success "已清理旧备份（保留最近 10 个）"
}

# 恢复函数
do_restore() {
    print_header
    
    if [ -z "$1" ]; then
        # 没有指定备份文件，列出可用备份
        echo -e "${YELLOW}可用的备份:${NC}"
        echo
        if [ -d "$BACKUP_DIR" ]; then
            ls -lht "$BACKUP_DIR"/agent_backup_*.tgz 2>/dev/null | head -10 || echo "  暂无备份文件"
        else
            echo "  备份目录不存在"
        fi
        echo
        echo -e "${YELLOW}使用方法:${NC}"
        echo "  $0 restore <备份文件路径>"
        echo "  $0 restore latest  # 使用最新备份"
        exit 0
    fi
    
    BACKUP_FILE="$1"
    
    # 如果是 latest，找最新备份
    if [ "$BACKUP_FILE" = "latest" ]; then
        BACKUP_FILE=$(ls -t "$BACKUP_DIR"/agent_backup_*.tgz 2>/dev/null | head -1)
        if [ -z "$BACKUP_FILE" ]; then
            print_error "找不到任何备份文件"
            exit 1
        fi
        print_success "使用最新备份：$BACKUP_FILE"
    fi
    
    # 检查备份文件
    if [ ! -f "$BACKUP_FILE" ]; then
        print_error "备份文件不存在：$BACKUP_FILE"
        exit 1
    fi
    
    echo
    echo -e "${YELLOW}准备恢复...${NC}"
    echo "备份文件：$BACKUP_FILE"
    echo "目标目录：$WORKSPACE"
    echo
    
    # 创建恢复前备份
    RESTORE_BACKUP="${BACKUP_DIR}/pre_restore_${TIMESTAMP}.tgz"
    echo -e "${YELLOW}创建恢复前备份...${NC}"
    cd "$WORKSPACE"
    tar -czf "$RESTORE_BACKUP" . 2>/dev/null || true
    print_success "恢复前备份：$RESTORE_BACKUP"
    echo
    
    # 确认恢复
    echo -e "${YELLOW}⚠  警告：这将覆盖现有文件！${NC}"
    read -p "确定要恢复吗？(y/N): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        print_warning "恢复已取消"
        exit 0
    fi
    
    # 执行恢复
    echo
    echo -e "${YELLOW}正在恢复...${NC}"
    tar -xzf "$BACKUP_FILE" -C "$WORKSPACE"
    
    print_success "恢复完成！"
    echo
    echo -e "${BLUE}请重启 OpenClaw 以应用更改${NC}"
}

# 列出备份
list_backups() {
    print_header
    echo -e "${YELLOW}可用的备份:${NC}"
    echo
    
    if [ -d "$BACKUP_DIR" ]; then
        ls -lht "$BACKUP_DIR"/agent_backup_*.tgz 2>/dev/null | head -10 || echo "  暂无备份文件"
    else
        echo "  备份目录不存在"
    fi
}

# 显示帮助
show_help() {
    print_header
    echo "用法：$0 <命令> [选项]"
    echo
    echo "命令:"
    echo "  backup              创建新备份"
    echo "  restore [文件]      恢复备份（不指定文件则列出可用备份）"
    echo "  list                列出所有备份"
    echo "  help                显示帮助"
    echo
    echo "示例:"
    echo "  $0 backup                    # 创建备份"
    echo "  $0 restore                   # 列出可用备份"
    echo "  $0 restore latest            # 恢复最新备份"
    echo "  $0 restore /path/to/file.tgz # 恢复指定备份"
    echo "  $0 list                      # 列出所有备份"
}

# 主程序
case "${1:-backup}" in
    backup)
        do_backup
        ;;
    restore)
        do_restore "$2"
        ;;
    list)
        list_backups
        ;;
    help|--help|-h)
        show_help
        ;;
    *)
        print_error "未知命令：$1"
        show_help
        exit 1
        ;;
esac
