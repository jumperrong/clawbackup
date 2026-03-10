#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
write_article.py - AI 生成公众号文章
调用 DeepSeek API 生成文章初稿并保存为 Markdown 文件
"""

import argparse
import os
import json
from datetime import datetime
from openai import OpenAI

# 4 种写作风格
STYLE_PROMPTS = {
    "干货": "专业、信息密度高、有实用价值，使用清晰的逻辑结构，提供可操作的建议和具体步骤。",
    "情感": "温暖、有共情力、有故事感，使用柔和的语言，引发读者情感共鸣，适当使用金句。",
    "资讯": "简洁、客观，信息密度高，使用新闻体，突出关键信息和数据，避免主观评价。",
    "活泼": "轻松、幽默、接地气，使用网络流行语，语言生动有趣，像和朋友聊天一样。"
}

def load_config():
    """加载配置文件"""
    config_path = os.path.join(os.path.dirname(__file__), '..', 'config.json')
    with open(config_path, 'r', encoding='utf-8') as f:
        return json.load(f)

# 写作风格提示词优化（适配 Qwen 模型）
STYLE_PROMPTS = {
    "干货": "专业、信息密度高、有实用价值，使用清晰的逻辑结构，提供可操作的建议和具体步骤。适合教程、指南、测评类文章。",
    "情感": "温暖、有共情力、有故事感，使用柔和的语言，引发读者情感共鸣，适当使用金句。适合情感文、鸡汤文。",
    "资讯": "简洁、客观，信息密度高，使用新闻体，突出关键信息和数据，避免主观评价。适合新闻、行业动态。",
    "活泼": "轻松、幽默、接地气，使用网络流行语，语言生动有趣，像和朋友聊天一样。适合生活分享、种草。"
}

def write_article(topic, style="干货", keywords="", length=1500, title_hint=""):
    """
    生成公众号文章
    
    Args:
        topic: 文章主题
        style: 写作风格（干货/情感/资讯/活泼）
        keywords: 关键词（可选）
        length: 文章长度（字数）
        title_hint: 标题提示（可选）
    
    Returns:
        dict: 文章元数据（标题、内容、文件路径）
    """
    config = load_config()
    
    # 1. 构建 prompt
    style_prompt = STYLE_PROMPTS.get(style, STYLE_PROMPTS["干货"])
    
    system_prompt = """你是一位经验丰富的公众号爆款文章写手。
请根据用户提供的主题和要求，写一篇高质量的公众号文章。

要求：
1. 标题吸引人，有点击欲
2. 结构清晰，使用##标记小标题
3. 语言流畅，符合公众号阅读习惯
4. 适当使用 emoji 增加可读性
5. 文末有互动引导（点赞、在看、评论）"""

    user_prompt = f"""
主题：{topic}
风格：{style_prompt}
关键词：{keywords if keywords else "无特定要求"}
字数：约{length}字
{f"标题提示：{title_hint}" if title_hint else ""}

请开始创作：
"""

    # 2. 调用 Bailian API（使用 qwen3-max 复杂任务最强性能）
    client = OpenAI(
        api_key=config.get('bailian_api_key', config.get('deepseek_api_key')),
        base_url=config.get('bailian_base_url', 'https://coding.dashscope.aliyuncs.com/v1')
    )
    
    response = client.chat.completions.create(
        model=config.get('writing_model', 'qwen3-max-2026-01-23'),
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        temperature=0.7,
        max_tokens=3000
    )
    
    content = response.choices[0].message.content
    
    # 3. 保存 Markdown 文件
    output_dir = os.path.join(os.path.dirname(__file__), 'output', 'articles')
    os.makedirs(output_dir, exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"article_{timestamp}.md"
    filepath = os.path.join(output_dir, filename)
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    
    # 4. 提取标题（第一行）
    title = content.split('\n')[0].replace('#', '').strip()
    
    # 5. 输出元数据
    metadata = {
        "title": title,
        "content": content,
        "filepath": filepath,
        "word_count": len(content),
        "style": style,
        "created_at": datetime.now().isoformat()
    }
    
    print(f"✅ 文章生成完成")
    print(f"📄 标题：{title}")
    print(f"📊 字数：{len(content)}")
    print(f"💾 路径：{filepath}")
    
    return metadata

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='AI 生成公众号文章')
    parser.add_argument('--topic', type=str, required=True, help='文章主题')
    parser.add_argument('--style', type=str, default='干货', 
                       choices=['干货', '情感', '资讯', '活泼'], help='写作风格')
    parser.add_argument('--keywords', type=str, default='', help='关键词')
    parser.add_argument('--length', type=int, default=1500, help='文章字数')
    parser.add_argument('--title-hint', type=str, default='', help='标题提示')
    
    args = parser.parse_args()
    
    write_article(
        topic=args.topic,
        style=args.style,
        keywords=args.keywords,
        length=args.length,
        title_hint=args.title_hint
    )
