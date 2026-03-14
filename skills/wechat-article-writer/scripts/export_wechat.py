#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
export_wechat.py - 导出微信公众号格式文章
将 Markdown 文章转换为微信公众号支持的 HTML 格式（样式内联化）
"""

import argparse
import os
import re
import json
from datetime import datetime

# 微信公众号支持的样式（经过验证）
# 参考：微信公众号编辑器实际测试 + 第三方编辑器最佳实践
THEMES = {
    "default": {
        "name": "经典红",
        "h2_border": "#ff6b6b",
        "quote_bg": "#ffe3e3",
        "quote_border": "#ff6b6b",
        "tag_bg": "#ff6b6b",
        "strong_color": "#ff6b6b"
    },
    "medical": {
        "name": "医疗专业",
        "h2_border": "#07c160",
        "quote_bg": "#e8f7f0",
        "quote_border": "#07c160",
        "tag_bg": "#07c160",
        "strong_color": "#07c160"
    },
    "tech": {
        "name": "科技蓝",
        "h2_border": "#1890ff",
        "quote_bg": "#e6f7ff",
        "quote_border": "#1890ff",
        "tag_bg": "#1890ff",
        "strong_color": "#1890ff"
    }
}

def load_markdown(filepath):
    """加载 Markdown 文件"""
    with open(filepath, 'r', encoding='utf-8') as f:
        return f.read()

def markdown_to_html(md_content, theme="default"):
    """
    将 Markdown 转换为微信公众号支持的 HTML（样式内联化）
    微信公众号不支持 CSS 变量，必须内联所有样式
    """
    styles = THEMES.get(theme, THEMES["default"])
    
    lines = md_content.split('\n')
    html_lines = []
    in_list = False
    
    for line in lines:
        # 处理标题
        if line.startswith('## '):
            if in_list:
                html_lines.append('</ul>')
                in_list = False
            title_text = line.replace('## ', '')
            # 微信公众号支持 border-left，必须内联
            html_lines.append(f'<h2 style="font-size: 18px; color: #333; margin: 25px 0 15px; padding-left: 10px; border-left: 4px solid {styles["h2_border"]}; font-weight: 600;">{title_text}</h2>')
        
        elif line.startswith('### '):
            if in_list:
                html_lines.append('</ul>')
                in_list = False
            title_text = line.replace('### ', '')
            html_lines.append(f'<h3 style="font-size: 16px; color: #333; margin: 20px 0 12px; font-weight: 600;">{title_text}</h3>')
        
        # 处理引用块
        elif line.startswith('> '):
            if in_list:
                html_lines.append('</ul>')
                in_list = False
            quote_text = line.replace('> ', '')
            # 微信公众号支持 background 和 border-left
            html_lines.append(f'<blockquote style="background: {styles["quote_bg"]}; border-left: 4px solid {styles["quote_border"]}; padding: 15px 20px; margin: 20px 0; color: #666; font-style: italic; border-radius: 4px;">{quote_text}</blockquote>')
        
        # 处理列表
        elif line.startswith('- ') or line.startswith('* '):
            if not in_list:
                html_lines.append('<ul style="margin: 15px 0; padding-left: 20px;">')
                in_list = True
            list_text = line[2:]
            # 处理列表中的粗体
            list_text = re.sub(r'\*\*(.*?)\*\*', f'<strong style="font-weight: 600; color: {styles["strong_color"]};">\\1</strong>', list_text)
            html_lines.append(f'<li style="margin: 8px 0; line-height: 1.8; color: #333;">{list_text}</li>')
        
        # 处理空行
        elif line.strip() == '':
            if in_list:
                html_lines.append('</ul>')
                in_list = False
            html_lines.append('')
        
        # 处理图片
        elif line.startswith('!['):
            if in_list:
                html_lines.append('</ul>')
                in_list = False
            match = re.match(r'!\[(.*?)\]\((.*?)\)', line)
            if match:
                alt, src = match.groups()
                # 微信公众号图片样式
                html_lines.append(f'<img src="{src}" alt="{alt}" style="max-width: 100%; height: auto; border-radius: 8px; margin: 20px 0; box-shadow: 0 2px 8px rgba(0,0,0,0.1); display: block;">')
        
        # 处理粗体
        elif '**' in line:
            if in_list:
                html_lines.append('</ul>')
                in_list = False
            line = re.sub(r'\*\*(.*?)\*\*', f'<strong style="font-weight: 600; color: {styles["strong_color"]};">\\1</strong>', line)
            html_lines.append(f'<p style="margin: 15px 0; line-height: 1.8; color: #333; text-align: justify;">{line}</p>')
        
        # 普通段落
        else:
            if in_list:
                html_lines.append('</ul>')
                in_list = False
            if line.strip():
                html_lines.append(f'<p style="margin: 15px 0; line-height: 1.8; color: #333; text-align: justify;">{line}</p>')
    
    # 关闭未关闭的列表
    if in_list:
        html_lines.append('</ul>')
    
    return '\n'.join(html_lines)

def export_to_wechat(md_filepath, theme="default", output_dir=None, article_id=None):
    """导出为微信公众号格式"""
    # 加载 Markdown
    md_content = load_markdown(md_filepath)
    
    # 如果有 article_id，加载图片并替换
    if article_id:
        images_dir = os.path.join(os.path.dirname(md_filepath), '..', 'images', article_id)
        metadata_file = os.path.join(images_dir, 'metadata.json')
        
        if os.path.exists(metadata_file):
            with open(metadata_file, 'r', encoding='utf-8') as f:
                images = json.load(f)
            
            print(f"📸 加载到 {len(images)} 张图片...")
            
            # 替换 Markdown 图片标记为 HTML img 标签
            for img in images:
                markdown_img = f"![{img.get('description', '')}]({img['filename']})"
                html_img = f'<img src="{img["path"]}" alt="{img.get("description", "")}" style="max-width: 100%; display: block; margin: 20px auto;"/>'
                md_content = md_content.replace(markdown_img, html_img)
            
            print(f"✅ 图片已嵌入")
    
    # 转换为 HTML（样式内联化）
    html_content = markdown_to_html(md_content, theme)
    
    # 生成输出文件名
    if output_dir is None:
        output_dir = os.path.dirname(md_filepath)
    
    base_name = os.path.splitext(os.path.basename(md_filepath))[0]
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_filename = f"{base_name}_{theme}_wechat_{timestamp}.html"
    output_path = os.path.join(output_dir, output_filename)
    
    # 写入文件
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print(f"✅ 微信公众号格式导出完成")
    print(f"🎨 主题：{THEMES[theme]['name']}")
    print(f"📄 文件：{output_path}")
    print(f"\n📋 使用方法：")
    print(f"1. 打开微信公众号后台 → 新建图文")
    print(f"2. 用浏览器打开上面的 HTML 文件")
    print(f"3. 全选 (Cmd+A) → 复制 (Cmd+C)")
    print(f"4. 在公众号编辑器粘贴 (Cmd+V)")
    print(f"\n✨ 样式已内联化，确保在公众号后台正确显示！")
    
    return output_path

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='导出微信公众号格式文章')
    parser.add_argument('--input', type=str, required=True, help='Markdown 文件路径')
    parser.add_argument('--theme', type=str, default='default',
                       choices=['default', 'medical', 'tech'],
                       help='主题样式')
    parser.add_argument('--output', type=str, default=None, help='输出目录（可选）')
    parser.add_argument('--article-id', type=str, default=None, help='文章 ID（用于加载图片）')
    
    args = parser.parse_args()
    
    export_to_wechat(
        md_filepath=args.input,
        theme=args.theme,
        output_dir=args.output,
        article_id=args.article_id
    )
