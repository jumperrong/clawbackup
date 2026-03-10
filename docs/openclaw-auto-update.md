# OpenClaw 自动更新通知系统

## 配置概览

### 1. 更新检查脚本
**位置**: `/Users/jumpermac/.openclaw/workspace/scripts/daily-update-check.sh`

**功能**:
- 检查当前安装的 OpenClaw 版本
- 对比 npm 上的最新版本
- 如有更新，自动执行 `npm install -g openclaw@latest`
- 将更新结果写入通知文件

**执行时间**: 每天早上 9:00（通过 launchd）

### 2. 通知文件
**位置**: `/Users/jumpermac/.openclaw/workspace/logs/pending-notify.txt`

**内容格式**:
```
🎉 OpenClaw 更新完成！

已从 `2026.3.1` 更新到 `2026.3.2`
更新时间：2026-03-05 13:21:00
```

或（更新失败时）:
```
⚠️ OpenClaw 更新失败

当前版本：2026.3.1
目标版本：2026.3.2
错误信息：[错误详情]
更新时间：2026-03-05 13:21:00
```

### 3. 通知发送机制
**触发方式**: Heartbeat 检查

**流程**:
1. Heartbeat 检查 `pending-notify.txt` 是否存在
2. 如果存在，读取文件内容
3. 通过飞书发送通知给用户
4. 删除通知文件

### 4. 定时任务配置
**Launchd Plist**: `/Users/jumpermac/.openclaw/workspace/com.openclaw.daily-update-check.plist`

**执行时间**: 每天 09:00

**日志文件**: `/Users/jumpermac/.openclaw/workspace/logs/daily-update.log`

## 手动操作

### 手动检查更新
```bash
/Users/jumpermac/.openclaw/workspace/scripts/daily-update-check.sh
```

### 查看更新日志
```bash
tail -f /Users/jumpermac/.openclaw/workspace/logs/daily-update.log
```

### 查看当前版本
```bash
npm list -g openclaw
```

### 手动更新
```bash
npm install -g openclaw@latest
```

## 通知示例

### 成功更新
```
🎉 OpenClaw 更新完成！

已从 `2026.3.1` 更新到 `2026.3.2`
更新时间：2026-03-05 13:21:00
```

### 无需更新
```
（无通知，静默跳过）
```

### 更新失败
```
⚠️ OpenClaw 更新失败

当前版本：2026.3.1
目标版本：2026.3.2
错误信息：[详细错误]
更新时间：2026-03-05 13:21:00
```

## 配置验证

### 检查 launchd 任务状态
```bash
launchctl list | grep openclaw
```

### 测试脚本
```bash
/Users/jumpermac/.openclaw/workspace/scripts/daily-update-check.sh
```

### 测试通知发送
```bash
# 创建测试通知文件
echo "🎉 测试通知" > /Users/jumpermac/.openclaw/workspace/logs/pending-notify.txt

# 然后在 heartbeat 中会自动发送
```

## 注意事项

1. **飞书通知依赖 heartbeat 机制**：更新脚本本身不直接发送飞书消息，而是写入通知文件，由 heartbeat 检查并发送

2. **heartbeat 频率**：建议配置为每天检查 2-4 次，确保及时发送更新通知

3. **日志轮转**：定期清理 `daily-update.log` 避免文件过大

4. **权限问题**：确保脚本有执行权限：
   ```bash
   chmod +x /Users/jumpermac/.openclaw/workspace/scripts/*.sh
   ```

## 故障排查

### 问题：没有收到更新通知
**检查步骤**:
1. 确认 launchd 任务已加载：`launchctl list | grep openclaw`
2. 检查日志文件：`tail /Users/jumpermac/.openclaw/workspace/logs/daily-update.log`
3. 手动运行脚本测试
4. 检查是否有 `pending-notify.txt` 文件

### 问题：更新失败
**可能原因**:
- 网络连接问题
- npm 仓库访问问题
- 权限不足

**解决方案**:
1. 检查网络连接
2. 手动执行 `npm install -g openclaw@latest`
3. 查看详细错误日志

---

**最后更新**: 2026-03-05
**配置者**: 小爪 🦞
