# Memos 配置指南

## 📦 什么是 Memos

MemOS 是一个 AI 驱动的笔记和知识管理系统，可以与 OpenClaw 集成，让你的 Agent 能够：
- 保存对话和记忆到 Memos
- 检索历史笔记
- 管理知识库

## 🔑 配置 API Key

### 方式 1：使用 OpenClaw 配置命令

```bash
# 运行配置向导
openclaw configure

# 或者配置特定部分
openclaw configure --section workspace
```

### 方式 2：手动配置环境变量

编辑 `~/.openclaw/config/gateway.env` 或在启动时设置：

```bash
export MEMOS_API_KEY="mpg-Weand1FH0aM1vjJWfNBXd8WRL5i7z/Y5E9iPCONl"
export MEMOS_API_URL="https://memos.memtensor.cn"
```

### 方式 3：添加到 OpenClaw 配置

编辑 `~/.openclaw/config/config.yaml`（如果存在），添加：

```yaml
memos:
  apiKey: "mpg-Weand1FH0aM1vjJWfNBXd8WRL5i7z/Y5E9iPCONl"
  apiUrl: "https://memos.memtensor.cn"
```

## 📝 使用 Memos

配置完成后，你可以让 Agent：

```
帮我把这个保存到 Memos
查找我昨天关于 XXX 的笔记
创建一个关于 XXX 的备忘录
```

## 🔗 相关资源

- **官方文档**: https://memos-docs.openmem.net
- **Web 界面**: https://memos.openmem.net
- **Dashboard**: https://memos-dashboard.openmem.net

## ⚠️ 注意事项

1. **API Key 安全** - 不要将 API key 提交到 Git 仓库
2. **网络访问** - 确保可以访问 `memos.memtensor.cn`
3. **配额限制** - 检查你的账户配额和使用限制

---

*配置时间：2026-03-04*
