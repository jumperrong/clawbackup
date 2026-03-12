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
