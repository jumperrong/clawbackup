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
