# 公网 IP 监控配置指南

> 📅 创建时间：2026-03-10 14:27  
> 🎯 用途：监控公网 IP 变化，自动通知更新微信公众号 IP 白名单

---

## 📊 系统架构

### 工作流程

```
1. 每 5 分钟检查一次
   ↓
2. 获取当前公网 IP
   ↓
3. 对比上次记录的 IP
   ↓
4. 如果变化 → 发送飞书通知
   ↓
5. 更新 IP 记录文件
```

### 核心组件

| 组件 | 用途 | 位置 |
|------|------|------|
| **monitor_ip.py** | IP 监控主脚本 | `scripts/monitor_ip.py` |
| **ip-monitor-check.sh** | Shell 包装脚本 | `scripts/ip-monitor-check.sh` |
| **com.openclaw.ip-monitor.plist** | LaunchAgent 配置 | `~/Library/LaunchAgents/` |
| **last_ip.txt** | IP 记录文件 | `logs/last_ip.txt` |
| **pending-notify.txt** | 通知文件 | `logs/pending-notify.txt` |

---

## 🔧 使用说明

### 手动检查

```bash
# 运行 IP 监控脚本
python3 ~/openclaw-workspace/scripts/monitor_ip.py
```

**输出示例：**
```
============================================================
🌐 公网 IP 监控
============================================================

✅ 从 https://icanhazip.com 获取 IP: 123.253.224.104
📊 上次记录 IP: 180.113.194.180
📊 当前公网 IP: 123.253.224.104

⚠️  IP 发生变化！

📬 通知已写入：.../logs/pending-notify.txt

🌐 公网 IP 变化通知

📅 检测时间：2026-03-10 14:27:00

🔴 旧 IP：180.113.194.180
🟢 新 IP：123.253.224.104

⚠️ 请在微信公众号后台更新 IP 白名单：
1. 登录 https://mp.weixin.qq.com
2. 开发 → 基本配置 → IP 白名单
3. 添加新 IP：123.253.224.104
4. 删除旧 IP：180.113.194.180

📝 配置完成后测试发布功能。

✅ IP 监控完成（检测到变化）
```

### 自动监控

**状态：** ✅ 已启动（每 5 分钟检查一次）

**查看状态：**
```bash
# 查看 LaunchAgent 状态
launchctl list | grep ip-monitor

# 查看日志
tail -f ~/openclaw-workspace/logs/ip-monitor.log
```

**停止监控：**
```bash
launchctl unload ~/Library/LaunchAgents/com.openclaw.ip-monitor.plist
```

**重启监控：**
```bash
launchctl unload ~/Library/LaunchAgents/com.openclaw.ip-monitor.plist
launchctl load ~/Library/LaunchAgents/com.openclaw.ip-monitor.plist
```

---

## 📝 通知流程

### IP 变化时

1. **检测变化** - 脚本检测到 IP 变化
2. **写入通知** - 写入 `logs/pending-notify.txt`
3. **Heartbeat 发送** - 下次 heartbeat 时通过飞书发送
4. **用户收到通知** - 包含新旧 IP 和更新步骤

### 通知内容

```
🌐 公网 IP 变化通知

📅 检测时间：2026-03-10 14:27:00

🔴 旧 IP：180.113.194.180
🟢 新 IP：123.253.224.104

⚠️ 请在微信公众号后台更新 IP 白名单：
1. 登录 https://mp.weixin.qq.com
2. 开发 → 基本配置 → IP 白名单
3. 添加新 IP：123.253.224.104
4. 删除旧 IP：180.113.194.180

📝 配置完成后测试发布功能。
```

---

## 🎯 配置步骤

### 步骤 1：微信公众号后台更新

**收到通知后：**

1. 登录微信公众平台
   - https://mp.weixin.qq.com

2. 进入 IP 白名单配置
   - 开发 → 基本配置 → 开发者 ID → IP 白名单

3. 更新 IP 地址
   - 添加新 IP（通知中的🟢新 IP）
   - 删除旧 IP（通知中的🔴旧 IP）

4. 保存并确认
   - 可能需要管理员扫码

### 步骤 2：测试发布功能

**更新白名单后：**

```bash
cd ~/openclaw-workspace/skills/wechat-article-writer

# 测试微信 API 连接
python3 -c "
import requests
import json

with open('config.json', 'r') as f:
    config = json.load(f)

appid = config['wechat_appid']
appsecret = config['wechat_appsecret']

url = f'https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid={appid}&secret={appsecret}'
response = requests.get(url)
data = response.json()

if 'access_token' in data:
    print('✅ 微信公众号连接成功！')
else:
    print('❌ 连接失败：', data)
"

# 测试发布文章
python3 scripts/publish_draft.py \
  --article "scripts/output/articles/article_xxx.md" \
  --title "文章标题"
```

---

## 📊 当前状态

### 已配置

| 项目 | 状态 | 说明 |
|------|------|------|
| **监控脚本** | ✅ 已创建 | `scripts/monitor_ip.py` |
| **Shell 脚本** | ✅ 已创建 | `scripts/ip-monitor-check.sh` |
| **LaunchAgent** | ✅ 已加载 | `com.openclaw.ip-monitor` |
| **IP 记录** | ✅ 已保存 | 当前 IP: 123.253.224.104 |
| **通知机制** | ✅ 已配置 | 飞书通知 |

### 微信公众号配置

| 项目 | 值 | 状态 |
|------|-----|------|
| **AppID** | wx6211e097a5ed2c87 | ✅ 已配置 |
| **AppSecret** | f550525da1d55dd4e324bcc76aa4787b | ✅ 已配置 |
| **IP 白名单** | 待更新 | ⚠️ 需要配置最新 IP |

---

## 🔧 故障排查

### 问题 1：无法获取 IP

**现象：**
```
❌ https://api.ipify.org 失败：...
❌ https://icanhazip.com 失败：...
```

**解决：**
- 检查网络连接
- 脚本会自动尝试多个 IP 服务
- 如果都失败，会跳过本次检查

### 问题 2：通知未发送

**现象：** IP 变化但未收到通知

**检查：**
```bash
# 检查通知文件
cat ~/openclaw-workspace/logs/pending-notify.txt

# 检查 heartbeat 状态
openclaw gateway status
```

**解决：**
- 确保 heartbeat 正常运行
- 检查飞书插件配置

### 问题 3：微信 API 连接失败

**现象：**
```
❌ 连接失败：{'errcode': 40164, ...}
```

**原因：** IP 不在白名单

**解决：**
1. 查看最新 IP：`cat ~/openclaw-workspace/logs/last_ip.txt`
2. 在公众号后台添加该 IP
3. 等待 5 分钟生效
4. 重新测试

---

## 📋 配置文件

### monitor_ip.py

**位置：** `scripts/monitor_ip.py`

**功能：**
- 获取当前公网 IP
- 对比上次记录
- 检测变化时发送通知

### ip-monitor-check.sh

**位置：** `scripts/ip-monitor-check.sh`

**功能：**
- Shell 包装脚本
- 被 LaunchAgent 调用
- 记录日志

### com.openclaw.ip-monitor.plist

**位置：** `~/Library/LaunchAgents/com.openclaw.ip-monitor.plist`

**配置：**
```xml
<key>StartInterval</key>
<integer>300</integer>  <!-- 每 5 分钟 -->
```

---

## 🎯 最佳实践

### IP 记录备份

**定期备份 IP 记录：**
```bash
# 添加到 git
cd ~/openclaw-workspace
git add logs/last_ip.txt
git commit -m "backup: IP 记录"
git push
```

### 通知清理

**Heartbeat 会自动删除通知文件，无需手动清理。**

### 监控日志

**定期查看日志：**
```bash
# 查看最近 10 条日志
tail -n 10 ~/openclaw-workspace/logs/ip-monitor.log

# 实时监控
tail -f ~/openclaw-workspace/logs/ip-monitor.log
```

---

## 🔗 相关资源

**微信公众平台：**
- 登录：https://mp.weixin.qq.com
- 开发文档：https://developers.weixin.qq.com/doc/offiaccount/
- IP 白名单配置：开发 → 基本配置 → IP 白名单

**IP 查询服务：**
- https://api.ipify.org
- https://icanhazip.com
- https://ifconfig.me/ip
- https://ip.sb

---

_文档生成时间：2026-03-10 14:27_  
_作者：AI 助手_
