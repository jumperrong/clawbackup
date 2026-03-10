#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
使用 nomic-embed-text 模型搜索记忆
"""

from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
import json
import os
import sys

MODEL_NAME = 'nomic-ai/nomic-embed-text-v1.5'
INDEX_DIR = '/Users/jumpermac/.openclaw/memory/'

def load_model():
    """加载模型"""
    print(f"🤖 加载模型：{MODEL_NAME}")
    model = SentenceTransformer(MODEL_NAME, trust_remote_code=True)
    return model

def load_index(index_dir):
    """加载索引和片段"""
    index_path = os.path.join(index_dir, 'nomic.index')
    chunks_path = os.path.join(index_dir, 'chunks.json')
    meta_path = os.path.join(index_dir, 'meta.json')
    
    if not os.path.exists(index_path):
        print(f"❌ 索引文件不存在：{index_path}")
        print("   请先运行：python3 scripts/nomic-memory-embed.py")
        sys.exit(1)
    
    index = faiss.read_index(index_path)
    
    with open(chunks_path, 'r', encoding='utf-8') as f:
        chunks = json.load(f)
    
    meta = {}
    if os.path.exists(meta_path):
        with open(meta_path, 'r', encoding='utf-8') as f:
            meta = json.load(f)
    
    return index, chunks, meta

def search(query, model, index, chunks, top_k=5):
    """搜索记忆"""
    # 生成查询嵌入
    query_embedding = model.encode([query])
    query_fp32 = query_embedding.astype('float32')
    
    # 搜索
    distances, indices = index.search(query_fp32, top_k)
    
    # 显示结果
    print(f"\n🔍 搜索：{query}")
    print("="*60)
    
    found = False
    for i, (dist, idx) in enumerate(zip(distances[0], indices[0])):
        if idx >= 0 and idx < len(chunks):
            found = True
            # 余弦距离转换为相似度
            similarity = 1 - dist
            
            print(f"\n{i+1}. 相似度：{similarity:.4f}")
            print(f"   内容：{chunks[idx][:300]}...")
    
    if not found:
        print("\n⚠️  未找到相关结果")
    
    return distances, indices

def interactive_search(model, index, chunks, meta):
    """交互式搜索"""
    print("\n" + "="*60)
    print("🔍 交互式记忆搜索")
    print("="*60)
    
    if meta:
        print(f"\n📊 索引信息：")
        print(f"   模型：{meta.get('model', 'Unknown')}")
        print(f"   片段数：{meta.get('chunks_count', 0)}")
        print(f"   创建时间：{meta.get('created_at', 'Unknown')}")
    
    print("\n💡 输入查询内容，按 Enter 搜索")
    print("   输入 'quit' 或 'q' 退出\n")
    
    while True:
        try:
            query = input("🔍 查询：").strip()
            
            if query.lower() in ['quit', 'q', 'exit']:
                print("\n👋 再见！")
                break
            
            if not query:
                continue
            
            search(query, model, index, chunks, top_k=5)
            print()
            
        except KeyboardInterrupt:
            print("\n\n👋 再见！")
            break
        except Exception as e:
            print(f"\n❌ 错误：{e}")

if __name__ == "__main__":
    print("="*60)
    print("🧠 记忆搜索 (nomic-embed-text)")
    print("="*60)
    
    # 加载
    model = load_model()
    index, chunks, meta = load_index(INDEX_DIR)
    
    # 如果有命令行参数，执行单次搜索
    if len(sys.argv) > 1:
        query = ' '.join(sys.argv[1:])
        search(query, model, index, chunks, top_k=5)
    else:
        # 否则进入交互式搜索
        interactive_search(model, index, chunks, meta)
