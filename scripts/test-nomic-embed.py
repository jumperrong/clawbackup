#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试 nomic-embed-text 模型
"""

import subprocess
import sys

def install_dependencies():
    """安装依赖"""
    print("📦 正在安装依赖...")
    
    packages = [
        "sentence-transformers",
        "faiss-cpu",
        "numpy",
        "tqdm"
    ]
    
    for package in packages:
        print(f"  安装 {package}...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", package, "-q"])
    
    print("✅ 依赖安装完成\n")

def test_model():
    """测试模型"""
    print("="*60)
    print("🧪 nomic-embed-text 模型测试")
    print("="*60)
    print()
    
    try:
        from sentence_transformers import SentenceTransformer
        import numpy as np
        
        # 加载模型
        print("🤖 加载模型：nomic-ai/nomic-embed-text-v1.5")
        model = SentenceTransformer(
            'nomic-ai/nomic-embed-text-v1.5',
            trust_remote_code=True
        )
        print("✅ 模型加载成功\n")
        
        # 测试文本
        test_texts = [
            "今天天气不错",
            "I love programming",
            "北京是中国的首都",
            "Machine learning is fascinating"
        ]
        
        print("📝 测试文本：")
        for text in test_texts:
            print(f"  - {text}")
        print()
        
        # 生成嵌入
        print("🔧 生成嵌入中...")
        embeddings = model.encode(
            test_texts,
            batch_size=4,
            show_progress_bar=True,
            convert_to_numpy=True
        )
        
        print(f"\n✅ 嵌入生成完成")
        print(f"📊 嵌入形状：{embeddings.shape}")
        print(f"📏 嵌入维度：{embeddings.shape[1]}")
        print()
        
        # 计算相似度
        print("📐 计算相似度...")
        print()
        
        # 中文相似度
        emb1 = embeddings[0]  # 今天天气不错
        emb3 = embeddings[2]  # 北京是中国的首都
        
        from sklearn.metrics.pairwise import cosine_similarity
        sim_cn = cosine_similarity([emb1], [emb3])[0][0]
        
        print(f"中文文本相似度：")
        print(f"  '{test_texts[0]}'")
        print(f"  vs")
        print(f"  '{test_texts[2]}'")
        print(f"  相似度：{sim_cn:.4f}")
        print()
        
        # 英文相似度
        emb2 = embeddings[1]  # I love programming
        emb4 = embeddings[3]  # Machine learning is fascinating
        
        sim_en = cosine_similarity([emb2], [emb4])[0][0]
        
        print(f"英文文本相似度：")
        print(f"  '{test_texts[1]}'")
        print(f"  vs")
        print(f"  '{test_texts[3]}'")
        print(f"  相似度：{sim_en:.4f}")
        print()
        
        # 跨语言相似度
        sim_cross = cosine_similarity([emb2], [emb4])[0][0]
        
        print("🌍 跨语言相似度（英文 vs 中文）：")
        print(f"  '{test_texts[1]}'")
        print(f"  vs")
        print(f"  '{test_texts[0]}'")
        print(f"  相似度：{sim_cross:.4f}")
        print()
        
        print("="*60)
        print("✅ 测试完成！")
        print("="*60)
        
        return True
        
    except Exception as e:
        print(f"\n❌ 测试失败：{e}")
        print("\n请检查：")
        print("  1. 网络连接（首次需要下载模型）")
        print("  2. Python 环境")
        print("  3. 磁盘空间（约 500MB）")
        return False

if __name__ == "__main__":
    print("🚀 开始测试 nomic-embed-text 模型\n")
    
    # 检查依赖
    try:
        import sentence_transformers
        import faiss
        import numpy
    except ImportError:
        print("⚠️  缺少依赖，正在安装...\n")
        install_dependencies()
    
    # 测试模型
    success = test_model()
    
    if success:
        print("\n💡 下一步：")
        print("  1. 运行：python3 scripts/nomic-memory-embed.py")
        print("  2. 生成 MEMORY.md 的嵌入索引")
        print("  3. 运行：python3 scripts/nomic-search-memory.py <查询>")
