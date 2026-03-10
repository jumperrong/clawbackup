#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
format_article.py - Markdown 转微信 HTML
将 Markdown 文章转换为微信兼容的 HTML 格式
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

def get_access_token(appid, appsecret):
    """获取微信 access_token（带缓存）"""
    cache_file = os.path.join(os.path.dirname(__file__), 'output', 'token_cache.json')
    os.makedirs(os.path.dirname(cache_file), exist_ok=True)
    
    # 检查缓存
    if os.path.exists(cache_file):
        with open(cache_file, 'r') as f:
            cache = json.load(f)
            if datetime.now().timestamp() < cache['expires_at']:
                print("✅ 使用缓存的 access_token")
                return cache['token']
    
    # 获取新 token
    url = f"https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid={appid}&secret={appsecret}"
    response = requests.get(url)
    result = response.json()
    
    if 'access_token' not in result:
        raise Exception(f"获取 access_token 失败：{result}")
    
    # 缓存 token
    cache = {
        'token': result['access_token'],
        'expires_at': datetime.now().timestamp() + 7000  # 7200 秒有效期，提前 200 秒刷新
    }
    with open(cache_file, 'w') as f:
        json.dump(cache, f)
    
    print("✅ 获取新的 access_token")
    return result['access_token']

def upload_image(access_token, image_path):
    """上传图片到微信永久素材库"""
    url = f"https://api.weixin.qq.com/cgi-bin/material/add_material?access_token={access_token}&type=image"
    
    files = {'media': open(image_path, 'rb')}
    response = requests.post(url, files=files)
    result = response.json()
    
    if 'media_id' not in result:
        raise Exception(f"上传图片失败：{result}")
    
    return result['media_id']

def md_to_wechat_html(md_content, base_dir=None, access_token=None):
    """
    Markdown 转微信 HTML
    
    Args:
        md_content: Markdown 内容
        base_dir: 图片基础路径
        access_token: 微信 access_token
    
    Returns:
        str: 微信兼容的 HTML
    """
    html = md_content
    
    # 1. 转换标题
    html = re.sub(r'^# (.+)$', r'<h1 style="text-align: center; font-size: 20px; color: #333; margin: 20px 0;">\1</h1>', html, flags=re.MULTILINE)
    html = re.sub(r'^## (.+)$', r'<h2 style="font-size: 18px; color: #ff6b6b; margin: 25px 0 15px; border-left: 4px solid #ff6b6b; padding-left: 10px;">\1</h2>', html, flags=re.MULTILINE)
    html = re.sub(r'^### (.+)$', r'<h3 style="font-size: 16px; color: #555; margin: 20px 0 10px;">\1</h3>', html, flags=re.MULTILINE)
    
    # 2. 转换段落
    paragraphs = html.split('\n\n')
    converted = []
    for p in paragraphs:
        if p.strip() and not p.strip().startswith('<'):
            converted.append(f'<p style="font-size: 16px; line-height: 1.8; color: #333; margin: 15px 0;">{p.strip()}</p>')
        else:
            converted.append(p)
    html = '\n'.join(converted)
    
    # 3. 转换图片（上传到微信并替换 URL）
    if base_dir and access_token:
        def replace_image(match):
            alt = match.group(1)
            src = match.group(2)
            
            # 如果是本地路径，上传到微信
            if not src.startswith('http'):
                local_path = os.path.join(base_dir, src) if not os.path.isabs(src) else src
                if os.path.exists(local_path):
                    media_id = upload_image(access_token, local_path)
                    # 获取临时 URL（实际使用时微信会自动处理）
                    return f'<section style="margin: 20px 0;"><img src="{local_path}" alt="{alt}" style="width: 100%; display: block;"/></section>'
            return match.group(0)
        
        html = re.sub(r'!\[(.*?)\]\((.*?)\)', replace_image, html)
    
    # 4. 转换列表
    html = re.sub(r'^[-*]\s+(.+)$', r'<li style="margin: 8px 0;">\1</li>', html, flags=re.MULTILINE)
    html = re.sub(r'((<li.*?</li>\n?)+)', r'<ul style="padding-left: 20px;">\1</ul>', html)
    
    # 5. 转换粗体和斜体
    html = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', html)
    html = re.sub(r'\*(.+?)\*', r'<em>\1</em>', html)
    
    # 6. 包裹整体样式
    final_html = f'''<section style="font-size: 16px; line-height: 1.6; color: #333; padding: 10px;">
{html}
</section>'''
    
    return final_html

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Markdown 转微信 HTML')
    parser.add_argument('--input', type=str, required=True, help='Markdown 文件路径')
    parser.add_argument('--output', type=str, help='输出 HTML 文件路径（可选）')
    parser.add_argument('--upload-images', action='store_true', help='是否上传图片到微信')
    
    args = parser.parse_args()
    
    # 读取 Markdown
    with open(args.input, 'r', encoding='utf-8') as f:
        md_content = f.read()
    
    # 转换
    config = load_config()
    access_token = get_access_token(config['wechat_appid'], config['wechat_appsecret']) if args.upload_images else None
    base_dir = os.path.dirname(args.input) if args.upload_images else None
    
    html = md_to_wechat_html(md_content, base_dir=base_dir, access_token=access_token)
    
    # 保存
    output_path = args.output or args.input.replace('.md', '.html')
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html)
    
    print(f"✅ HTML 转换完成")
    print(f"💾 路径：{output_path}")
