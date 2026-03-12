# TOOLS.md - Local Notes

Skills define _how_ tools work. This file is for _your_ specifics — the stuff that's unique to your setup.

## What Goes Here

Things like:

- Camera names and locations
- SSH hosts and aliases
- Preferred voices for TTS
- Speaker/room names
- Device nicknames
- Anything environment-specific

## 🔍 搜索工具配置

**已启用：**
- ✅ **Tavily Search** - 唯一使用的搜索工具
  - API Key: `TAVILY_API_KEY` (已配置)
  - 技能路径：`skills/tavily-search/`
  - 用法：`node scripts/search.mjs "query"`

**已禁用：**
- ❌ **Brave Search (web_search)** - 不使用，已禁用
  - 原因：用户明确要求只用 Tavily
  - 行为：即使 web_search 工具可用，也不主动调用

## Examples

```markdown
### Cameras

- living-room → Main area, 180° wide angle
- front-door → Entrance, motion-triggered

### SSH

- home-server → 192.168.1.100, user: admin

### TTS

- Preferred voice: "Nova" (warm, slightly British)
- Default speaker: Kitchen HomePod
```

## Why Separate?

Skills are shared. Your setup is yours. Keeping them apart means you can update skills without losing your notes, and share skills without leaking your infrastructure.

---

Add whatever helps you do your job. This is your cheat sheet.
