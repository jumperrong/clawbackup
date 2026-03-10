#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
publish_draft.py - 发布草稿箱
将文章发布到公众号草稿箱
"""

import argparse
import os
import json
import requests
from datetime import datetime

def load_config():
    config_path = os.path.join(os.path.dirname(__file__), '..', 'config.json')
    with open(config_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def get_access_token(appid, appsecret):
    """获取微信 access_token（带缓存）"""
    cache_file = os.path.join(os.path.dirname(__file__), 'output', 'token_cache.json')
    os.makedirs(os.path.dirname(cache_file), exist_ok=True)
    
    if os.path.exists(cache_file):
        with open(cache_file, 'r') as f:
            cache = json.load(f)
            if datetime.now().timestamp() < cache['expires_at']:
                return cache['token']
    
    url = f"https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid={appid}&secret={appsecret}"
    response = requests.get(url)
    result = response.json()
    
    if 'access_token' not in result:
        raise Exception(f"获取 access_token 失败：{result}")
    
    cache = {
        'token': result['access_token'],
        'expires_at': datetime.now().timestamp() + 7000
    }
    with open(cache_file, 'w') as f:
        json.dump(cache, f)
    
    return result['access_token']

def upload_thumb(access_token, image_path):
    """上传封面图为永久素材"""
    url = f"https://api.weixin.qq.com/cgi-bin/material/add_material?access_token={access_token}&type=image"
    
    files = {'media': open(image_path, 'rb')}
    response = requests.post(url, files=files)
    result = response.json()
    
    if 'media_id' not in result:
        raise Exception(f"上传封面图失败：{result}")
    
    return result['media_id']

def add_draft(access_token, title, html_content, thumb_media_id):
    """创建草稿"""
    url = f"https://api.weixin.qq.com/cgi-bin/draft/add?access_token={access_token}"
    
    payload = {
        "articles": [
            {
                "title": title,
                "author": "AI 助手",
                "digest": title,
                "content": html_content,
                "thumb_media_id": thumb_media_id,
                "show_cover_pic": 1,
                "need_open_comment": 0,
                "only_fans_can_comment": 0
            }
        ]
    }
    
    response = requests.post(url, json=payload)
    result = response.json()
    
    if 'media_id' not in result:
        raise Exception(f"创建草稿失败：{result}")
    
    return result['media_id']

def publish_draft(html_path, cover_image_path, title=None):
    """
    发布文章到草稿箱
    
    Args:
        html_path: HTML 文件路径
        cover_image_path: 封面图路径
        title: 文章标题（可选，默认从文件名提取）
    
    Returns:
        dict: 草稿元数据
    """
    config = load_config()
    
    # 1. 获取 access_token
    access_token = get_access_token(config['wechat_appid'], config['wechat_appsecret'])
    
    # 2. 读取 HTML 内容
    with open(html_path, 'r', encoding='utf-8') as f:
        html_content = f.read()
    
    # 3. 上传封面图
    thumb_media_id = upload_thumb(access_token, cover_image_path)
    print(f"✅ 封面图已上传：{thumb_media_id}")
    
    # 4. 创建草稿
    if title is None:
        title = os.path.basename(html_path).replace('.html', '')
    
    media_id = add_draft(access_token, title, html_content, thumb_media_id)
    
    metadata = {
        "media_id": media_id,
        "title": title,
        "created_at": datetime.now().isoformat()
    }
    
    print(f"✅ 草稿发布成功")
    print(f"📄 标题：{title}")
    print(f"🆔 媒体 ID: {media_id}")
    print(f"🔗 请在公众号后台查看草稿箱")
    
    return metadata

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='发布文章到公众号草稿箱')
    parser.add_argument('--html', type=str, required=True, help='HTML 文件路径')
    parser.add_argument('--cover', type=str, required=True, help='封面图路径')
    parser.add_argument('--title', type=str, help='文章标题')
    
    args = parser.parse_args()
    
    publish_draft(args.html, args.cover, args.title)
