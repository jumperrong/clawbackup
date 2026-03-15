# MEMORY.md - 长期记忆

_这是 curated memories， distilled essence，不是 raw logs._

---

## 👤 用户信息

**称呼：** Jumpermac  
**设备：** Mac mini (OpenClaw)  
**时区：** Asia/Shanghai

---

## 🛠️ 技术偏好

### OpenClaw 配置
- **网关管理：** LaunchAgent（非 Terminal 手动启动）
- **模型调用原则：**
  - `qwen3.5-plus` - 通用任务，性能均衡
  - `qwen3-max-2026-01-23` - 复杂任务，最强性能 ✨
  - `qwen3-coder-next` - 代码生成专用
  - `qwen3-coder-plus` - 代码理解增强
  - `glm-5` - 复杂 Agent 任务
  - `glm-4.7` - 快速响应任务
  - `kimi-k2.5` - 长文本和推理

### API 配置
- ✅ **Bailian API Key** - 已配置（通义千问）
- ✅ **豆包 API Key** - 已配置（ed9137d1...，用于生图）
- ✅ **Tavily API Key** - 已配置（tvly-dev-...，用于搜索）
- ⚠️ **微信公众号** - 待配置 AppID/Secret

### 已安装技能
- ✅ **wechat-article-writer** - 微信公众号自动生成（2026-03-09 创建）
  - AI 写文章（Qwen3-Max）
  - AI 生图（豆包 Seedream 4.5）
  - 支持两种封面：头条 900×383，分享 383×383

---

## 📝 重要决策

### 2026-03-09
1. **Bonjour 冲突问题** - 接受现状，不影响核心功能
2. **主机名修改** - jumpermac-openclaw（解决 Bonjour 冲突尝试）
3. **微信公众号技能** - 已搭建并测试通过

### 2026-03-12
1. **飞书配置移除** - 完全清理飞书相关配置，只用钉钉
2. **openclaw-dingtalk 移除** - 卸载废弃的旧钉钉插件，只用 dingtalk-connector

### 2026-03-15 钉钉通道会话路由修复

**问题：** 钉钉消息会话路由不稳定，WebUI 测试后消息被路由到 heartbeat group

**根本原因：** 钉钉连接器 v0.7.8 的设计问题
- 插件使用 `sessionKey: sessionContextJson` 调用 Gateway
- Gateway 根据 `X-OpenClaw-Memory-User` header 创建 `openai-user` 会话
- 这是插件内部路由逻辑，配置无法完全解决

**解决方案：**
1. 配置 `separateSessionByConversation: false` - 按用户维度路由
2. 移除 `sessionTimeout` - 禁用会话超时
3. 移除 `asyncMode` - 使用 AI Card 模式
4. 接受 `openai-user` 会话作为钉钉工作会话
5. 清理空壳 `dingtalk-connector:direct` 会话

**最终配置：**
```json
{
  "channels": {
    "dingtalk-connector": {
      "enabled": true,
      "separateSessionByConversation": false,
      "dmPolicy": "open",
      "allowFrom": ["*"]
    }
  }
}
```

**会话状态（2 个）：**
1. `agent:main:main` - WebChat 主会话（heartbeat、WebUI）
2. `agent:main:openai-user:{...}` - 钉钉工作会话（实际使用）

**功能确认：**
- ✅ 钉钉消息正常接收和回复
- ✅ 会话不会超时重开
- ✅ WebUI 测试不影响钉钉路由

---

## 🎯 项目与兴趣

### 内容创作
- 微信公众号自动化
- 小红书自动化（感兴趣，未实施）

### 技术关注
- OpenClaw 配置和优化
- AI 工具链整合
- 自动化工作流

---

## 📌 待办事项

- [ ] 配置微信公众号 AppID/Secret
- [ ] 探索小红书自动化技能
- [ ] 定期回顾 daily notes，更新 MEMORY.md

---

_最后更新：2026-03-10 09:35_

---

## 📅 2026-03-10 重要更新

### 微信公众号排版系统

1. **封面图优化**（06:45）
   - 重新生成医疗专业风格封面
   - 修复预览页面图片路径问题
   - 新增 3 张康复训练配图

2. **多主题导出功能**（07:16）
   - 创建 `export_wechat.py` 脚本
   - 支持 3 种主题：经典红、医疗绿、科技蓝
   - 样式内联化，确保公众号后台正确显示
   - 创建 `THEMES_GUIDE.md` 使用文档

3. **技术调研**
   - 秀米 API：不开放，需要商务对接
   - 微信公众号 CSS 支持：支持 border-left、background、border-radius 等
   - 不支持：CSS 变量（`:root`/`var()`）、`<style>` 标签

### 记忆机制检查（09:35）

- **问题**：向量化索引未激活（Provider: none）
- **原因**：OpenClaw 不支持 memory 配置
- **解决方案**：使用 MemOS Cloud（已配置）+ 手动维护 MEMORY.md
- **MemOS 配置**：API Key 已设置，插件已安装

---

## 📌 待办事项（更新）

- [x] 配置微信公众号 AppID/Secret（待用户配置）
- [ ] 探索小红书自动化技能
- [x] 定期回顾 daily notes，更新 MEMORY.md（2026-03-10 已更新）
- [ ] 评估 MemOS Cloud 使用效果
