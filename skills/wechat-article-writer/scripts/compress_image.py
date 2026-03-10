#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
compress_image.py - 图片压缩优化
压缩图片符合微信要求（封面图<64KB）
"""

import argparse
import os
from PIL import Image

def compress_image(input_path, output_path=None, target_size=(900, 500), quality=85):
    """
    压缩图片
    
    Args:
        input_path: 输入图片路径
        output_path: 输出路径（可选，默认覆盖原文件）
        target_size: 目标尺寸 (宽，高)
        quality: JPEG 质量 (1-100)
    
    Returns:
        dict: 压缩后的元数据
    """
    # 1. 打开图片
    img = Image.open(input_path)
    
    # 2. 转换为 RGB（处理 PNG 等格式）
    if img.mode in ('RGBA', 'LA', 'P'):
        img = img.convert('RGB')
    
    # 3. 裁剪到目标比例（公众号封面 2.35:1）
    target_ratio = target_size[0] / target_size[1]
    current_ratio = img.width / img.height
    
    if current_ratio > target_ratio:
        # 图片太宽，裁剪宽度
        new_width = int(img.height * target_ratio)
        left = (img.width - new_width) // 2
        img = img.crop((left, 0, left + new_width, img.height))
    else:
        # 图片太高，裁剪高度
        new_height = int(img.width / target_ratio)
        top = (img.height - new_height) // 2
        img = img.crop((0, top, img.width, top + new_height))
    
    # 4. 缩放
    img = img.resize(target_size, Image.Resampling.LANCZOS)
    
    # 5. 保存
    if output_path is None:
        output_path = input_path
    
    img.save(output_path, 'JPEG', quality=quality, optimize=True, progressive=True)
    
    # 6. 检查文件大小
    file_size = os.path.getsize(output_path) / 1024  # KB
    
    metadata = {
        "filepath": output_path,
        "size": f"{img.width}x{img.height}",
        "file_size_kb": round(file_size, 2),
        "quality": quality
    }
    
    print(f"✅ 图片压缩完成")
    print(f"📐 尺寸：{img.width}x{img.height}")
    print(f"💾 大小：{file_size:.2f} KB")
    
    return metadata

def compress_all_images_in_folder(folder_path, target_size=(900, 500), quality=85):
    """压缩文件夹中的所有图片"""
    for filename in os.listdir(folder_path):
        if filename.lower().endswith(('.jpg', '.jpeg', '.png')):
            filepath = os.path.join(folder_path, filename)
            print(f"\n处理：{filename}")
            compress_image(filepath, target_size=target_size, quality=quality)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='压缩图片符合微信要求')
    parser.add_argument('--input', type=str, required=True, help='输入图片路径或文件夹')
    parser.add_argument('--width', type=int, default=900, help='目标宽度')
    parser.add_argument('--height', type=int, default=500, help='目标高度')
    parser.add_argument('--quality', type=int, default=85, help='JPEG 质量 (1-100)')
    
    args = parser.parse_args()
    
    if os.path.isdir(args.input):
        compress_all_images_in_folder(
            args.input,
            target_size=(args.width, args.height),
            quality=args.quality
        )
    else:
        compress_image(
            args.input,
            target_size=(args.width, args.height),
            quality=args.quality
        )
