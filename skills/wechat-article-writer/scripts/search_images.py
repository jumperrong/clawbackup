#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
search_images.py - 搜索和复用已生成的图片
根据标签搜索图片，支持按主题、风格、标签搜索
"""

import os
import json
import argparse
from datetime import datetime

def load_all_metadata(images_dir):
    """加载所有图片的元数据"""
    metadata_list = []
    
    for filename in os.listdir(images_dir):
        if filename.endswith('.meta.json'):
            filepath = os.path.join(images_dir, filename)
            with open(filepath, 'r', encoding='utf-8') as f:
                metadata = json.load(f)
                metadata_list.append(metadata)
    
    return metadata_list

def search_images(query=None, topic=None, style=None, tags=None, limit=10):
    """
    搜索图片
    
    Args:
        query: 搜索关键词（在标题、提示词中搜索）
        topic: 文章主题
        style: 文章风格
        tags: 标签列表
        limit: 返回数量限制
    
    Returns:
        list: 匹配的图片元数据列表
    """
    images_dir = os.path.join(os.path.dirname(__file__), 'output', 'images')
    all_metadata = load_all_metadata(images_dir)
    
    results = []
    
    for meta in all_metadata:
        score = 0
        
        # 1. 按关键词搜索
        if query:
            query_lower = query.lower()
            if query_lower in meta.get('prompt', '').lower():
                score += 3
            if query_lower in meta.get('topic', '').lower():
                score += 3
            if query_lower in meta.get('title', '').lower():
                score += 2
            if query_lower in meta.get('section_title', '').lower():
                score += 2
        
        # 2. 按主题搜索
        if topic and topic.lower() in meta.get('topic', '').lower():
            score += 5
        
        # 3. 按风格搜索
        if style and style == meta.get('style', ''):
            score += 3
        
        # 4. 按标签搜索
        if tags:
            meta_tags = meta.get('tags', [])
            matching_tags = set(tags) & set(meta_tags)
            score += len(matching_tags) * 2
        
        # 如果有匹配，添加到结果
        if score > 0:
            meta['score'] = score
            results.append(meta)
    
    # 按分数排序
    results.sort(key=lambda x: x['score'], reverse=True)
    
    return results[:limit]

def show_image_info(metadata):
    """显示图片详细信息"""
    print("\n" + "="*60)
    print(f"🖼️ 图片：{os.path.basename(metadata['filepath'])}")
    print("="*60)
    print(f"📁 路径：{metadata['filepath']}")
    print(f"📐 尺寸：{metadata.get('size', '未知')}")
    print(f"💾 大小：{metadata.get('file_size_kb', '未知')} KB")
    print(f"🏷️ 标签：{', '.join(metadata.get('tags', []))}")
    print(f"🎨 风格：{metadata.get('style', '未知')}")
    print(f"📝 主题：{metadata.get('topic', '未知')}")
    if 'title' in metadata:
        print(f"📰 标题：{metadata['title']}")
    if 'section_title' in metadata:
        print(f"📑 章节：{metadata['section_title']}")
    print(f"🤖 AI 提示词：{metadata.get('use_ai_prompt', False)}")
    print(f"📅 创建时间：{metadata.get('created_at', '未知')}")
    print(f"\n📝 提示词：\n{metadata.get('prompt', '无')}")
    print("="*60)

def list_all_tags():
    """列出所有标签"""
    images_dir = os.path.join(os.path.dirname(__file__), 'output', 'images')
    all_metadata = load_all_metadata(images_dir)
    
    tag_count = {}
    for meta in all_metadata:
        for tag in meta.get('tags', []):
            tag_count[tag] = tag_count.get(tag, 0) + 1
    
    # 按使用次数排序
    sorted_tags = sorted(tag_count.items(), key=lambda x: x[1], reverse=True)
    
    print("\n🏷️ 所有标签（按使用次数排序）：")
    print("="*60)
    for tag, count in sorted_tags[:30]:  # 显示前 30 个
        print(f"{tag:20s} - {count} 次")
    print("="*60)

def export_tags_to_file(output_file):
    """导出标签到文件"""
    images_dir = os.path.join(os.path.dirname(__file__), 'output', 'images')
    all_metadata = load_all_metadata(images_dir)
    
    tag_data = {
        "exported_at": datetime.now().isoformat(),
        "total_images": len(all_metadata),
        "tags": {}
    }
    
    for meta in all_metadata:
        for tag in meta.get('tags', []):
            if tag not in tag_data['tags']:
                tag_data['tags'][tag] = []
            tag_data['tags'][tag].append({
                "filepath": meta['filepath'],
                "prompt": meta.get('prompt', ''),
                "topic": meta.get('topic', ''),
                "style": meta.get('style', '')
            })
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(tag_data, f, ensure_ascii=False, indent=2)
    
    print(f"✅ 标签已导出到：{output_file}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='搜索和复用已生成的图片')
    parser.add_argument('--search', type=str, help='搜索关键词')
    parser.add_argument('--topic', type=str, help='文章主题')
    parser.add_argument('--style', type=str, help='文章风格')
    parser.add_argument('--tags', type=str, nargs='+', help='标签列表')
    parser.add_argument('--limit', type=int, default=10, help='返回数量限制')
    parser.add_argument('--list-tags', action='store_true', help='列出所有标签')
    parser.add_argument('--export', type=str, help='导出标签到文件')
    
    args = parser.parse_args()
    
    if args.list_tags:
        list_all_tags()
    elif args.export:
        export_tags_to_file(args.export)
    else:
        results = search_images(
            query=args.search,
            topic=args.topic,
            style=args.style,
            tags=args.tags,
            limit=args.limit
        )
        
        if not results:
            print("\n❌ 未找到匹配的图片")
        else:
            print(f"\n✅ 找到 {len(results)} 张匹配的图片：\n")
            for i, meta in enumerate(results, 1):
                print(f"{i}. {os.path.basename(meta['filepath'])}")
                print(f"   主题：{meta.get('topic', '无')} | 风格：{meta.get('style', '无')}")
                print(f"   标签：{', '.join(meta.get('tags', []))}")
                print(f"   评分：{meta.get('score', 0)}")
                print()
            
            # 显示第一张的详细信息
            if results:
                show_image_info(results[0])
