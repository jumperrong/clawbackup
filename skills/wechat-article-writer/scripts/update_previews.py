#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
update_previews.py - 更新草稿文章索引

扫描 previews/ 目录，生成 list.json
用于预览页面显示未锁定的草稿文章
"""

import os
import json
import re
from datetime import datetime
from pathlib import Path


def extract_title_from_md(filepath):
    """从 Markdown 文件提取标题"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            first_line = f.readline().strip()
            if first_line.startswith('# '):
                return first_line[2:].strip()
    except Exception as e:
        print(f"⚠️ 读取 {filepath} 失败：{e}")
    return None


def count_words(content):
    """统计字数"""
    text = re.sub(r'!?\[.*?\]\(.*?\)', '', content)
    text = re.sub(r'\[.*?\]\(.*?\)', '', text)
    text = re.sub(r'^#+\s*', '', text, flags=re.MULTILINE)
    text = re.sub(r'\*+', '', text)
    
    chinese_chars = len(re.findall(r'[\u4e00-\u9fff]', text))
    english_words = len(re.findall(r'\b[a-zA-Z]+\b', text))
    
    return chinese_chars + english_words


def count_images(content):
    """统计图片数量"""
    return len(re.findall(r'!\[.*?\]\(.*?\)', content))


def scan_previews(previews_dir):
    """扫描草稿目录"""
    articles = []
    
    if not os.path.exists(previews_dir):
        print(f"⚠️ 草稿目录不存在：{previews_dir}")
        return articles
    
    # 扫描所有 .md 文件
    for md_file in Path(previews_dir).glob("*.md"):
        article_id = md_file.stem.replace('draft_', '')
        
        # 读取内容
        with open(md_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 提取元数据
        title = extract_title_from_md(md_file)
        if not title:
            print(f"⚠️ 跳过 {md_file}：无法提取标题")
            continue
        
        # 查找封面图
        cover_path = None
        images_dir = os.path.join(os.path.dirname(previews_dir), 'images', article_id)
        if os.path.exists(images_dir):
            cover_files = list(Path(images_dir).glob("cover_*.jpg"))
            if cover_files:
                cover_path = f"images/{article_id}/{cover_files[0].name}"
        
        # 统计信息
        word_count = count_words(content)
        image_count = count_images(content)
        
        # 提取日期
        date_match = re.search(r'(\d{4}-\d{2}-\d{2})', article_id)
        date = date_match.group(1) if date_match else datetime.now().strftime('%Y-%m-%d')
        
        article_data = {
            "id": article_id,
            "title": title,
            "date": date,
            "status": "draft",
            "files": {
                "markdown": f"previews/{md_file.name}",
                "cover": cover_path
            },
            "stats": {
                "words": word_count,
                "style": "草稿",
                "images": image_count
            },
            "tags": []
        }
        
        articles.append(article_data)
        print(f"✅ 收录草稿：{title[:30]}...")
    
    return articles


def update_previews_index(previews_dir):
    """
    更新草稿索引文件
    
    Args:
        previews_dir: previews 目录路径
    """
    list_path = os.path.join(previews_dir, 'list.json')
    
    # 扫描草稿文章
    articles = scan_previews(previews_dir)
    
    # 按日期排序（最新的在前）
    articles.sort(key=lambda a: a['date'], reverse=True)
    
    # 更新索引文件
    index_data = {
        "version": "1.0",
        "updated": datetime.now().isoformat(),
        "articles": articles
    }
    
    with open(list_path, 'w', encoding='utf-8') as f:
        json.dump(index_data, f, ensure_ascii=False, indent=2)
    
    print(f"\n✅ 草稿索引更新完成！")
    print(f"📊 总计：{len(articles)} 篇草稿")
    print(f"💾 路径：{list_path}")
    
    return index_data


def main():
    """主函数"""
    # 自动查找 previews 目录
    script_dir = os.path.dirname(__file__)
    previews_dir = os.path.join(script_dir, 'output', 'previews')
    
    update_previews_index(previews_dir)


if __name__ == "__main__":
    main()
