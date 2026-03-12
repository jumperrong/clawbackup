#!/usr/bin/env python3
"""生成测试图片"""
from PIL import Image, ImageDraw

# 创建渐变背景
img = Image.new('RGB', (800, 600), color=(102, 126, 234))
draw = ImageDraw.Draw(img)

# 添加文字
text_lines = [
    "🦞 钉钉图片发送测试",
    "",
    "✅ 图片生成成功",
    "✅ 文件路径正确",
    "✅ 准备发送到钉钉",
    "",
    "测试时间：2026-03-12 19:57",
    "",
    "小爪 | OpenClaw Assistant"
]

y = 200
for line in text_lines:
    draw.text((50, y), line, fill=(255, 255, 255))
    y += 50

# 保存
img.save("/Users/jumpermac/.openclaw/workspace/test-dingtalk-image.png")
print("✅ 测试图片已生成")
