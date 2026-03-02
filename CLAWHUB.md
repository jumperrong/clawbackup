# ClawHub 使用指南

ClawHub 是 OpenClaw 的公共技能注册中心，可以搜索、安装、更新技能。

网站：https://clawhub.ai

## 安装 ClawHub CLI

```bash
npm i -g clawhub
# 或
pnpm add -g clawhub
```

## 常用命令

### 搜索技能

```bash
# 搜索技能
clawhub search "calendar"
clawhub search "gmail"
clawhub search "spotify"

# 限制结果数量
clawhub search "todo" --limit 10
```

### 安装技能

```bash
# 安装技能（到当前目录的 skills/ 文件夹）
clawhub install <skill-slug>

# 安装到指定目录
clawhub install <skill-slug> --dir ~/.openclaw/skills

# 强制覆盖已存在的技能
clawhub install <skill-slug> --force

# 安装特定版本
clawhub install <skill-slug> --version 1.2.0
```

### 更新技能

```bash
# 更新所有已安装的技能
clawhub update

# 更新特定技能
clawhub update <skill-slug>
```

### 查看已安装的技能

```bash
clawhub list
```

### 卸载技能

```bash
clawhub uninstall <skill-slug>
```

### 浏览最新技能

```bash
clawhub explore
```

### 查看技能详情（不安装）

```bash
clawhub inspect <skill-slug>
```

## 工作流程

1. **搜索技能** → `clawhub search "关键词"`
2. **查看技能详情** → `clawhub inspect <slug>` 或上 clawhub.ai 网站
3. **安装技能** → `clawhub install <slug>`
4. **重启 OpenClaw 会话** → 新技能在下次会话中生效

## 技能安装位置

默认安装到：
- 当前工作目录的 `./skills/` 文件夹
- 或 OpenClaw workspace 配置的 `skills/` 文件夹

OpenClaw 会从以下位置加载技能：
- `~/.openclaw/skills/` (全局)
- `<workspace>/skills/` (工作区)
-  bundled skills (内置)

## 示例

```bash
# 搜索日历相关技能
clawhub search "calendar"

# 安装 Google Calendar 技能
clawhub install google-calendar

# 安装到全局技能目录
clawhub install google-calendar --dir ~/.openclaw/skills

# 查看所有已安装技能
clawhub list

# 更新所有技能
clawhub update
```

## 注意事项

- 安装新技能后需要**重启 OpenClaw 会话**才能使用
- 技能优先级：工作区 > 全局 > 内置
- 使用 `openclaw skills list` 查看哪些技能已就绪
