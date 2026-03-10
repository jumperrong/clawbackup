#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
使用 nomic-embed-text 模型生成记忆嵌入
"""

from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
import json
import os
from datetime import datetime

MODEL_NAME = 'nomic-ai/nomic-embed-text-v1.5'
MEMORY_FILE = '/Users/jumpermac/.openclaw/workspace/MEMORY.md'
OUTPUT_DIR = '/Users/jumpermac/.openclaw/memory/'

def load_model():
    """加载嵌入模型"""
    print(f"🤖 加载模型：{MODEL_NAME}")
    model = SentenceTransformer(MODEL_NAME, trust_remote_code=True)
    print(f"✅ 模型加载完成")
    return model

def embed_memory_file(model, filepath):
    """嵌入整个记忆文件"""
    print(f"\n📖 读取文件：{filepath}")
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 分段（按段落）
    chunks = []
    for p in content.split('\n\n'):
        p = p.strip()
        if len(p) > 50 and len(p) < 4000:  # 过滤太短和太长的段落
            chunks.append(p)
    
    print(f"📦 分割为 {len(chunks)} 个片段")
    
    # 批量生成嵌入
    print("\n🔧 生成嵌入中...")
    embeddings = model.encode(
        chunks,
        batch_size=32,
        show_progress_bar=True,
        convert_to_numpy=True
    )
    
    print(f"\n✅ 嵌入完成")
    print(f"📊 嵌入形状：{embeddings.shape}")
    
    return chunks, embeddings

def save_index(chunks, embeddings, output_dir):
    """保存 FAISS 索引"""
    os.makedirs(output_dir, exist_ok=True)
    
    # 转换为 float32
    embeddings_fp32 = embeddings.astype('float32')
    
    # 创建索引
    dimension = embeddings_fp32.shape[1]
    index = faiss.IndexFlatL2(dimension)
    index.add(embeddings_fp32)
    
    # 保存索引
    index_path = os.path.join(output_dir, 'nomic.index')
    faiss.write_index(index, index_path)
    print(f"\n💾 索引已保存：{index_path}")
    
    # 保存文本片段
    chunks_path = os.path.join(output_dir, 'chunks.json')
    with open(chunks_path, 'w', encoding='utf-8') as f:
        json.dump(chunks, f, ensure_ascii=False, indent=2)
    print(f"💾 片段已保存：{chunks_path}")
    
    # 保存元数据
    meta = {
        'model': MODEL_NAME,
        'dimension': int(dimension),
        'chunks_count': len(chunks),
        'created_at': str(datetime.now()),
        'memory_file': MEMORY_FILE
    }
    meta_path = os.path.join(output_dir, 'meta.json')
    with open(meta_path, 'w', encoding='utf-8') as f:
        json.dump(meta, f, indent=2, ensure_ascii=False)
    print(f"💾 元数据已保存：{meta_path}")
    
    # 打印统计
    print(f"\n📊 统计信息：")
    print(f"   片段数：{len(chunks)}")
    print(f"   嵌入维度：{dimension}")
    print(f"   索引大小：{os.path.getsize(index_path) / 1024:.1f} KB")

if __name__ == "__main__":
    print("="*60)
    print("🧠 生成记忆嵌入 (nomic-embed-text)")
    print("="*60)
    
    # 加载模型
    model = load_model()
    
    # 嵌入 MEMORY.md
    chunks, embeddings = embed_memory_file(model, MEMORY_FILE)
    
    # 保存索引
    save_index(chunks, embeddings, OUTPUT_DIR)
    
    print("\n✅ 所有任务完成！")
    print("\n💡 下一步：")
    print("  运行：python3 scripts/nomic-search-memory.py <查询>")
