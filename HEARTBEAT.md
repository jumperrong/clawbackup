# HEARTBEAT.md

## 自动任务

### 每次 heartbeat 检查时：

1. **检查系统状态**（可选）
   - 确认 OpenClaw 网关运行正常
   - 检查是否有未处理的错误日志

---

## 定时任务（Cron Jobs）

### 已配置的自动更新任务

| 任务 | 频率 | 时间 | 脚本 |
|------|------|------|------|
| **GitHub 自动推送** | 每 6 小时 | - | `auto-github-push.sh` |

### 手动更新所有插件

```bash
# 一次性更新所有插件
bash /Users/jumpermac/.openclaw/workspace/scripts/update-all-plugins.sh
```

### 插件更新策略

**原则：**
- 所有启用的插件都纳入自动更新
- 每周四凌晨统一更新（避开工作时间）
- 更新后自动重启网关
- 失败时记录日志并通知

**日志位置：**
- 统一更新：`logs/all-plugins-update.log`
