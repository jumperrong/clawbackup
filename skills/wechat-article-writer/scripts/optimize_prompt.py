#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
optimize_prompt.py - 使用 AI 模型优化生图提示词
调用 qwen3.5-plus 模型分析和优化提示词
"""

import argparse
import os
import json
from openai import OpenAI

def load_config():
    """加载配置文件"""
    config_path = os.path.join(os.path.dirname(__file__), '..', 'config.json')
    with open(config_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def optimize_prompt(base_prompt, article_content="", section_title="", style="干货"):
    """
    使用 AI 优化提示词
    
    Args:
        base_prompt: 基础提示词（模板生成）
        article_content: 文章内容（可选）
        section_title: 章节标题（可选）
        style: 文章风格
    
    Returns:
        str: 优化后的提示词
    """
    config = load_config()
    
    # 构建优化请求
    system_prompt = """你是一位专业的 AI 绘画提示词优化专家。
你的任务是根据文章内容和章节标题，优化生图提示词，让生成的图片更贴合内容。

优化原则：
1. 保持提示词简洁明了（100 字以内）
2. 突出核心主题和关键元素
3. 指定适合的风格和色调
4. 避免抽象和模糊的描述
5. 符合健康科普的专业性和可读性"""

    user_prompt = f"""请优化以下生图提示词：

【基础提示词】
{base_prompt}

【文章内容】（前 500 字）
{article_content[:500] if article_content else "无"}

【章节标题】
{section_title if section_title else "无"}

【文章风格】
{style}

请输出优化后的提示词（直接输出提示词，不要其他说明）："""

    # 调用 Bailian API（使用 qwen3.5-plus）
    client = OpenAI(
        api_key=config.get('bailian_api_key'),
        base_url=config.get('bailian_base_url', 'https://coding.dashscope.aliyuncs.com/v1')
    )
    
    response = client.chat.completions.create(
        model="qwen3.5-plus",  # 使用 qwen3.5-plus，性价比高
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        temperature=0.7,
        max_tokens=200
    )
    
    optimized_prompt = response.choices[0].message.content.strip()
    
    return optimized_prompt

def batch_optimize_prompts(articles_data):
    """
    批量优化提示词
    
    Args:
        articles_data: 文章数据列表
    
    Returns:
        list: 优化后的提示词列表
    """
    optimized_prompts = []
    
    for article in articles_data:
        base_prompt = article.get('base_prompt', '')
        content = article.get('content', '')
        title = article.get('section_title', '')
        style = article.get('style', '干货')
        
        print(f"🔧 优化提示词：{title}")
        optimized = optimize_prompt(base_prompt, content, title, style)
        optimized_prompts.append({
            'original': base_prompt,
            'optimized': optimized,
            'title': title
        })
        print(f"✅ 优化完成\n")
    
    return optimized_prompts

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='AI 优化生图提示词')
    parser.add_argument('--prompt', type=str, help='基础提示词')
    parser.add_argument('--content', type=str, default='', help='文章内容')
    parser.add_argument('--title', type=str, default='', help='章节标题')
    parser.add_argument('--style', type=str, default='干货', help='文章风格')
    
    args = parser.parse_args()
    
    if not args.prompt:
        print("❌ 请提供基础提示词（--prompt）")
        parser.print_help()
        exit(1)
    
    print("="*60)
    print("🤖 AI 提示词优化")
    print("="*60)
    print()
    
    print(f"📝 基础提示词：\n{args.prompt}\n")
    
    optimized = optimize_prompt(
        base_prompt=args.prompt,
        article_content=args.content,
        section_title=args.title,
        style=args.style
    )
    
    print(f"✨ 优化后的提示词：\n{optimized}\n")
    print("="*60)
