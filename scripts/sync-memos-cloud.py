#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
同步 MemOS Cloud 记忆到本地
"""

import requests
import json
import os
from datetime import datetime

# 配置
MEMOS_API_KEY = os.environ.get('MEMOS_API_KEY', 'mpg-Weand1FH0aM1vjJWfNBXd8WRL5i7z/Y5E9iPCONl')
MEMOS_API_URL = 'https://memos.memtensor.cn'
MEMORY_FILE = '/Users/jumpermac/.openclaw/workspace/MEMORY.md'
BACKUP_DIR = '/Users/jumpermac/.openclaw/workspace/backups/'

def fetch_memos(limit=50):
    """从 MemOS Cloud 获取记忆（优雅降级）"""
    print(f"📡 尝试从 MemOS Cloud 获取记忆...")
    
    headers = {
        'Authorization': f'Token {MEMOS_API_KEY}',
        'Content-Type': 'application/json'
    }
    
    params = {
        'pageSize': limit,
        'pinned': False
    }
    
    try:
        response = requests.get(
            f'{MEMOS_API_URL}/api/v1/memos',
            headers=headers,
            params=params,
            timeout=10  # 缩短超时时间
        )
        
        if response.status_code == 200:
            data = response.json()
            memos = data.get('data', [])
            print(f"✅ 获取到 {len(memos)} 条记忆")
            return memos
        else:
            print(f"⚠️  MemOS Cloud 暂时不可用（{response.status_code}），使用本地记忆")
            return []
            
    except Exception as e:
        print(f"⚠️  MemOS Cloud 连接失败，使用本地记忆：{e}")
        return []

def backup_memory():
    """备份当前 MEMORY.md"""
    if not os.path.exists(MEMORY_FILE):
        print("⚠️  MEMORY.md 不存在，跳过备份")
        return None
    
    os.makedirs(BACKUP_DIR, exist_ok=True)
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    backup_path = os.path.join(BACKUP_DIR, f'MEMORY_{timestamp}.md')
    
    with open(MEMORY_FILE, 'r', encoding='utf-8') as f:
        content = f.read()
    
    with open(backup_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"💾 已备份到：{backup_path}")
    return backup_path

def merge_memos(memos, memory_file):
    """合并 Memos 到 MEMORY.md"""
    print(f"\n📝 合并记忆...")
    
    # 读取现有 MEMORY.md
    if os.path.exists(memory_file):
        with open(memory_file, 'r', encoding='utf-8') as f:
            existing_content = f.read()
    else:
        existing_content = ""
    
    # 添加新的 Memos
    new_section = f"\n\n## 📝 MemOS Cloud 同步记忆\n\n_同步时间：{datetime.now().strftime('%Y-%m-%d %H:%M')}_\n\n"
    
    for memo in memos[:10]:  # 只添加最近 10 条
        content = memo.get('content', '')
        created_ts = memo.get('createdTs', 0)
        created_time = datetime.fromtimestamp(created_ts).strftime('%Y-%m-%d %H:%M')
        
        new_section += f"### {created_time}\n\n{content}\n\n"
    
    # 写入文件
    with open(memory_file, 'w', encoding='utf-8') as f:
        f.write(existing_content + new_section)
    
    print(f"✅ 已添加 {len(memos[:10])} 条记忆到 MEMORY.md")

def update_index():
    """更新本地嵌入索引"""
    print(f"\n🔧 更新本地索引...")
    
    import subprocess
    script_path = '/Users/jumpermac/.openclaw/workspace/scripts/nomic-memory-embed.py'
    
    if os.path.exists(script_path):
        result = subprocess.run(
            ['python3', script_path],
            capture_output=True,
            text=True
        )
        
        if result.returncode == 0:
            print("✅ 索引更新完成")
        else:
            print(f"❌ 索引更新失败：{result.stderr}")
    else:
        print(f"⚠️  脚本不存在：{script_path}")

def main():
    print("="*60)
    print("🔄 MemOS Cloud 记忆同步")
    print("="*60)
    print()
    
    # 1. 备份现有记忆
    backup_memory()
    
    # 2. 获取云端记忆
    memos = fetch_memos(limit=50)
    
    if not memos:
        print("\n⚠️  没有新记忆，跳过同步")
        return
    
    # 3. 合并到 MEMORY.md
    merge_memos(memos, MEMORY_FILE)
    
    # 4. 更新本地索引
    update_index()
    
    print("\n" + "="*60)
    print("✅ 同步完成！")
    print("="*60)

if __name__ == "__main__":
    main()
