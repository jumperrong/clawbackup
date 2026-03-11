#!/usr/bin/env python3
"""
增强版工作流程脚本
整合主题推荐、内容验证、封面优化功能
"""

import sys
import os
import json
from pathlib import Path

# 添加脚本目录到路径
script_dir = os.path.dirname(__file__)
sys.path.insert(0, script_dir)

from theme_loader import ThemeLoader
from cover_prompt_generator import CoverPromptGenerator
from content_validator import ContentValidator


def analyze_article_topic(title: str, content: str = "") -> dict:
    """
    分析文章主题并推荐配置
    
    Args:
        title: 文章标题
        content: 文章内容（可选）
        
    Returns:
        包含推荐主题、关键词、验证建议的字典
    """
    # 初始化组件
    theme_loader = ThemeLoader()
    cover_generator = CoverPromptGenerator()
    validator = ContentValidator()
    
    # 1. 提取关键词
    keywords = extract_keywords(title, content)
    
    # 2. 推荐主题
    recommended_theme = theme_loader.recommend_theme(keywords)
    theme_info = theme_loader.get_theme(recommended_theme)
    
    # 3. 生成封面提示词
    # 根据推荐主题判断封面风格
    theme_category = theme_info['category'] if theme_info else 'classic'
    theme_id = recommended_theme
    
    if theme_id.startswith('macaron_'):
        cover_theme = 'warm'  # 马卡龙系列用温暖风格
    elif any(kw in keywords for kw in ['康复', '医疗', '健康', '训练']):
        cover_theme = 'medical'
    elif theme_id in ['tech_modern', 'geek_tech', 'data_analytics']:
        cover_theme = 'tech'
    else:
        cover_theme = 'default'
    
    cover_prompt = cover_generator.generate_prompt(title, cover_theme)
    
    # 4. 识别需要验证的内容
    facts_to_verify = validator.identify_facts_to_verify(content) if content else []
    
    return {
        'keywords': keywords,
        'recommended_theme': {
            'id': recommended_theme,
            'name': theme_info['name'] if theme_info else recommended_theme,
            'description': theme_info['description'] if theme_info else '',
            'category': theme_info['category'] if theme_info else 'classic'
        },
        'cover_prompt': cover_prompt,
        'facts_to_verify': facts_to_verify,
        'verification_needed': len(facts_to_verify) > 0
    }


def extract_keywords(title: str, content: str = "") -> list:
    """从标题和内容提取关键词"""
    import re
    
    words = []
    
    # 医疗康复类核心词（用于从长句中提取）
    CORE_MEDICAL = [
        '康复', '训练', '治疗', '症状', '肌肉', '骨骼', '关节',
        '神经', '运动', '损伤', '疼痛', '拉伸', '锻炼', '髂胫束',
        '臀肌', '挛缩', '膝盖', '综合征', '指南', '方法', '康复训练',
        '自我', '评估', '放松', '按摩', '热敷', '冷敷'
    ]
    
    # 从标题提取
    title_words = re.findall(r'[\u4e00-\u9fa5]{2,}', title)
    words.extend(title_words)
    
    # 额外：从标题提取核心医疗词（即使被包含在长词中）
    for med in CORE_MEDICAL:
        if med in title:
            words.append(med)
    
    # 从内容提取（前 2000 字）
    if content:
        content_words = re.findall(r'[\u4e00-\u9fa5]{2,}', content[:2000])
        words.extend(content_words)
        
        # 额外：从内容提取核心医疗词
        for med in CORE_MEDICAL:
            if med in content:
                words.append(med)
    
    # 去重并排序（医疗相关词排前面）
    seen = set()
    medical_words = []
    other_words = []
    
    for w in words:
        if w not in seen and len(w) >= 2:
            seen.add(w)
            if any(med in w for med in CORE_MEDICAL) or w in CORE_MEDICAL:
                medical_words.append(w)
            else:
                other_words.append(w)
    
    # 医疗词优先，最多 10 个
    result = medical_words + other_words
    return result[:10]


def print_analysis(result: dict):
    """打印分析结果"""
    print("\n" + "=" * 60)
    print("📊 文章分析报告")
    print("=" * 60)
    
    print(f"\n🏷️  关键词:")
    for i, kw in enumerate(result['keywords'], 1):
        print(f"   {i}. {kw}")
    
    print(f"\n🎨 推荐主题:")
    theme = result['recommended_theme']
    print(f"   ID: {theme['id']}")
    print(f"   名称：{theme['name']}")
    print(f"   分类：{theme['category']}")
    print(f"   描述：{theme['description']}")
    
    print(f"\n🖼️  封面提示词:")
    cover = result['cover_prompt']
    print(f"   风格：{cover['style']}")
    print(f"   提示词：{cover['prompt'][:100]}...")
    print(f"   标签：{', '.join(cover['tags'])}")
    print(f"   尺寸：头条 {cover['dimensions']['header']['width']}×{cover['dimensions']['header']['height']}, "
          f"分享 {cover['dimensions']['share']['width']}×{cover['dimensions']['share']['height']}")
    
    if result['verification_needed']:
        print(f"\n⚠️  需要验证的内容:")
        for fact in result['facts_to_verify'][:5]:
            print(f"   - {fact['text']} ({fact['type']})")
        if len(result['facts_to_verify']) > 5:
            print(f"   ... 还有 {len(result['facts_to_verify']) - 5} 项")
    else:
        print(f"\n✅ 无需特别验证的内容")
    
    print("\n" + "=" * 60)


def main():
    """主函数"""
    if len(sys.argv) < 2:
        print("用法：python enhanced_workflow.py <文章标题> [文章内容文件]")
        print("\n示例:")
        print("  python enhanced_workflow.py \"臀肌挛缩康复指南\"")
        print("  python enhanced_workflow.py \"髂胫束综合症\" article.md")
        sys.exit(1)
    
    title = sys.argv[1]
    content = ""
    
    # 如果有内容文件，读取它
    if len(sys.argv) >= 3:
        content_file = sys.argv[2]
        if os.path.exists(content_file):
            with open(content_file, 'r', encoding='utf-8') as f:
                content = f.read()
    
    # 分析文章
    result = analyze_article_topic(title, content)
    
    # 打印结果
    print_analysis(result)
    
    # 保存结果到 JSON
    output_file = os.path.join(script_dir, 'output', 'analysis_result.json')
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
    
    print(f"\n💾 分析结果已保存到：{output_file}")


if __name__ == '__main__':
    main()
