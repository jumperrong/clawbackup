#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
manage_article_status.py - 文章状态管理

支持文章状态流转：草稿 → 审核中 → 已锁定 → 已发布
"""

import os
import json
import shutil
from datetime import datetime
from pathlib import Path


class ArticleStatusManager:
    """文章状态管理器"""
    
    # 状态定义
    STATUS_DRAFT = "draft"      # 草稿
    STATUS_REVIEW = "review"    # 审核中
    STATUS_READY = "ready"      # 已锁定
    STATUS_PUBLISHED = "published"  # 已发布
    
    def __init__(self, output_dir):
        """
        初始化
        
        Args:
            output_dir: output 目录路径
        """
        self.output_dir = output_dir
        self.previews_dir = os.path.join(output_dir, 'previews')
        self.articles_dir = os.path.join(output_dir, 'articles')
        self.images_dir = os.path.join(output_dir, 'images')
        self.index_path = os.path.join(output_dir, 'index.json')
        
        # 确保目录存在
        os.makedirs(self.previews_dir, exist_ok=True)
        os.makedirs(self.articles_dir, exist_ok=True)
        os.makedirs(self.images_dir, exist_ok=True)
    
    def get_article_info(self, article_id):
        """获取文章信息"""
        # 先在草稿中查找
        draft_path = os.path.join(self.previews_dir, f"draft_{article_id}.md")
        if os.path.exists(draft_path):
            return {
                "id": article_id,
                "status": self.STATUS_DRAFT,
                "md_path": draft_path,
                "images_dir": os.path.join(self.images_dir, article_id)
            }
        
        # 再在已完成中查找
        article_path = os.path.join(self.articles_dir, f"article_{article_id}.md")
        if os.path.exists(article_path):
            return {
                "id": article_id,
                "status": self.STATUS_READY,
                "md_path": article_path,
                "images_dir": os.path.join(self.images_dir, article_id)
            }
        
        return None
    
    def submit_for_review(self, article_id):
        """
        提交审核（草稿 → 审核中）
        
        Args:
            article_id: 文章 ID
        
        Returns:
            bool: 是否成功
        """
        info = self.get_article_info(article_id)
        if not info:
            print(f"❌ 文章不存在：{article_id}")
            return False
        
        if info["status"] != self.STATUS_DRAFT:
            print(f"⚠️ 文章当前状态不是草稿：{info['status']}")
            return False
        
        # 标记为审核中（暂时只打印日志）
        print(f"✅ 文章 {article_id} 已提交审核")
        return True
    
    def lock_article(self, article_id):
        """
        锁定文章（审核中 → 已锁定）
        
        将文章从 previews/ 移动到 articles/
        
        Args:
            article_id: 文章 ID
        
        Returns:
            bool: 是否成功
        """
        info = self.get_article_info(article_id)
        if not info:
            print(f"❌ 文章不存在：{article_id}")
            return False
        
        if info["status"] == self.STATUS_READY:
            print(f"⚠️ 文章已经是锁定状态")
            return True
        
        # 移动 Markdown 文件
        src_md = info["md_path"]
        dst_md = os.path.join(self.articles_dir, f"article_{article_id}.md")
        
        if os.path.exists(src_md):
            shutil.copy2(src_md, dst_md)
            print(f"📄 移动文章：{src_md} → {dst_md}")
        
        # 移动图片目录
        src_images = info["images_dir"]
        dst_images = os.path.join(self.images_dir, article_id)
        
        if os.path.exists(src_images) and src_images != dst_images:
            if os.path.exists(dst_images):
                shutil.rmtree(dst_images)
            shutil.copytree(src_images, dst_images)
            print(f"🖼️  移动图片：{src_images} → {dst_images}")
        
        # 更新索引
        self._update_index(article_id)
        
        print(f"✅ 文章 {article_id} 已锁定")
        return True
    
    def publish_article(self, article_id, wechat_article_id=None):
        """
        发布文章（已锁定 → 已发布）
        
        Args:
            article_id: 文章 ID
            wechat_article_id: 微信公众号文章 ID（发布后返回）
        
        Returns:
            bool: 是否成功
        """
        info = self.get_article_info(article_id)
        if not info:
            print(f"❌ 文章不存在：{article_id}")
            return False
        
        if info["status"] != self.STATUS_READY:
            print(f"⚠️ 文章未锁定，无法发布：{info['status']}")
            return False
        
        # 更新状态为已发布
        self._update_index(article_id, status=self.STATUS_PUBLISHED, 
                          wechat_id=wechat_article_id)
        
        print(f"✅ 文章 {article_id} 已发布")
        if wechat_article_id:
            print(f"📱 微信公众号文章 ID: {wechat_article_id}")
        
        return True
    
    def _update_index(self, article_id, status=None, wechat_id=None):
        """更新索引文件"""
        # 加载现有索引
        index_data = {"articles": []}
        if os.path.exists(self.index_path):
            with open(self.index_path, 'r', encoding='utf-8') as f:
                index_data = json.load(f)
        
        # 查找并更新文章
        for article in index_data.get("articles", []):
            if article.get("id") == article_id:
                if status:
                    article["status"] = status
                if wechat_id:
                    article["wechat_id"] = wechat_id
                    article["published_at"] = datetime.now().isoformat()
                break
        
        # 保存索引
        index_data["updated"] = datetime.now().isoformat()
        with open(self.index_path, 'w', encoding='utf-8') as f:
            json.dump(index_data, f, ensure_ascii=False, indent=2)
    
    def list_articles(self, status=None):
        """
        列出文章
        
        Args:
            status: 筛选状态（可选）
        
        Returns:
            list: 文章列表
        """
        articles = []
        
        # 加载索引
        if os.path.exists(self.index_path):
            with open(self.index_path, 'r', encoding='utf-8') as f:
                index_data = json.load(f)
                articles = index_data.get("articles", [])
        
        # 筛选
        if status:
            articles = [a for a in articles if a.get("status") == status]
        
        return articles
    
    def show_status(self):
        """显示所有文章状态"""
        articles = self.list_articles()
        
        if not articles:
            print("📭 暂无文章")
            return
        
        print(f"\n{'='*60}")
        print(f"📚 文章状态列表")
        print(f"{'='*60}\n")
        
        status_icons = {
            self.STATUS_DRAFT: "📝",
            self.STATUS_REVIEW: "👀",
            self.STATUS_READY: "🔒",
            self.STATUS_PUBLISHED: "✅"
        }
        
        for article in articles:
            status = article.get("status", "unknown")
            icon = status_icons.get(status, "📄")
            title = article.get("title", "无标题")[:40]
            date = article.get("date", "")
            
            print(f"{icon} [{status.upper():10}] {title} ({date})")
        
        print(f"\n{'='*60}")


def main():
    """主函数"""
    import argparse
    
    script_dir = os.path.dirname(__file__)
    output_dir = os.path.join(script_dir, 'output')
    
    parser = argparse.ArgumentParser(description='文章状态管理')
    parser.add_argument('action', choices=['list', 'lock', 'publish', 'status'],
                       help='操作类型')
    parser.add_argument('--article-id', type=str, help='文章 ID')
    parser.add_argument('--output-dir', type=str, default=output_dir,
                       help='output 目录路径')
    
    args = parser.parse_args()
    
    manager = ArticleStatusManager(args.output_dir)
    
    if args.action == 'list':
        articles = manager.list_articles()
        print(f"📚 共 {len(articles)} 篇文章")
        for a in articles:
            print(f"  - {a.get('title', '无标题')[:50]} [{a.get('status', 'unknown')}]")
    
    elif args.action == 'lock':
        if not args.article_id:
            print("❌ 需要指定 --article-id")
            return
        manager.lock_article(args.article_id)
    
    elif args.action == 'publish':
        if not args.article_id:
            print("❌ 需要指定 --article-id")
            return
        manager.publish_article(args.article_id)
    
    elif args.action == 'status':
        manager.show_status()


if __name__ == "__main__":
    main()
