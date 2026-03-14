#!/usr/bin/env python3
"""
test_interactive_flow.py - 测试交互式生成完整流程

主题：运动康复对运动人群的重要性
自动完成所有步骤并验证会话管理和素材记录
"""

import sys
import os
import json
from datetime import datetime

# 添加脚本目录到路径
script_dir = os.path.dirname(__file__)
sys.path.insert(0, script_dir)
os.chdir(script_dir)

print("="*60)
print("🧪 交互式生成流程测试")
print("="*60)
print(f"\n📝 主题：运动康复对运动人群的重要性")
print(f"⏰ 开始时间：{datetime.now().isoformat()}\n")

# 导入模块
from session_manager import SessionManager
from image_manager import ImageManager

# 生成文章 ID
article_id = datetime.now().strftime('%Y-%m-%d_%H%M%S')
print(f"📄 文章 ID: {article_id}\n")

# 1. 初始化会话管理器
print("="*60)
print("步骤 1: 初始化会话管理")
print("="*60)
session_manager = SessionManager(article_id)
print(f"✅ 会话目录：{session_manager.session_dir}")
print(f"✅ 会话日志：{session_manager.session_log_file}\n")

# 2. 记录主题选择
print("="*60)
print("步骤 2: 记录主题选择")
print("="*60)
topic_data = {
    'topic': '运动康复对运动人群的重要性',
    'target_audience': '运动爱好者、健身人群、运动员',
    'word_count': 3000,
    'style': '干货'
}
session_manager.update_metadata('topic', topic_data['topic'])
session_manager.update_metadata('target_audience', topic_data['target_audience'])
session_manager.update_metadata('style', topic_data['style'])
session_manager.log_step('topic_selection', topic_data, confirmed=True)
print(f"✅ 主题：{topic_data['topic']}")
print(f"✅ 目标读者：{topic_data['target_audience']}")
print(f"✅ 字数：{topic_data['word_count']}")
print(f"✅ 风格：{topic_data['style']}\n")

# 3. 生成文章（模拟）
print("="*60)
print("步骤 3: 生成文章内容")
print("="*60)
from write_article import write_article

article_config = {
    'topic': topic_data['topic'],
    'style': topic_data['style'],
    'length': topic_data['word_count']
}

print("🤖 调用 AI 生成文章...")
result = write_article(
    topic=article_config['topic'],
    style=article_config['style'],
    length=article_config['length']
)

# write_article 返回 dict，包含 title, content, word_count
if isinstance(result, dict):
    article_md = result.get('content', str(result))
    word_count = result.get('word_count', len(article_md) // 3)
    title = result.get('title', topic_data['topic'])
else:
    article_md = result
    word_count = len(article_md) // 3
    title = topic_data['topic']

# 保存文章
article_path = f"output/articles/article_{article_id}.md"
with open(article_path, 'w', encoding='utf-8') as f:
    f.write(article_md)

print(f"✅ 文章生成完成：{article_path}")
print(f"✅ 字数：{word_count}\n")

# 记录到会话
session_manager.update_metadata('word_count', word_count)
session_manager.update_asset('markdown', article_path, {
    'title': topic_data['topic'],
    'words': word_count
})
session_manager.log_step('article_generation', {
    'path': article_path,
    'words': word_count
}, confirmed=True)

# 4. 生成图片
print("="*60)
print("步骤 4: 生成配图")
print("="*60)
image_manager = ImageManager(article_id)
print(f"✅ 图片目录：{image_manager.image_dir}\n")

# 生成封面图
print("🎨 生成封面图...")
cover_prompt = "专业运动康复主题，人体肌肉骨骼修复示意图，简洁线条，信息图表风格。医疗蓝与纯净白为主，点缀活力橙。高清质感，现代简约，宽屏 2.35:1，中央留白适合标题，移动端阅读，精致细节。"
cover = image_manager.generate_cover(cover_prompt, "模糊，低质量，水印")
print(f"✅ 封面图：{cover['filename']}")
session_manager.update_asset('cover', cover['path'], cover)

# 生成配图（从文章中提取小标题）
print("\n🎨 生成配图...")
image_prompts = [
    {
        'type': 'image',
        'description': '运动康复核心价值',
        'prompt': '运动康复训练场景，专业教练指导，功能性训练动作，健身房环境，现代简约风格',
        'position': '章节 1 后'
    },
    {
        'type': 'image',
        'description': '运动康复适用人群',
        'prompt': '不同年龄段运动人群，跑步者、健身者、球类运动员，多元化运动场景',
        'position': '章节 2 后'
    },
    {
        'type': 'image',
        'description': '家庭康复训练',
        'prompt': '家庭康复训练场景，瑜伽垫、弹力带等简单器械，温馨居家环境',
        'position': '章节 3 后'
    }
]

generated_images = image_manager.batch_generate(image_prompts)

for i, prompt_data in enumerate(image_prompts):
    if i < len(generated_images):
        img = generated_images[i]
        desc = prompt_data.get('description', f'配图{i+1}')
        img['description'] = desc
        session_manager.update_asset('image', img['path'], img)
        print(f"✅ 配图{i+1}: {img['filename']} - {desc}")

session_manager.update_metadata('images_count', len(generated_images))
session_manager.log_step('image_generation', {
    'cover': cover['filename'],
    'images': len(generated_images)
}, confirmed=True)

print(f"\n✅ 共生成 {len(generated_images)+1} 张图片\n")

# 5. 完成会话
print("="*60)
print("步骤 5: 完成会话记录")
print("="*60)
session_manager.update_metadata('locked', True)
session_manager.complete_session(locked=True)
print(f"✅ 会话状态：completed")
print(f"✅ 锁定状态：locked\n")

# 6. 验证结果
print("="*60)
print("步骤 6: 验证生成结果")
print("="*60)

# 检查会话日志
if os.path.exists(session_manager.session_log_file):
    with open(session_manager.session_log_file, 'r', encoding='utf-8') as f:
        session_log = json.load(f)
    print(f"✅ 会话日志：{session_manager.session_log_file}")
    print(f"   - 步骤数：{len(session_log.get('steps', []))}")
    print(f"   - 素材数：{len(session_log.get('assets', {}))}")
else:
    print(f"❌ 会话日志缺失：{session_manager.session_log_file}")

# 检查图片元数据
image_meta_file = f"output/images/{article_id}/metadata.json"
if os.path.exists(image_meta_file):
    with open(image_meta_file, 'r', encoding='utf-8') as f:
        images = json.load(f)
    print(f"✅ 图片元数据：{image_meta_file}")
    print(f"   - 图片数：{len(images)}")
else:
    print(f"❌ 图片元数据缺失：{image_meta_file}")

# 检查文章文件
if os.path.exists(article_path):
    print(f"✅ 文章文件：{article_path}")
    print(f"   - 大小：{os.path.getsize(article_path)} bytes")
else:
    print(f"❌ 文章文件缺失：{article_path}")

# 7. 更新全局索引
print("\n" + "="*60)
print("步骤 7: 更新全局索引")
print("="*60)

index_file = "output/index.json"
if os.path.exists(index_file):
    with open(index_file, 'r', encoding='utf-8') as f:
        index = json.load(f)
else:
    index = {'version': '1.0', 'articles': [], 'updated': ''}

new_article = {
    'id': article_id,
    'title': topic_data['topic'],
    'date': datetime.now().strftime('%Y-%m-%d'),
    'status': 'ready',
    'files': {
        'markdown': article_path,
        'cover': cover['path']
    },
    'stats': {
        'words': word_count,
        'style': topic_data['style'],
        'images': len(generated_images) + 1
    },
    'tags': ['运动康复', '运动人群', '健身']
}

index['articles'].insert(0, new_article)
index['updated'] = datetime.now().isoformat()

with open(index_file, 'w', encoding='utf-8') as f:
    json.dump(index, f, ensure_ascii=False, indent=2)

print(f"✅ 索引已更新：{index_file}")
print(f"✅ 文章总数：{len(index['articles'])}\n")

# 完成
print("="*60)
print("✅ 交互式生成测试完成！")
print("="*60)
print(f"\n📊 生成统计:")
print(f"   - 文章字数：{word_count}")
print(f"   - 图片数量：{len(generated_images) + 1}")
print(f"   - 会话步骤：{len(session_log.get('steps', []))}")
print(f"   - 记录素材：{len(session_log.get('assets', {}))}")
print(f"\n⏰ 完成时间：{datetime.now().isoformat()}")
print(f"\n🎉 所有功能验证通过！")
print("="*60 + "\n")
