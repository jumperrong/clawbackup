# Exa Web Search 集成指南

通过 MCP (Model Context Protocol) 集成 Exa AI 搜索引擎，提供强大的网页搜索和代码搜索能力。

## 安装配置

### 1. 安装 mcporter

```bash
npm install -g mcporter
```

### 2. 配置 Exa MCP 服务器

```bash
mcporter config add exa https://mcp.exa.ai/mcp
```

配置文件位置：`~/.openclaw/workspace/config/mcporter.json`

配置示例：
```json
{
  "mcpServers": {
    "exa": {
      "baseUrl": "https://mcp.exa.ai/mcp"
    }
  },
  "imports": []
}
```

## 可用工具

### 🔍 exa.web_search_exa - 通用网页搜索

搜索任意主题，获取干净的网页内容。

**参数：**
- `query` (必需) - 搜索关键词
- `numResults` (可选) - 返回结果数量，默认 8
- `livecrawl` (可选) - 实时抓取模式：`fallback` 或 `preferred`
- `type` (可选) - 搜索类型：`auto` 或 `fast`
- `contextMaxCharacters` (可选) - 上下文最大字符数，默认 10000

**使用示例：**
```bash
# 基础搜索
mcporter call exa.web_search_exa query:"OpenClaw 是什么" numResults:5

# 快速搜索
mcporter call exa.web_search_exa query:"最新 AI 新闻" type:"fast"

# 深度搜索（更多结果）
mcporter call exa.web_search_exa query:"React 最佳实践" numResults:10
```

**适合场景：**
- 查找最新信息和新闻
- 研究某个主题
- 获取事实性答案
- 竞品分析

---

### 💻 exa.get_code_context_exa - 代码搜索

搜索代码示例、API 文档、编程解决方案。

**参数：**
- `query` (必需) - 搜索查询（如 "React useState hook 示例"）
- `tokensNum` (可选) - 返回 token 数量，范围 1000-50000，默认 5000

**使用示例：**
```bash
# 查找 API 用法
mcporter call exa.get_code_context_exa query:"Express.js middleware 示例"

# 查找代码示例
mcporter call exa.get_code_context_exa query:"Python pandas dataframe 过滤" tokensNum:10000

# 查找库文档
mcporter call exa.get_code_context_exa query:"Next.js partial prerendering 配置"
```

**搜索源：**
- GitHub
- Stack Overflow
- 官方文档

**适合场景：**
- API 用法查询
- 代码示例查找
- 调试帮助
- 技术选型调研

---

## 在 OpenClaw 中使用

配置完成后，可以直接让助手使用 Exa 搜索：

```
"帮我搜索一下 OpenClaw 的最新功能"
"找一下 React 19 的更新内容"
"搜索 Python 异步编程最佳实践"
```

## 查看可用工具

```bash
# 列出所有配置的服务
mcporter list

# 查看 Exa 工具详情
mcporter list exa --schema
```

## 注意事项

1. **API 限制** - Exa 有免费额度，超出后需要付费
2. **网络要求** - 需要能访问 https://mcp.exa.ai/mcp
3. **结果验证** - 搜索结果来自外部来源，请验证关键信息

## 相关链接

- Exa 官网：https://exa.ai/
- Exa 文档：https://docs.exa.ai/
- MCP 官网：https://modelcontextprotocol.io/
- mcporter GitHub: https://github.com/mcporter/mcporter
