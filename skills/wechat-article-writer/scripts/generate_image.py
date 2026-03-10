#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
generate_image.py - AI 生成封面图
调用豆包 AI 生图接口（Seedream）生成公众号封面图
使用 OpenAI SDK 兼容方式
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

def generate_cover_image(topic, title="", style="干货", cover_type="header"):
    """
    生成封面图
    
    Args:
        topic: 文章主题
        title: 文章标题（可选）
        style: 文章风格
        cover_type: 封面类型（header=头条封面 2.35:1, share=分享封面 1:1）
    
    Returns:
        dict: 图片元数据
    """
    config = load_config()
    
    # 1. 构建提示词
    style_prompts = {
        "干货": "专业、简洁、信息图表风格",
        "情感": "温暖、柔和、治愈系配色",
        "资讯": "现代、简洁、新闻风格",
        "活泼": "鲜艳、活泼、卡通风格"
    }
    
    prompt = f"""公众号封面图，主题：{topic}
{f"标题：{title}" if title else ""}
风格要求：{style_prompts.get(style, style_prompts['干货'])}
尺寸比例：2.35:1（公众号封面标准比例）
质量要求：高清、精美、适合移动端阅读
"""
    
    # 2. 调用豆包 API 生图（使用 OpenAI SDK）
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
    filename = f"cover_{timestamp}.jpg"
    filepath = os.path.join(output_dir, filename)
    
    # 临时保存原始图片
    temp_path = os.path.join(output_dir, f"temp_{filename}")
    with open(temp_path, 'wb') as f:
        f.write(image_response.content)
    
    # 4. 压缩图片到微信要求
    from PIL import Image
    
    img = Image.open(temp_path)
    
    # 转换为 RGB（处理 PNG 等格式）
    if img.mode in ('RGBA', 'LA', 'P'):
        img = img.convert('RGB')
    
    # 根据封面类型设置尺寸
    if cover_type == "header":
        # 头条封面：2.35:1, 900x383
        target_width, target_height = 900, 383
        target_ratio = 2.35
        size_label = "900x383"
    else:  # share
        # 分享封面：1:1, 383x383
        target_width, target_height = 383, 383
        target_ratio = 1.0
        size_label = "383x383"
    
    # 裁剪到目标比例
    current_ratio = img.width / img.height
    
    if current_ratio > target_ratio:
        # 图片太宽，裁剪宽度
        new_width = int(img.height * target_ratio)
        left = (img.width - new_width) // 2
        img = img.crop((left, 0, left + new_width, img.height))
    else:
        # 图片太高，裁剪高度
        new_height = int(img.width / target_ratio)
        top = (img.height - new_height) // 2
        img = img.crop((0, top, img.width, top + new_height))
    
    # 缩放到目标尺寸
    img = img.resize((target_width, target_height), Image.Resampling.LANCZOS)
    
    # 压缩到小于 100KB
    quality = 85
    img.save(filepath, 'JPEG', quality=quality, optimize=True, progressive=True)
    
    # 如果文件大于 100KB，降低质量重新保存
    while os.path.getsize(filepath) > 102400 and quality > 10:  # 100KB = 102400 bytes
        quality -= 5
        img.save(filepath, 'JPEG', quality=quality, optimize=True, progressive=True)
    
    # 删除临时文件
    os.remove(temp_path)
    
    file_size = os.path.getsize(filepath) / 1024  # KB
    
    # 5. 输出元数据
    metadata = {
        "filepath": filepath,
        "url": image_url,
        "prompt": prompt,
        "size": size_label,
        "cover_type": cover_type,
        "file_size_kb": round(file_size, 2),
        "created_at": datetime.now().isoformat()
    }
    
    print(f"✅ 封面图生成完成 ({'头条' if cover_type == 'header' else '分享'})")
    print(f"🖼️ 路径：{filepath}")
    print(f"📐 尺寸：{size_label}")
    print(f"💾 大小：{file_size:.2f} KB")
    print(f"🔗 URL: {image_url}")
    
    return metadata

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='AI 生成公众号封面图')
    parser.add_argument('--topic', type=str, required=True, help='文章主题')
    parser.add_argument('--title', type=str, default='', help='文章标题')
    parser.add_argument('--style', type=str, default='干货', 
                       choices=['干货', '情感', '资讯', '活泼'], help='文章风格')
    parser.add_argument('--type', type=str, default='header',
                       choices=['header', 'share'], 
                       help='封面类型：header=头条封面 (2.35:1), share=分享封面 (1:1)')
    
    args = parser.parse_args()
    
    generate_cover_image(
        topic=args.topic,
        title=args.title,
        style=args.style,
        cover_type=args.type
    )
