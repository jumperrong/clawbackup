#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
generate_image.py - AI 生成封面图（完全使用 AI 生成提示词）
调用 qwen3.5-plus 生成提示词，然后调用豆包 AI 生图
"""

import argparse
import os
import json
import requests
from datetime import datetime
from openai import OpenAI

def load_config():
    """加载配置文件"""
    config_path = os.path.join(os.path.dirname(__file__), '..', 'config.json')
    with open(config_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def generate_prompt_with_ai(topic, title="", style="干货", content=""):
    """
    使用 AI 生成提示词
    
    Args:
        topic: 文章主题
        title: 文章标题（可选）
        style: 文章风格
        content: 文章内容（可选，用于更准确生成）
    
    Returns:
        str: AI 生成的提示词
    """
    config = load_config()
    
    system_prompt = """你是一位专业的 AI 绘画提示词生成专家。
你的任务是根据文章主题和标题，生成适合公众号封面的 AI 绘画提示词。

生成原则：
1. 简洁明了（100 字以内）
2. 突出核心主题和关键元素
3. 指定适合的风格和色调
4. 符合公众号封面标准（2.35:1 比例）
5. 高清、精美、适合移动端阅读

风格参考：
- 干货：专业、简洁、信息图表风格
- 情感：温暖、柔和、治愈系配色
- 资讯：现代、简洁、新闻风格
- 活泼：鲜艳、活泼、卡通风格"""

    user_prompt = f"""请为以下公众号文章生成封面图提示词：

【文章主题】
{topic}

【文章标题】
{title if title else "无"}

【文章风格】
{style}

【文章内容】（前 500 字）
{content[:500] if content else "无"}

请生成提示词（直接输出提示词，不要其他说明）："""

    # 调用 Bailian API（使用 qwen3.5-plus）
    client = OpenAI(
        api_key=config.get('bailian_api_key'),
        base_url=config.get('bailian_base_url', 'https://coding.dashscope.aliyuncs.com/v1')
    )
    
    response = client.chat.completions.create(
        model="qwen3.5-plus",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        temperature=0.7,
        max_tokens=200
    )
    
    ai_prompt = response.choices[0].message.content.strip()
    
    return ai_prompt

def generate_cover_image(topic, title="", style="干货", content="", use_ai_prompt=True, tags=None):
    """
    生成封面图
    
    Args:
        topic: 文章主题
        title: 文章标题（可选）
        style: 文章风格
        content: 文章内容（可选，用于 AI 生成提示词）
        use_ai_prompt: 是否使用 AI 生成提示词（默认 True）
        tags: 图片标签列表（可选）
    
    Returns:
        dict: 图片元数据
    """
    config = load_config()
    
    # 1. 生成提示词
    if use_ai_prompt:
        print(f"🤖 使用 AI 生成提示词...")
        prompt = generate_prompt_with_ai(topic, title, style, content)
        print(f"✅ 提示词生成完成")
    else:
        # 备用：模板方式（不推荐）
        style_prompts = {
            "干货": "专业、简洁、信息图表风格",
            "情感": "温暖、柔和、治愈系配色",
            "资讯": "现代、简洁、新闻风格",
            "活泼": "鲜艳、活泼、卡通风格"
        }
        prompt = f"""公众号封面图，主题：{topic}
{f"标题：{title}" if title else ""}
风格要求：{style_prompts.get(style, style_prompts['干货'])}
尺寸比例：2.35:1
质量要求：高清、精美、适合移动端阅读
"""
    
    print(f"\n📝 提示词：\n{prompt}\n")
    
    # 2. 调用豆包 API 生图
    client = OpenAI(
        base_url="https://ark.cn-beijing.volces.com/api/v3",
        api_key=config['doubao_api_key'],
    )
    
    imagesResponse = client.images.generate(
        model="doubao-seedream-4-5-251128",
        prompt=prompt,
        size="2K",
        response_format="url",
        extra_body={
            "watermark": True,
        },
    )
    
    # 3. 下载并保存图片
    image_url = imagesResponse.data[0].url
    image_response = requests.get(image_url)
    
    output_dir = os.path.join(os.path.dirname(__file__), 'output', 'images')
    os.makedirs(output_dir, exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # 生成标签文件名
    if tags:
        tags_str = "_".join(tags[:3])  # 取前 3 个标签
        filename = f"cover_{tags_str}_{timestamp}.jpg"
    else:
        filename = f"cover_{timestamp}.jpg"
    
    filepath = os.path.join(output_dir, filename)
    
    # 临时保存原始图片
    temp_path = os.path.join(output_dir, f"temp_{filename}")
    with open(temp_path, 'wb') as f:
        f.write(image_response.content)
    
    # 4. 压缩图片到微信要求
    from PIL import Image
    
    img = Image.open(temp_path)
    
    # 转换为 RGB
    if img.mode in ('RGBA', 'LA', 'P'):
        img = img.convert('RGB')
    
    # 头条封面：2.35:1, 900x383
    target_width, target_height = 900, 383
    target_ratio = 2.35
    
    # 裁剪到目标比例
    current_ratio = img.width / img.height
    
    if current_ratio > target_ratio:
        new_width = int(img.height * target_ratio)
        left = (img.width - new_width) // 2
        img = img.crop((left, 0, left + new_width, img.height))
    else:
        new_height = int(img.width / target_ratio)
        top = (img.height - new_height) // 2
        img = img.crop((0, top, img.width, top + new_height))
    
    # 缩放到目标尺寸
    img = img.resize((target_width, target_height), Image.Resampling.LANCZOS)
    
    # 压缩到小于 100KB
    quality = 85
    img.save(filepath, 'JPEG', quality=quality, optimize=True, progressive=True)
    
    while os.path.getsize(filepath) > 102400 and quality > 10:
        quality -= 5
        img.save(filepath, 'JPEG', quality=quality, optimize=True, progressive=True)
    
    # 删除临时文件
    os.remove(temp_path)
    
    file_size = os.path.getsize(filepath) / 1024
    
    # 5. 保存元数据（含标签）
    metadata = {
        "filepath": filepath,
        "url": image_url,
        "prompt": prompt,
        "size": "900x383",
        "cover_type": "header",
        "file_size_kb": round(file_size, 2),
        "created_at": datetime.now().isoformat(),
        "topic": topic,
        "title": title,
        "style": style,
        "tags": tags if tags else [],
        "use_ai_prompt": use_ai_prompt
    }
    
    # 保存元数据到 JSON 文件
    meta_path = os.path.join(output_dir, f"{filename}.meta.json")
    with open(meta_path, 'w', encoding='utf-8') as f:
        json.dump(metadata, f, ensure_ascii=False, indent=2)
    
    print(f"\n✅ 封面图生成完成")
    print(f"🖼️ 路径：{filepath}")
    print(f"📐 尺寸：900x383")
    print(f"💾 大小：{file_size:.2f} KB")
    print(f"🏷️ 标签：{', '.join(tags) if tags else '无'}")
    
    return metadata

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='AI 生成公众号封面图（完全使用 AI 生成提示词）')
    parser.add_argument('--topic', type=str, required=True, help='文章主题')
    parser.add_argument('--title', type=str, default='', help='文章标题')
    parser.add_argument('--style', type=str, default='干货', 
                       choices=['干货', '情感', '资讯', '活泼'], help='文章风格')
    parser.add_argument('--content', type=str, default='', help='文章内容（用于 AI 生成提示词）')
    parser.add_argument('--tags', type=str, nargs='+', help='图片标签（用于复用）')
    parser.add_argument('--no-ai', action='store_true', help='不使用 AI 生成提示词（备用）')
    
    args = parser.parse_args()
    
    generate_cover_image(
        topic=args.topic,
        title=args.title,
        style=args.style,
        content=args.content,
        use_ai_prompt=not args.no_ai,
        tags=args.tags
    )
