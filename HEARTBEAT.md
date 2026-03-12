# HEARTBEAT.md

## 自动任务

### 每次 heartbeat 检查时：

1. **检查待发送通知**：如果 `workspace/logs/pending-notify.txt` 存在
   - 读取文件内容
   - 通过飞书发送给用户
   - 删除该文件

2. **检查系统状态**（可选）
   - 确认 OpenClaw 网关运行正常
   - 检查是否有未处理的错误日志

3. **检查更新**（每 3-4 次 heartbeat 执行一次）
   - 运行 `openclaw status` 检查是否有可用更新
   - 如果有更新，将更新信息写入 `logs/pending-notify.txt`
   - 下次 heartbeat 时会自动通过飞书发送通知

---

## 定时任务（Cron Jobs）

### 已配置的自动更新任务

| 任务 | 频率 | 时间 | 脚本 |
|------|------|------|------|
| **飞书插件更新** | 每周 | 周四 03:00 | `update-feishu-plugin.sh` |
| **Memos Cloud 插件更新** | 每周 | 周四 03:00 | `update-memos-plugin.sh` |
| **OpenClaw 核心更新** | 每天 | 02:00 | `daily-update-check.sh` |
| **GitHub 自动推送** | 每 6 小时 | - | `auto-github-push.sh` |

### 手动更新所有插件

```bash
# 一次性更新所有插件
bash /Users/jumpermac/.openclaw/workspace/scripts/update-all-plugins.sh

# 单独更新某个插件
bash /Users/jumpermac/.openclaw/workspace/scripts/update-feishu-plugin.sh
bash /Users/jumpermac/.openclaw/workspace/scripts/update-memos-plugin.sh
```

### 插件更新策略

**原则：**
- 所有启用的插件都纳入自动更新
- 每周四凌晨统一更新（避开工作时间）
- 更新后自动重启网关
- 失败时记录日志并通知

**日志位置：**
- 飞书插件：`logs/feishu-plugin-update.log`
- Memos Cloud：`logs/memos-plugin-update.log`
- 统一更新：`logs/all-plugins-update.log`
