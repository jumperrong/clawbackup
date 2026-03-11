#!/usr/bin/env python3
"""
主题加载器和推荐器
支持从 YAML 配置加载主题，并根据内容关键词智能推荐主题
"""

import os
import yaml
from typing import Dict, List, Optional
from pathlib import Path


class ThemeLoader:
    """主题加载器"""
    
    def __init__(self, themes_dir: Optional[str] = None):
        if themes_dir is None:
            themes_dir = os.path.join(os.path.dirname(__file__), '..', 'themes')
        self.themes_dir = Path(themes_dir)
        self.themes = {}
        self._load_all_themes()
    
    def _load_all_themes(self):
        """加载所有主题配置"""
        # 加载经典主题
        classic_dir = self.themes_dir / 'classic'
        if classic_dir.exists():
            for yaml_file in classic_dir.glob('*.yaml'):
                theme_id = yaml_file.stem
                self.themes[theme_id] = self._load_theme(yaml_file, 'classic')
        
        # 加载马卡龙主题
        macaron_dir = self.themes_dir / 'macaron'
        if macaron_dir.exists():
            for yaml_file in macaron_dir.glob('*.yaml'):
                if yaml_file.stem.startswith('_'):  # 跳过模板文件
                    continue
                theme_id = f"macaron_{yaml_file.stem}"
                self.themes[theme_id] = self._load_theme(yaml_file, 'macaron')
    
    def _load_theme(self, yaml_path: Path, category: str) -> Dict:
        """加载单个主题配置"""
        with open(yaml_path, 'r', encoding='utf-8') as f:
            config = yaml.safe_load(f)
        
        return {
            'id': yaml_path.stem,
            'category': category,
            'name': config.get('name', ''),
            'description': config.get('description', ''),
            'keywords': config.get('keywords', []),
            'colors': config.get('colors', {}),
            'styles': config.get('styles', {})
        }
    
    def get_theme(self, theme_id: str) -> Optional[Dict]:
        """获取指定主题"""
        return self.themes.get(theme_id)
    
    def list_themes(self, category: Optional[str] = None) -> List[Dict]:
        """列出所有主题，可按类别筛选"""
        if category is None:
            return list(self.themes.values())
        return [t for t in self.themes.values() if t['category'] == category]
    
    def recommend_theme(self, keywords: List[str]) -> Optional[str]:
        """
        根据内容关键词推荐主题
        
        Args:
            keywords: 文章关键词列表
            
        Returns:
            推荐的 theme_id
        """
        if not keywords:
            return 'minimal_business'  # 默认主题
        
        # 医疗康复类关键词映射
        MEDICAL_KEYWORDS = [
            '康复', '医疗', '健康', '训练', '治疗', '症状', '疾病',
            '肌肉', '骨骼', '关节', '神经', '运动', '损伤', '疼痛',
            '指南', '方法', '自我', '评估', '拉伸', '锻炼',
            # 具体部位
            '膝盖', '膝关节', '髋关节', '肩关节', '踝关节', '腰椎', '颈椎',
            '大腿', '小腿', '臀部', '髂胫束', '跟腱', '韧带', '半月板',
            # 症状相关
            '疼痛', '酸痛', '刺痛', '麻木', '肿胀', '炎症', '挛缩',
            '综合征', '损伤', '劳损', '扭伤', '拉伤', '磨损',
            # 治疗相关
            '手术', '非手术', '保守治疗', '物理治疗', '按摩', '热敷', '冷敷',
            '康复训练', '功能训练', '核心训练', '拉伸训练'
        ]
        
        scores = {}
        for theme_id, theme in self.themes.items():
            score = 0
            theme_keywords = [k.lower() for k in theme.get('keywords', [])]
            
            # 特殊处理：医疗康复内容优先推荐温暖文艺或自然清新
            has_medical = any(
                any(med_kw in kw for kw in keywords)
                for med_kw in MEDICAL_KEYWORDS
            )
            
            if has_medical:
                if theme_id in ['warm_artistic', 'nature_fresh', 'cozy_lifestyle']:
                    score += 10  # 医疗内容加分
                elif theme_id.startswith('macaron_'):
                    score += 5  # 马卡龙系列也适合
            
            for kw in keywords:
                kw_lower = kw.lower()
                if kw_lower in theme_keywords:
                    score += 2  # 完全匹配
                elif any(kw_lower in tk for tk in theme_keywords):
                    score += 1  # 部分匹配
            
            scores[theme_id] = score
        
        if scores:
            best_theme = max(scores, key=scores.get)
            if scores[best_theme] > 0:
                return best_theme
        
        return 'minimal_business'  # 默认主题


def main():
    """测试主题加载器"""
    loader = ThemeLoader()
    
    print("📚 已加载主题：")
    print(f"  总数：{len(loader.themes)}")
    
    classic = loader.list_themes('classic')
    macaron = loader.list_themes('macaron')
    print(f"  经典主题：{len(classic)}")
    print(f"  马卡龙主题：{len(macaron)}")
    
    # 测试推荐
    test_keywords = ['康复', '训练', '医疗', '健康']
    recommended = loader.recommend_theme(test_keywords)
    print(f"\n🎯 测试推荐:")
    print(f"  关键词：{test_keywords}")
    print(f"  推荐主题：{recommended}")
    
    if recommended:
        theme = loader.get_theme(recommended)
        if theme:
            print(f"  主题名称：{theme['name']}")
            print(f"  描述：{theme['description']}")


if __name__ == '__main__':
    main()
