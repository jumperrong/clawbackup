#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试百炼嵌入 API
文档：https://help.aliyun.com/zh/dashscope/developer-reference/text-embedding-api-details
"""

import requests
import json
import os

# 配置
API_KEY = "sk-sp-10f48e26ce354c59b083cbe9d711d5af"
BASE_URL = "https://dashscope.aliyuncs.com/api/v1/services/embeddings/text-embedding/text-embedding"

def test_embedding():
    """测试嵌入 API"""
    
    # 测试文本
    texts = [
        "今天天气不错",
        "我喜欢编程",
        "北京是中国的首都"
    ]
    
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "model": "text-embedding-v2",
        "input": {
            "texts": texts
        },
        "parameters": {
            "text_type": "query"
        }
    }
    
    print("🔍 测试百炼嵌入 API...")
    print(f"📝 文本：{texts}")
    print()
    
    try:
        response = requests.post(BASE_URL, headers=headers, json=payload, timeout=30)
        
        print(f"📊 状态码：{response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print("✅ 调用成功！")
            print()
            
            # 解析结果
            output = data.get('output', {})
            embeddings = output.get('embeddings', [])
            
            print(f"📦 返回 {len(embeddings)} 个嵌入")
            print()
            
            for i, emb in enumerate(embeddings):
                text = emb.get('text', texts[i])
                embedding = emb.get('embedding', [])
                print(f"{i+1}. 文本：{text}")
                print(f"   维度：{len(embedding)}")
                print(f"   前 5 个值：{embedding[:5]}")
                print()
            
            # 使用统计
            usage = data.get('usage', {})
            print(f"📊 使用统计：")
            print(f"   总 token 数：{usage.get('total_tokens', 0)}")
            
            return True
            
        else:
            print("❌ 调用失败")
            print(f"错误信息：{response.text}")
            return False
            
    except Exception as e:
        print(f"❌ 异常：{e}")
        return False


def calculate_similarity():
    """测试相似度计算"""
    print("\n" + "="*60)
    print("📐 测试相似度计算")
    print("="*60)
    
    # 先获取两个文本的嵌入
    texts = ["我喜欢编程", "编程是我的爱好"]
    
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "model": "text-embedding-v2",
        "input": {"texts": texts}
    }
    
    response = requests.post(BASE_URL, headers=headers, json=payload, timeout=30)
    
    if response.status_code == 200:
        data = response.json()
        embeddings = data['output']['embeddings']
        
        import numpy as np
        emb1 = np.array(embeddings[0]['embedding'])
        emb2 = np.array(embeddings[1]['embedding'])
        
        # 计算余弦相似度
        similarity = np.dot(emb1, emb2) / (np.linalg.norm(emb1) * np.linalg.norm(emb2))
        
        print(f"文本 1: {texts[0]}")
        print(f"文本 2: {texts[1]}")
        print(f"余弦相似度：{similarity:.4f} (越接近 1 越相似)")
        
    else:
        print(f"获取嵌入失败：{response.text}")


if __name__ == "__main__":
    print("="*60)
    print("🧪 百炼嵌入 API 测试")
    print("="*60)
    print()
    
    success = test_embedding()
    
    if success:
        calculate_similarity()
        print("\n✅ 测试完成！")
    else:
        print("\n❌ 测试失败，请检查 API key 和网络连接")
