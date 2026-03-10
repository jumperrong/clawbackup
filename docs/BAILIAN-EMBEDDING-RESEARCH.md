# 百炼嵌入模型可行性研究报告

> 📅 研究时间：2026-03-10 11:17  
> 🎯 目标：评估使用阿里云百炼（Bailian）text-embedding 模型实现记忆向量化的可行性

---

## 📊 研究结论

### ✅ 可行性评估

| 维度 | 评分 | 说明 |
|------|------|------|
| **技术可行性** | ⭐⭐⭐⭐ | API 存在，支持中文嵌入 |
| **成本** | ⭐⭐⭐⭐ | 约 ¥0.0007/千 tokens，成本低 |
| **实施难度** | ⭐⭐⭐ | 需要解决 API key 认证问题 |
| **性能** | ⭐⭐⭐⭐⭐ | 阿里云基础设施，速度快 |
| **隐私性** | ⭐⭐⭐ | 数据需发送到云端 |

**总体评价：** ✅ **推荐实施**（需先解决 API key 问题）

---

## 🔍 API 信息

### 官方文档

- **API 名称：** text-embedding-v2 / text-embedding-v3
- **服务提供商：** 阿里云百炼（DashScope）
- **文档链接：** https://help.aliyun.com/zh/dashscope/developer-reference/text-embedding-api-details

### 模型规格

| 模型 | 维度 | 最大输入 | 语言支持 |
|------|------|---------|---------|
| **text-embedding-v2** | 1536 | 2048 tokens | 中英文 |
| **text-embedding-v3** | 2048 | 8192 tokens | 多语言 |

### 价格（参考）

| 模型 | 单价 | 免费额度 |
|------|------|---------|
| **text-embedding-v2** | ¥0.0007/千 tokens | 新用户赠送 |
| **text-embedding-v3** | ¥0.002/千 tokens | 新用户赠送 |

**估算成本：**
- MEMORY.md（约 3000 字）→ 约 ¥0.02/次
- 每月更新 4 次 → 约 ¥0.08/月

---

## 🔧 实施步骤

### 步骤 1：确认 API Key

**当前状态：** ❌ API key 认证失败（401 InvalidApiKey）

**可能原因：**
1. API key 格式不正确
2. API key 已过期或被禁用
3. 需要开通嵌入模型服务

**解决方案：**

```bash
# 1. 登录阿里云百炼控制台
open https://bailian.console.aliyun.com/?tab=model#/api-key

# 2. 创建新的 API Key
# - 选择"中国内地（北京）"地域
# - 确保开通"文本嵌入"服务

# 3. 更新配置
nano ~/.openclaw/openclaw.json
# 或
nano ~/.openclaw/.env
```

### 步骤 2：创建嵌入脚本

**文件：** `scripts/bailian-memory-embed.py`

```python
#!/usr/bin/env python3
import requests
import json
import numpy as np
import faiss

API_KEY = "YOUR_NEW_API_KEY"
BASE_URL = "https://dashscope.aliyuncs.com/api/v1/services/embeddings/text-embedding/text-embedding"

def embed_text(text):
    """生成文本嵌入"""
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "model": "text-embedding-v2",
        "input": {"texts": [text]},
        "parameters": {"text_type": "query"}
    }
    
    response = requests.post(BASE_URL, headers=headers, json=payload)
    
    if response.status_code == 200:
        data = response.json()
        return data['output']['embeddings'][0]['embedding']
    else:
        print(f"错误：{response.text}")
        return None

def embed_memory_file(filepath):
    """嵌入整个记忆文件"""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 分段（按段落）
    chunks = [p.strip() for p in content.split('\n\n') if len(p.strip()) > 50]
    
    embeddings = []
    for chunk in chunks:
        emb = embed_text(chunk)
        if emb:
            embeddings.append(emb)
            print(f"✅ 已嵌入：{chunk[:30]}...")
    
    return chunks, embeddings

def save_index(chunks, embeddings, output_dir):
    """保存 FAISS 索引"""
    import faiss
    
    # 转换为 numpy 数组
    embeddings_np = np.array(embeddings).astype('float32')
    
    # 创建索引
    dimension = embeddings_np.shape[1]
    index = faiss.IndexFlatL2(dimension)
    index.add(embeddings_np)
    
    # 保存
    faiss.write_index(index, f'{output_dir}/bailian.index')
    
    with open(f'{output_dir}/chunks.json', 'w', encoding='utf-8') as f:
        json.dump(chunks, f, ensure_ascii=False, indent=2)
    
    print(f"✅ 索引已保存：{len(chunks)} 个片段")

if __name__ == "__main__":
    chunks, embeddings = embed_memory_file('/Users/jumpermac/.openclaw/workspace/MEMORY.md')
    save_index(chunks, embeddings, '/Users/jumpermac/.openclaw/memory/')
```

### 步骤 3：创建搜索脚本

**文件：** `scripts/search-memory.py`

```python
#!/usr/bin/env python3
import faiss
import numpy as np
import json

def search_memory(query, top_k=5):
    """搜索记忆"""
    # 加载索引
    index = faiss.read_index('/Users/jumpermac/.openclaw/memory/bailian.index')
    
    with open('/Users/jumpermac/.openclaw/memory/chunks.json', 'r', encoding='utf-8') as f:
        chunks = json.load(f)
    
    # 生成查询嵌入（需要调用百炼 API）
    query_embedding = embed_text(query)  # 使用上面的 embed_text 函数
    
    if query_embedding:
        query_np = np.array([query_embedding]).astype('float32')
        
        # 搜索
        distances, indices = index.search(query_np, top_k)
        
        # 显示结果
        print(f"🔍 搜索结果：{query}")
        print("="*60)
        for i, (dist, idx) in enumerate(zip(distances[0], indices[0])):
            if idx < len(chunks):
                print(f"{i+1}. 相似度：{1-dist:.4f}")
                print(f"   内容：{chunks[idx][:100]}...")
                print()

if __name__ == "__main__":
    import sys
    query = sys.argv[1] if len(sys.argv) > 1 else "测试"
    search_memory(query)
```

### 步骤 4：集成到 Heartbeat

**文件：** `HEARTBEAT.md`

```markdown
## 自动任务

### 每次 heartbeat 检查时：

1. **检查记忆更新**
   - 如果 MEMORY.md 有变化，重新生成嵌入
   - 运行：`python3 scripts/bailian-memory-embed.py`

2. **检查待发送通知**
   ...
```

---

## 📋 完整实施清单

### 准备工作

- [ ] 登录阿里云百炼控制台
- [ ] 创建新的 API Key（北京地域）
- [ ] 确认开通 text-embedding 服务
- [ ] 测试 API 连接

### 安装依赖

```bash
# 安装 Python 库
pip3 install requests faiss-cpu numpy
```

### 创建脚本

- [ ] `scripts/bailian-memory-embed.py` - 嵌入生成
- [ ] `scripts/search-memory.py` - 语义搜索
- [ ] `scripts/test-bailian-embedding.py` - API 测试

### 配置集成

- [ ] 更新 `~/.openclaw/.env` 添加新 API key
- [ ] 更新 `HEARTBEAT.md` 添加自动索引
- [ ] 创建命令行搜索工具

### 测试验证

- [ ] 测试单个文本嵌入
- [ ] 测试 MEMORY.md 全量嵌入
- [ ] 测试语义搜索
- [ ] 测试增量更新

---

## 🎯 推荐方案

### 方案对比

| 方案 | 成本 | 实施难度 | 效果 | 推荐度 |
|------|------|---------|------|--------|
| **百炼嵌入** | ¥0.08/月 | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ |
| **本地嵌入** | 免费 | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| **MemOS Cloud** | 未知 | ⭐⭐ | ❌ 不可用 | ❌ |

### 最终建议

**推荐方案：本地嵌入（sentence-transformers）**

**理由：**
1. ✅ 一次性投入，永久免费
2. ✅ 数据隐私性好
3. ✅ 不依赖外部 API
4. ✅ 效果接近百炼

**百炼嵌入作为备选：**
- 如果本地嵌入效果不理想
- 如果需要更强的中文语义理解
- 如果愿意承担少量费用

---

## 🔗 相关资源

- **百炼控制台**: https://bailian.console.aliyun.com/
- **API 文档**: https://help.aliyun.com/zh/dashscope/developer-reference/text-embedding-api-details
- **SDK 文档**: https://help.aliyun.com/zh/dashscope/developer-reference/python-sdk-reference
- **定价详情**: https://help.aliyun.com/zh/dashscope/pricing

---

_研究报告生成时间：2026-03-10 11:17_  
_研究者：AI 助手_
