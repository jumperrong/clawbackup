#!/usr/bin/env python3
"""
封面提示词生成器
根据文章标题和主题自动生成优化的封面图片提示词
"""

from typing import Optional, Dict


class CoverPromptGenerator:
    """封面提示词生成器"""
    
    # 不同主题的视觉风格描述
    THEME_STYLES = {
        'medical': {
            'style': '医疗专业风格',
            'elements': ['简洁', '专业', '可信赖', '清爽'],
            'colors': '绿色、蓝色、白色为主',
            'avoid': '过于花哨、卡通化'
        },
        'tech': {
            'style': '科技感风格',
            'elements': ['现代', '简洁', '未来感'],
            'colors': '蓝色、紫色、深色背景',
            'avoid': '复古、暖色调'
        },
        'warm': {
            'style': '温暖文艺风格',
            'elements': ['温馨', '柔和', '治愈'],
            'colors': '暖黄色、橙色、粉色',
            'avoid': '冷色调、过于严肃'
        },
        'default': {
            'style': '通用专业风格',
            'elements': ['清晰', '醒目', '易读'],
            'colors': '根据内容决定',
            'avoid': '过于复杂'
        }
    }
    
    def __init__(self):
        pass
    
    def generate_prompt(self, title: str, theme: str = 'default', 
                       subtitle: Optional[str] = None) -> Dict:
        """
        生成封面提示词
        
        Args:
            title: 文章标题
            theme: 主题类型 (medical/tech/warm/default)
            subtitle: 副标题（可选）
            
        Returns:
            包含提示词和元数据的字典
        """
        style_info = self.THEME_STYLES.get(theme, self.THEME_STYLES['default'])
        
        # 提取标题关键词
        keywords = self._extract_keywords(title)
        
        # 生成主提示词
        main_prompt = self._build_main_prompt(title, keywords, style_info)
        
        # 生成负面提示词
        negative_prompt = self._build_negative_prompt(style_info)
        
        return {
            'prompt': main_prompt,
            'negative_prompt': negative_prompt,
            'style': style_info['style'],
            'keywords': keywords,
            'dimensions': {
                'header': {'width': 900, 'height': 383},
                'share': {'width': 383, 'height': 383}
            },
            'tags': self._generate_tags(title, theme)
        }
    
    def _extract_keywords(self, title: str) -> list:
        """从标题提取关键词"""
        # 移除标点和表情符号
        import re
        clean_title = re.sub(r'[^\w\s\u4e00-\u9fff]', '', title)
        
        # 简单的关键词提取（按空格和常见分隔符）
        words = clean_title.split()
        
        # 过滤掉太短的词
        keywords = [w for w in words if len(w) >= 2]
        
        return keywords[:5]  # 最多 5 个关键词
    
    def _build_main_prompt(self, title: str, keywords: list, 
                          style_info: Dict) -> str:
        """构建主提示词"""
        prompt_parts = [
            f"微信公众号封面图，{style_info['style']}",
            f"主题元素：{', '.join(style_info['elements'])}",
            f"色调：{style_info['colors']}",
        ]
        
        if keywords:
            prompt_parts.append(f"内容相关：{', '.join(keywords)}")
        
        prompt_parts.extend([
            "构图简洁大气",
            "文字清晰可读",
            "适合 900x383 和 383x383 尺寸",
            "高质量，专业设计"
        ])
        
        return '，'.join(prompt_parts)
    
    def _build_negative_prompt(self, style_info: Dict) -> str:
        """构建负面提示词"""
        negatives = [
            "模糊", "低质量", "水印", "签名",
            "过于复杂", "文字过多", "混乱"
        ]
        
        if style_info.get('avoid'):
            negatives.append(style_info['avoid'])
        
        return '，'.join(negatives)
    
    def _generate_tags(self, title: str, theme: str) -> list:
        """生成图片标签用于复用"""
        import hashlib
        
        # 基于标题生成唯一 ID
        title_hash = hashlib.md5(title.encode('utf-8')).hexdigest()[:8]
        
        tags = [
            f"cover_{theme}",
            f"title_{title_hash}",
            "wechat_article",
            "ai_generated"
        ]
        
        return tags


def main():
    """测试提示词生成器"""
    generator = CoverPromptGenerator()
    
    # 测试用例
    test_title = "臀肌挛缩不用开刀？这份非手术康复指南，90% 的人都不知道！"
    
    print("🎨 封面提示词生成测试\n")
    print(f"📄 标题：{test_title}\n")
    
    for theme in ['medical', 'tech', 'warm', 'default']:
        result = generator.generate_prompt(test_title, theme)
        print(f"━━━ {theme.upper()} 主题 ━━━")
        print(f"提示词：{result['prompt']}")
        print(f"负面：{result['negative_prompt']}")
        print(f"标签：{', '.join(result['tags'])}")
        print(f"尺寸：头条 {result['dimensions']['header']['width']}×{result['dimensions']['header']['height']}, "
              f"分享 {result['dimensions']['share']['width']}×{result['dimensions']['share']['height']}")
        print()


if __name__ == '__main__':
    main()
