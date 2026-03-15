# HEARTBEAT.md

## 自动任务

### 每次 heartbeat 检查时：

1. **检查系统版本** ⭐ 新增
   - 检查是否有新版本可用
   - 如有更新，**通过钉钉通知用户**
   - **不自主更新**，等待用户确认

2. **检查 pending 通知** ⭐ 新增
   - 读取 `pending-notify.txt` 文件（如有）
   - **通过钉钉发送 pending 通知给用户**（使用 openclaw message 工具或钉钉 connector）
   - 发送后清空该文件

**pending-notify.txt 格式：**
```
✅ GitHub 推送成功 - 提交已推送到 github.com:jumperrong/clawbackup.git
❌ GitHub 推送失败 - 请检查网络或权限
```

3. **检查系统状态**（可选）
   - 确认 OpenClaw 网关运行正常
   - 检查是否有未处理的错误日志
   - **检查结果通过钉钉通知用户**（如有异常）

---

## 定时任务（Cron Jobs）

### 已配置的自动更新任务

| 任务 | 频率 | 时间 | 脚本 | 通知方式 |
|------|------|------|------|----------|
| **GitHub 自动推送** | 每 6 小时 | - | `auto-github-push.sh` | **钉钉**（写入 pending-notify.txt，heartbeat 发送） |

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
