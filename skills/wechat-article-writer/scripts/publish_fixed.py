#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
发布文章到微信公众号草稿箱（修复版）
"""

import requests
import json
import markdown
import re

def load_config():
    with open('config.json', 'r', encoding='utf-8') as f:
        return json.load(f)

def get_access_token():
    config = load_config()
    appid = config['wechat_appid']
    appsecret = config['wechat_appsecret']
    
    url = f'https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid={appid}&secret={appsecret}'
    response = requests.get(url, timeout=10)
    data = response.json()
    
    if 'access_token' in data:
        return data['access_token']
    else:
        raise Exception(f"获取 access_token 失败：{data}")

def main():
    print('='*60)
    print('🚀 发布文章到微信公众号草稿箱')
    print('='*60)
    print()
    
    # 获取 token
    token = get_access_token()
    print('✅ Access Token 获取成功')
    
    # 读取封面 media_id
    with open('wechat_cover_media_id.txt', 'r') as f:
        thumb_media_id = f.read().strip()
    print(f'✅ 封面图 media_id: {thumb_media_id[:30]}...')
    
    # 读取文章
    article_path = 'scripts/output/articles/article_20260310_154351.md'
    with open(article_path, 'r', encoding='utf-8') as f:
        md_content = f.read()
    print(f'✅ 文章读取成功')
    
    # 提取标题
    title_match = re.search(r'^# (.*?)$', md_content, re.MULTILINE)
    title = title_match.group(1) if title_match else '未命名文章'
    print(f'📝 标题：{title}')
    
    # 转换 HTML
    html_content = markdown.markdown(md_content, extensions=['extra', 'codehilite'])
    
    # 去掉 h1 标题（微信会自动添加）
    html_content = re.sub(r'<h1>.*?</h1>', '', html_content)
    
    # 去掉可能的代码高亮（微信不支持）
    html_content = re.sub(r'<pre class="codehilite">.*?</pre>', '', html_content, flags=re.DOTALL)
    
    # 简化图片标签，去掉 alt 属性中的特殊字符
    html_content = re.sub(r'<img alt=".*?" src="(.*?)" />', r'<img src="\1" />', html_content)
    
    # 添加微信样式
    html_content = f'''
<section style="font-size: 16px; line-height: 1.8; color: #333; font-family: -apple-system, BlinkMacSystemFont, 'Helvetica Neue', 'PingFang SC', 'Hiragino Sans GB', 'Microsoft YaHei', Arial, sans-serif;">
{html_content}
</section>
'''
    
    print(f'📊 内容长度：{len(html_content)} 字符')
    print()
    
    # 发布
    draft_url = f'https://api.weixin.qq.com/cgi-bin/draft/add?access_token={token}'
    
    data = {
        'articles': [{
            'title': title,
            'author': 'AI 助手',
            'digest': title[:50] + '...' if len(title) > 50 else title,
            'content': html_content,
            'thumb_media_id': thumb_media_id,
            'show_cover_pic': 1
        }]
    }
    
    print('📤 发布中...')
    # 使用 data 参数而不是 json 参数，避免 ensure_ascii=True
    response = requests.post(
        draft_url,
        data=json.dumps(data, ensure_ascii=False).encode('utf-8'),
        headers={'Content-Type': 'application/json; charset=utf-8'},
        timeout=30
    )
    result = response.json()
    
    print()
    print('='*60)
    print('📤 发布结果')
    print('='*60)
    print()
    
    if result.get('errcode') == 0:
        print('✅ 发布成功！')
        print(f'   草稿 ID: {result.get("media_id")}')
        print()
        print('📱 可以在微信公众号后台查看草稿')
        print('🔗 预览链接：https://mp.weixin.qq.com')
    else:
        print('❌ 发布失败')
        print(f'   错误码：{result.get("errcode", "未知")}')
        print(f'   错误信息：{result.get("errmsg", "未知")}')
        print()
        print('💡 调试信息:')
        print(f'   标题长度：{len(title)}')
        print(f'   内容长度：{len(html_content)}')

if __name__ == "__main__":
    main()
