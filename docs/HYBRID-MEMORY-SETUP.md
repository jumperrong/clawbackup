# 混合记忆模式配置指南

> 📅 配置时间：2026-03-10 12:52  
> 🎯 模式：本地嵌入（nomic-embed-text）+ MemOS Cloud

---

## 📊 架构设计

### 双层记忆系统

```
┌─────────────────────────────────────────────────┐
│              应用层（OpenClaw）                   │
├─────────────────────────────────────────────────┤
│                                                 │
│  ┌──────────────┐         ┌──────────────┐     │
│  │  本地记忆层   │         │  云端记忆层   │     │
│  │              │         │              │     │
│  │ nomic-embed  │         │  MemOS Cloud │     │
│  │   FAISS 索引  │         │   API 存储    │     │
│  │              │         │              │     │
│  │ ✅ 快速检索   │         │ ✅ 跨设备同步  │     │
│  │ ✅ 隐私性好   │         │ ✅ 备份安全   │     │
│  │ ✅ 免费      │         │ ✅ 自动管理   │     │
│  └──────────────┘         └──────────────┘     │
│         ↓                        ↓              │
│  ~/.openclaw/memory/      https://memos.memtensor.cn
│                                                 │
└─────────────────────────────────────────────────┘
```

---

## 🔧 当前配置

### ✅ 本地记忆层

**模型：** nomic-ai/nomic-embed-text-v1.5

**索引文件：**
- `~/.openclaw/memory/nomic.index` - FAISS 索引（36KB）
- `~/.openclaw/memory/chunks.json` - 12 个文本片段
- `~/.openclaw/memory/meta.json` - 元数据

**脚本：**
- `scripts/nomic-memory-embed.py` - 嵌入生成
- `scripts/nomic-search-memory.py` - 语义搜索

### ✅ 云端记忆层

**服务：** MemOS Cloud

**配置：**
- API Key: `mpg-Weand1FH0aM1vjJWfNBXd8WRL5i7z/Y5E9iPCONl`
- API URL: `https://memos.memtensor.cn`
- 插件：`memos-cloud-openclaw-plugin v0.1.4-beta.0`

---

## 📋 工作流程

### 记忆保存流程

```
1. 对话结束
   ↓
2. OpenClaw 触发 agent_end hook
   ↓
3. MemOS Cloud 插件自动保存对话到云端
   ↓
4. （可选）本地脚本定期同步云端记忆
```

### 记忆检索流程

```
1. 用户查询
   ↓
2. 本地 FAISS 索引快速检索（<100ms）
   ↓
3. （可选）MemOS Cloud 补充检索
   ↓
4. 合并结果，返回最相关的记忆
```

---

## 🔧 使用指南

### 1. 本地记忆操作

**生成/更新索引：**
```bash
python3 ~/openclaw-workspace/scripts/nomic-memory-embed.py
```

**搜索记忆：**
```bash
# 命令行搜索
python3 ~/openclaw-workspace/scripts/nomic-search-memory.py "查询内容"

# 交互式搜索
python3 ~/openclaw-workspace/scripts/nomic-search-memory.py
```

### 2. MemOS Cloud 操作

**自动保存：**
- ✅ 已启用
- 每次对话结束后自动保存到云端

**手动同步：**
```bash
# 从云端拉取记忆
# （需要创建同步脚本）
```

---

## 📊 数据流向

### 写入路径

| 数据类型 | 存储位置 | 触发条件 |
|---------|---------|---------|
| **对话记录** | MemOS Cloud | 自动（每次对话） |
| **MEMORY.md** | 本地文件 | 手动更新 |
| **嵌入索引** | 本地 FAISS | 手动运行脚本 |

### 读取路径

| 查询类型 | 检索源 | 延迟 |
|---------|--------|------|
| **语义搜索** | 本地 FAISS | <100ms |
| **历史对话** | MemOS Cloud | ~500ms |
| **配置文件** | 本地文件 | <10ms |

---

## 🔄 同步策略

### 建议方案

**每日同步：**
```bash
# 添加到 crontab 或 LaunchAgent
0 2 * * * cd ~/openclaw-workspace && python3 scripts/sync-memos-cloud.py
```

**同步内容：**
1. 从 MemOS Cloud 导出新增记忆
2. 合并到 MEMORY.md
3. 重新生成嵌入索引

---

## 📁 文件结构

```
~/.openclaw/
├── .env                              # 环境变量（含 MEMOS_API_KEY）
├── openclaw.json                     # 主配置（含插件配置）
├── extensions/
│   └── memos-cloud-openclaw-plugin/  # MemOS Cloud 插件
├── memory/
│   ├── nomic.index                   # FAISS 索引
│   ├── chunks.json                   # 文本片段
│   ├── meta.json                     # 元数据
│   └── main.sqlite                   # SQLite 存储
└── workspace/
    ├── MEMORY.md                     # 长期记忆文件
    ├── scripts/
    │   ├── nomic-memory-embed.py     # 嵌入生成
    │   ├── nomic-search-memory.py    # 语义搜索
    │   └── sync-memos-cloud.py       # 云端同步（待创建）
    └── docs/
        └── HYBRID-MEMORY-SETUP.md    # 本文档
```

---

## 🎯 优势分析

### 本地记忆层（nomic-embed）

**优势：**
- ✅ 快速检索（<100ms）
- ✅ 完全离线
- ✅ 数据隐私
- ✅ 免费使用

**劣势：**
- ❌ 仅限单设备
- ❌ 需要手动更新索引
- ❌ 无自动备份

### 云端记忆层（MemOS Cloud）

**优势：**
- ✅ 跨设备同步
- ✅ 自动备份
- ✅ 自动管理
- ✅ 无需维护

**劣势：**
- ❌ 依赖网络
- ❌ 延迟较高
- ❌ 隐私顾虑

### 混合模式

**综合优势：**
- ✅ 快速本地检索 + 云端备份
- ✅ 隐私敏感数据本地存储
- ✅ 重要数据云端同步
- ✅ 离线可用 + 在线同步

---

## 🔧 维护指南

### 日常维护

**每周：**
- [ ] 检查本地索引大小
- [ ] 验证 MemOS Cloud 连接
- [ ] 清理过期记忆

**每月：**
- [ ] 备份本地索引
- [ ] 导出云端记忆
- [ ] 优化索引性能

### 故障排查

**问题 1：本地搜索无结果**
```bash
# 检查索引文件
ls -lh ~/.openclaw/memory/

# 重新生成索引
python3 scripts/nomic-memory-embed.py
```

**问题 2：MemOS Cloud 连接失败**
```bash
# 检查 API key
cat ~/.openclaw/.env | grep MEMOS

# 测试连接
curl -H "Authorization: Token $MEMOS_API_KEY" https://memos.memtensor.cn/api/v1/user/me
```

---

## 📝 下一步优化

### 短期（本周）

- [ ] 创建自动同步脚本
- [ ] 添加记忆去重功能
- [ ] 实现增量索引更新

### 中期（本月）

- [ ] 支持多设备同步
- [ ] 添加记忆版本控制
- [ ] 实现记忆关联分析

### 长期（下季度）

- [ ] 支持多模态记忆
- [ ] 实现记忆重要性评分
- [ ] 添加记忆时间衰减

---

## 🔗 相关资源

- **nomic-embed-text**: https://huggingface.co/nomic-ai/nomic-embed-text-v1.5
- **MemOS Cloud**: https://memos.memtensor.cn
- **FAISS**: https://faiss.ai/
- **sentence-transformers**: https://www.sbert.net/

---

_配置文档生成时间：2026-03-10 12:52_  
_配置者：AI 助手_
