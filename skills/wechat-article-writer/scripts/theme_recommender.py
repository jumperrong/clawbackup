#!/usr/bin/env python3
"""
主题推荐器 - 根据文章内容推荐最佳主题
"""

import sys
from pathlib import Path
from typing import List

# 添加脚本目录到路径
sys.path.insert(0, str(Path(__file__).parent))

from theme_loader import ThemeLoader


class ThemeRecommender:
    """主题推荐器"""
    
    def __init__(self):
        self.loader = ThemeLoader()
    
    def extract_keywords(self, text: str, max_keywords: int = 10) -> List[str]:
        """
        从文本中提取关键词
        
        Args:
            text: 文章标题或内容
            max_keywords: 最大关键词数量
            
        Returns:
            关键词列表
        """
        # 简单的关键词提取（可以后续优化为使用 NLP 模型）
        # 中文分词简化版：按字符和常见词组
        
        # 预定义的领域关键词
        domain_keywords = {
            '医疗': ['医疗', '健康', '康复', '训练', '治疗', '症状', '疾病', '运动', '肌肉', '关节', '疼痛', '恢复'],
            '技术': ['技术', '编程', '代码', '开发', 'AI', '人工智能', '算法', '系统', '软件', '工具'],
            '生活': ['生活', '旅行', '美食', '家居', '日常', '习惯', '方式', '体验'],
            '商业': ['商业', '管理', '职场', '公司', '团队', '领导', '策略', '市场'],
            '教育': ['教育', '学习', '教程', '指南', '知识', '技能', '培训'],
            '情感': ['情感', '心理', '情绪', '关系', '成长', '感悟', '思考'],
        }
        
        # 统计匹配
        scores = {}
        for domain, keywords in domain_keywords.items():
            score = sum(1 for kw in keywords if kw in text)
            if score > 0:
                scores[domain] = score
        
        # 返回得分最高的领域的关键词
        if scores:
            best_domain = max(scores, key=scores.get)
            return domain_keywords[best_domain][:max_keywords]
        
        # 如果没有匹配，返回空列表
        return []
    
    def recommend(self, title: str, content: str = "") -> dict:
        """
        推荐主题
        
        Args:
            title: 文章标题
            content: 文章内容（可选）
            
        Returns:
            {
                'theme_id': str,
                'theme_name': str,
                'category': str,
                'confidence': float,
                'matched_keywords': list
            }
        """
        # 提取关键词
        text = title + " " + content
        keywords = self.extract_keywords(text)
        
        # 使用加载器的推荐功能
        theme_id = self.loader.recommend_theme(keywords)
        theme_info = self.loader.get_theme(theme_id)
        
        if not theme_info:
            theme_id = 'tech_modern'
            theme_info = self.loader.get_theme(theme_id)
        
        # 计算置信度
        theme_keywords = theme_info.get('keywords', [])
        matched = [kw for kw in keywords if kw in theme_keywords]
        confidence = len(matched) / len(keywords) if keywords else 0.5
        
        return {
            'theme_id': theme_id,
            'theme_name': theme_info.get('name', theme_id),
            'category': 'macaron' if theme_id.startswith('macaron_') else 'classic',
            'confidence': confidence,
            'matched_keywords': matched,
            'all_keywords': keywords
        }
    
    def print_recommendation(self, title: str, content: str = ""):
        """打印推荐结果"""
        result = self.recommend(title, content)
        
        print("\n" + "=" * 60)
        print("🎯 主题推荐结果")
        print("=" * 60)
        print(f"文章标题：{title}")
        print(f"提取关键词：{', '.join(result['all_keywords']) or '无'}")
        print(f"\n✅ 推荐主题：{result['theme_name']} ({result['theme_id']})")
        print(f"主题类别：{result['category']}")
        print(f"匹配度：{result['confidence']:.0%}")
        print(f"匹配关键词：{', '.join(result['matched_keywords']) or '基于领域推断'}")
        print("=" * 60)


def main():
    """测试推荐器"""
    recommender = ThemeRecommender()
    
    # 测试用例
    test_cases = [
        ("臀肌挛缩不用开刀？这份非手术康复指南，90% 的人都不知道！", ""),
        ("一拉就痛？膝盖外侧'筋'绷紧了！髂胫束综合征自救全攻略", ""),
        ("AI 发展趋势 2026：这 5 个技术将改变世界", ""),
        ("Python 入门教程：从零开始学编程", ""),
        ("周末去哪儿？上海最值得去的 10 个地方", ""),
    ]
    
    for title, content in test_cases:
        recommender.print_recommendation(title, content)
        print()


if __name__ == '__main__':
    main()
