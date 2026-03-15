#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
update_index.py - 自动更新文章索引

扫描 articles/ 目录，自动更新 index.json
支持增量更新（只添加新文章，不删除旧文章）
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
    # 移除 Markdown 标记
    text = re.sub(r'!?\[.*?\]\(.*?\)', '', content)  # 移除图片
    text = re.sub(r'\[.*?\]\(.*?\)', '', text)  # 移除链接
    text = re.sub(r'^#+\s*', '', text, flags=re.MULTILINE)  # 移除标题标记
    text = re.sub(r'\*+', '', text)  # 移除粗体标记
    
    # 中文字数统计
    chinese_chars = len(re.findall(r'[\u4e00-\u9fff]', text))
    # 英文单词数
    english_words = len(re.findall(r'\b[a-zA-Z]+\b', text))
    
    return chinese_chars + english_words


def count_images(content):
    """统计图片数量"""
    return len(re.findall(r'!\[.*?\]\(.*?\)', content))


def scan_articles(articles_dir):
    """扫描文章目录"""
    articles = []
    
    if not os.path.exists(articles_dir):
        print(f"⚠️ 文章目录不存在：{articles_dir}")
        return articles
    
    # 扫描所有 .md 文件
    for md_file in Path(articles_dir).glob("*.md"):
        article_id = md_file.stem.replace('article_', '')
        
        # 读取内容
        with open(md_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 提取元数据
        title = extract_title_from_md(md_file)
        if not title:
            print(f"⚠️ 跳过 {md_file}：无法提取标题")
            continue
        
        # 查找对应的 HTML 文件
        html_files = list(Path(articles_dir).glob(f"{md_file.stem}_*.html"))
        html_path = None
        if html_files:
            # 选择最新的 HTML 文件（按修改时间）
            html_path = max(html_files, key=lambda f: f.stat().st_mtime)
            html_path = f"articles/{html_path.name}"
        
        # 查找封面图
        cover_path = None
        images_dir = os.path.join(os.path.dirname(articles_dir), 'images', article_id)
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
            "status": "ready",
            "files": {
                "markdown": f"articles/{md_file.name}",
                "html": html_path,
                "cover": cover_path
            },
            "stats": {
                "words": word_count,
                "style": "未分类",
                "images": image_count
            },
            "tags": []
        }
        
        articles.append(article_data)
        print(f"✅ 收录文章：{title[:30]}...")
    
    return articles


def update_index(output_dir, incremental=True):
    """
    更新索引文件
    
    Args:
        output_dir: output 目录路径
        incremental: 是否增量更新（保留已有文章）
    """
    index_path = os.path.join(output_dir, 'index.json')
    articles_dir = os.path.join(output_dir, 'articles')
    
    # 加载现有索引
    existing_articles = []
    if os.path.exists(index_path):
        with open(index_path, 'r', encoding='utf-8') as f:
            index_data = json.load(f)
            existing_articles = index_data.get('articles', [])
        print(f"📚 现有索引：{len(existing_articles)} 篇文章")
    
    # 扫描新文章
    new_articles = scan_articles(articles_dir)
    print(f"🔍 扫描到：{len(new_articles)} 篇文章")
    
    # 合并文章（去重）
    if incremental:
        existing_ids = {a['id'] for a in existing_articles}
        for article in new_articles:
            if article['id'] not in existing_ids:
                existing_articles.append(article)
                print(f"✨ 新增文章：{article['title'][:30]}...")
            else:
                print(f"⏭️  跳过已存在：{article['title'][:30]}...")
        final_articles = existing_articles
    else:
        final_articles = new_articles
    
    # 按日期排序（最新的在前）
    final_articles.sort(key=lambda a: a['date'], reverse=True)
    
    # 更新索引文件
    index_data = {
        "version": "1.0",
        "updated": datetime.now().isoformat(),
        "articles": final_articles
    }
    
    with open(index_path, 'w', encoding='utf-8') as f:
        json.dump(index_data, f, ensure_ascii=False, indent=2)
    
    print(f"\n✅ 索引更新完成！")
    print(f"📊 总计：{len(final_articles)} 篇文章")
    print(f"💾 路径：{index_path}")
    
    return index_data


def main():
    """主函数"""
    # 自动查找 output 目录
    script_dir = os.path.dirname(__file__)
    output_dir = os.path.join(script_dir, 'output')
    
    import argparse
    parser = argparse.ArgumentParser(description='更新文章索引')
    parser.add_argument('--full', action='store_true', help='完全重建索引（不保留已有文章）')
    parser.add_argument('--output-dir', type=str, default=output_dir, help='output 目录路径')
    
    args = parser.parse_args()
    
    update_index(args.output_dir, incremental=not args.full)


if __name__ == "__main__":
    main()
