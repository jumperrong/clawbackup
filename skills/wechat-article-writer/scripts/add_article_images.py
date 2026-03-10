#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
add_article_images.py - 智能配图（完全使用 AI 生成提示词 + 标签）
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

def generate_prompt_with_ai(topic, section_title, style="干货", content=""):
    """使用 AI 生成配图提示词"""
    config = load_config()
    
    system_prompt = """你是一位专业的 AI 绘画提示词生成专家。
你的任务是为健康科普文章生成配图提示词。

生成原则：
1. 简洁明了（100 字以内）
2. 突出医学专业性和准确性
3. 指定适合的风格和色调
4. 符合健康科普的严谨性
5. 16:9 比例，适合阅读

风格要求：
- 医学插图风格
- 清新、简洁、专业
- 色调温暖、明亮
- 适合健康科普阅读"""

    user_prompt = f"""请为以下健康科普文章章节生成配图提示词：

【文章主题】
{topic}

【章节标题】
{section_title}

【文章风格】
{style}

【文章内容】（前 500 字）
{content[:500] if content else "无"}

请生成提示词（直接输出提示词，不要其他说明）："""

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

def generate_section_image(topic, section_title, style="干货", content=""):
    """为章节生成配图（使用 AI 生成提示词 + 标签）"""
    config = load_config()
    
    # 1. 使用 AI 生成提示词
    print(f"  🤖 使用 AI 生成提示词...")
    prompt = generate_prompt_with_ai(topic, section_title, style, content)
    print(f"  ✅ 提示词生成完成")
    
    # 2. 生成标签（从章节标题提取关键词）
    tags = [
        topic.replace(" ", "_")[:10],
        section_title.replace(" ", "_")[:10],
        style,
        "健康科普",
        "医学插图"
    ]
    
    # 3. 调用豆包 API 生图
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
    
    # 4. 保存图片
    output_dir = os.path.join(os.path.dirname(__file__), 'output', 'images')
    os.makedirs(output_dir, exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    tags_str = "_".join([tag.replace(" ", "_")[:8] for tag in tags[:3]])
    filename = f"section_{tags_str}_{timestamp}.jpg"
    filepath = os.path.join(output_dir, filename)
    
    with open(filepath, 'wb') as f:
        f.write(image_response.content)
    
    # 5. 保存元数据（含标签）
    metadata = {
        "filepath": filepath,
        "url": image_url,
        "prompt": prompt,
        "size": "16:9",
        "created_at": datetime.now().isoformat(),
        "topic": topic,
        "section_title": section_title,
        "style": style,
        "tags": tags,
        "use_ai_prompt": True
    }
    
    # 保存元数据到 JSON
    meta_path = os.path.join(output_dir, f"{filename}.meta.json")
    with open(meta_path, 'w', encoding='utf-8') as f:
        json.dump(metadata, f, ensure_ascii=False, indent=2)
    
    print(f"  🏷️ 标签：{', '.join(tags)}")
    
    return filepath, tags

def analyze_article_structure(md_content):
    """分析文章结构，提取##标题"""
    pattern = r'^##\s+(.+)$'
    matches = re.finditer(pattern, md_content, re.MULTILINE)
    sections = []
    for match in matches:
        sections.append({
            "title": match.group(1),
            "position": match.start()
        })
    return sections

def add_images_to_article(article_path, topic, style="干货"):
    """为文章添加配图（使用 AI 生成提示词 + 标签）"""
    # 处理相对路径
    if not os.path.isabs(article_path):
        article_path = os.path.join(os.path.dirname(__file__), '..', article_path)
    
    with open(article_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    sections = analyze_article_structure(content)
    
    # 为前 3 个章节配图
    images_added = 0
    all_tags = []
    
    for section in sections[:3]:
        print(f"\n🔧 生成配图：{section['title']}")
        image_path, tags = generate_section_image(
            topic=topic,
            section_title=section['title'],
            style=style,
            content=content
        )
        
        # 在章节标题后插入图片
        image_markdown = f"\n\n![{section['title']}]({image_path})\n\n"
        insert_pos = section['position'] + len(f"## {section['title']}")
        content = content[:insert_pos] + image_markdown + content[insert_pos:]
        
        images_added += 1
        all_tags.extend(tags)
        print(f"✅ 已插入配图：{section['title']}")
    
    # 保存更新后的文章
    with open(article_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    # 保存所有标签到文件（便于复用）
    tags_file = os.path.join(os.path.dirname(article_path), 'image_tags.json')
    unique_tags = list(set(all_tags))  # 去重
    
    tags_data = {
        "topic": topic,
        "style": style,
        "created_at": datetime.now().isoformat(),
        "images_count": images_added,
        "tags": unique_tags
    }
    
    with open(tags_file, 'w', encoding='utf-8') as f:
        json.dump(tags_data, f, ensure_ascii=False, indent=2)
    
    print(f"\n✅ 共插入 {images_added} 张配图")
    print(f"🏷️ 标签已保存到：{tags_file}")
    
    return images_added, unique_tags

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='为公众号文章智能配图（AI 生成提示词 + 标签）')
    parser.add_argument('--article', type=str, required=True, help='文章路径')
    parser.add_argument('--topic', type=str, required=True, help='文章主题')
    parser.add_argument('--style', type=str, default='干货', help='文章风格')
    
    args = parser.parse_args()
    
    add_images_to_article(args.article, args.topic, args.style)
