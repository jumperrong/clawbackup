#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
add_article_images.py - 智能配图
分析文章结构，在小标题处自动插入配图
"""

import argparse
import os
import re
import json
import requests
from datetime import datetime

def load_config():
    config_path = os.path.join(os.path.dirname(__file__), '..', 'config.json')
    with open(config_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def analyze_article_structure(md_content):
    """分析文章结构，找出##标题"""
    pattern = r'^##\s+(.+)$'
    matches = re.finditer(pattern, md_content, re.MULTILINE)
    sections = []
    for match in matches:
        sections.append({
            "title": match.group(1),
            "position": match.start()
        })
    return sections

def generate_section_image(topic, section_title, style="干货"):
    """为章节生成配图"""
    config = load_config()
    
    prompt = f"""健康科普插图，主题：{topic}
内容：{section_title}
风格：{style}，清新、简洁、积极向上、适合阅读
色调：温暖、明亮、专业
尺寸比例：16:9
"""
    
    # 使用 OpenAI SDK 调用豆包 API
    from openai import OpenAI
    
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
    
    image_url = imagesResponse.data[0].url
    image_response = requests.get(image_url)
    
    output_dir = os.path.join(os.path.dirname(__file__), 'output', 'images')
    os.makedirs(output_dir, exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"section_{timestamp}.jpg"
    filepath = os.path.join(output_dir, filename)
    
    with open(filepath, 'wb') as f:
        f.write(image_response.content)
    
    return filepath

def add_images_to_article(article_path, topic, style="干货"):
    """为文章添加配图"""
    # 处理相对路径
    if not os.path.isabs(article_path):
        article_path = os.path.join(os.path.dirname(__file__), '..', article_path)
    
    with open(article_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    sections = analyze_article_structure(content)
    
    # 为前 3 个章节配图
    images_added = 0
    for section in sections[:3]:
        image_path = generate_section_image(topic, section['title'], style)
        
        # 在章节标题后插入图片
        image_markdown = f"\n\n![{section['title']}]({image_path})\n\n"
        insert_pos = section['position'] + len(f"## {section['title']}")
        content = content[:insert_pos] + image_markdown + content[insert_pos:]
        images_added += 1
        print(f"✅ 已插入配图：{section['title']}")
    
    # 保存更新后的文章
    with open(article_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"✅ 共插入 {images_added} 张配图")
    return images_added

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='为公众号文章智能配图')
    parser.add_argument('--article', type=str, required=True, help='文章路径')
    parser.add_argument('--topic', type=str, required=True, help='文章主题')
    parser.add_argument('--style', type=str, default='干货', help='文章风格')
    
    args = parser.parse_args()
    
    add_images_to_article(args.article, args.topic, args.style)
