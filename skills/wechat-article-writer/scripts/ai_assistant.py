#!/usr/bin/env python3
"""
自然语言指令接口
用户只需用自然语言描述需求，自动执行相应功能
"""

import sys
import os
import re
from pathlib import Path

# 添加脚本目录到路径
script_dir = os.path.dirname(__file__)
sys.path.insert(0, script_dir)

from theme_loader import ThemeLoader
from cover_prompt_generator import CoverPromptGenerator
from content_validator import ContentValidator
from config_loader import get_config


class NaturalLanguageInterface:
    """自然语言指令接口"""
    
    def __init__(self):
        self.theme_loader = ThemeLoader()
        self.cover_generator = CoverPromptGenerator()
        self.validator = ContentValidator()
        self.config = get_config()
    
    def parse_command(self, user_input: str) -> dict:
        """
        解析用户自然语言输入
        
        Args:
            user_input: 用户的自然语言描述
            
        Returns:
            包含操作类型和参数的字典
        """
        user_input = user_input.lower().strip()
        
        # 分析文章/推荐主题
        if any(kw in user_input for kw in ['分析', '推荐主题', '看看适合什么主题', '什么主题合适']):
            return {
                'action': 'analyze',
                'title': self._extract_title(user_input),
                'content_file': self._extract_file(user_input)
            }
        
        # 生成封面提示词
        if any(kw in user_input for kw in ['封面', '生成图片', '画图', '提示词']):
            return {
                'action': 'generate_cover',
                'title': self._extract_title(user_input),
                'style': self._extract_style(user_input)
            }
        
        # 查看主题列表
        if any(kw in user_input for kw in ['有哪些主题', '主题列表', '全部主题', '主题大全']):
            return {
                'action': 'list_themes',
                'category': self._extract_category(user_input)
            }
        
        # 检查配置
        if any(kw in user_input for kw in ['配置', 'api key', '检查配置', '配置状态']):
            return {
                'action': 'check_config'
            }
        
        # 验证内容
        if any(kw in user_input for kw in ['验证', '检查事实', '内容验证']):
            return {
                'action': 'validate',
                'content_file': self._extract_file(user_input)
            }
        
        # 预览文章
        if any(kw in user_input for kw in ['预览', '查看', '打开预览']):
            return {
                'action': 'preview'
            }
        
        # 交互模式
        if any(kw in user_input for kw in ['交互', '逐步', '一步步', '分步', '审核']):
            return {
                'action': 'interactive'
            }
        
        # 帮助
        if any(kw in user_input for kw in ['帮助', '怎么用', '如何使用', 'help']):
            return {
                'action': 'help'
            }
        
        # 默认：分析文章
        if user_input:
            return {
                'action': 'analyze',
                'title': user_input,
                'content_file': None
            }
        
        return {'action': 'help'}
    
    def _extract_title(self, text: str) -> str:
        """从文本提取文章标题"""
        # 尝试提取引号中的内容
        match = re.search(r'[""](.+?)[""]', text)
        if match:
            return match.group(1)
        
        # 否则返回去掉指令词后的内容
        for kw in ['分析', '推荐主题', '看看适合什么主题', '什么主题合适', '帮我', '给我']:
            text = text.replace(kw, '')
        return text.strip()
    
    def _extract_file(self, text: str) -> str:
        """从文本提取文件路径"""
        match = re.search(r'([\w./-]+\.md)', text)
        if match:
            return match.group(1)
        return None
    
    def _extract_style(self, text: str) -> str:
        """从文本提取封面风格"""
        if any(kw in text for kw in ['医疗', '康复', '健康']):
            return 'medical'
        elif any(kw in text for kw in ['科技', 'ai', '数码']):
            return 'tech'
        elif any(kw in text for kw in ['温暖', '文艺', '温馨']):
            return 'warm'
        return 'default'
    
    def _extract_category(self, text: str) -> str:
        """从文本提取主题类别"""
        if any(kw in text for kw in ['经典', '传统']):
            return 'classic'
        elif any(kw in text for kw in ['马卡龙', '可爱', '彩色']):
            return 'macaron'
        return None
    
    def execute(self, command: dict):
        """执行解析后的命令"""
        action = command.get('action')
        
        if action == 'analyze':
            self._analyze_article(command.get('title', ''), command.get('content_file'))
        
        elif action == 'generate_cover':
            self._generate_cover(command.get('title', ''), command.get('style', 'default'))
        
        elif action == 'list_themes':
            self._list_themes(command.get('category'))
        
        elif action == 'check_config':
            self._check_config()
        
        elif action == 'validate':
            self._validate_content(command.get('content_file'))
        
        elif action == 'preview':
            self._preview()
        
        elif action == 'interactive':
            self._start_interactive()
        
        elif action == 'help':
            self._show_help()
    
    def _analyze_article(self, title: str, content_file: str = None):
        """分析文章并推荐主题"""
        from enhanced_workflow import analyze_article_topic, extract_keywords
        
        print("\n" + "="*60)
        print("📊 文章分析报告")
        print("="*60)
        
        # 读取内容（如果有）
        content = ""
        if content_file and os.path.exists(content_file):
            with open(content_file, 'r', encoding='utf-8') as f:
                content = f.read()
        
        # 分析
        result = analyze_article_topic(title, content)
        
        # 显示关键词
        print(f"\n🏷️  关键词:")
        for i, kw in enumerate(result['keywords'][:5], 1):
            print(f"   {i}. {kw}")
        
        # 显示推荐主题
        theme = result['recommended_theme']
        print(f"\n🎨 推荐主题:")
        print(f"   ID: {theme['id']}")
        print(f"   名称：{theme['name']}")
        print(f"   分类：{theme['category']}")
        print(f"   描述：{theme['description']}")
        
        # 显示封面提示词
        cover = result['cover_prompt']
        print(f"\n🖼️  封面提示词:")
        print(f"   风格：{cover['style']}")
        print(f"   提示词：{cover['prompt'][:100]}...")
        print(f"   标签：{', '.join(cover['tags'])}")
        
        # 显示验证信息
        if result.get('verification_results'):
            print(f"\n✅ 内容验证:")
            for vr in result['verification_results'][:3]:
                status = "✅" if vr['verified'] else ("❌" if vr['verified'] == False else "⚠️")
                print(f"   {status} {vr['fact']}")
        elif result['verification_needed']:
            print(f"\n⚠️  需要验证的内容:")
            for fact in result['facts_to_verify'][:3]:
                print(f"   - {fact['text']} ({fact['type']})")
        else:
            print(f"\n✅ 无需特别验证")
        
        print("\n" + "="*60)
        print("💡 提示：说\"生成封面\"可以自动生成分封面提示词")
        print("="*60 + "\n")
    
    def _generate_cover(self, title: str, style: str):
        """生成封面提示词"""
        print("\n" + "="*60)
        print("🖼️  封面提示词生成")
        print("="*60)
        
        result = self.cover_generator.generate_prompt(title, style)
        
        print(f"\n📝 主提示词:")
        print(f"   {result['prompt']}")
        
        print(f"\n🚫 负面提示词:")
        print(f"   {result['negative_prompt']}")
        
        print(f"\n🏷️  图片标签:")
        print(f"   {', '.join(result['tags'])}")
        
        print(f"\n📐 尺寸:")
        print(f"   头条封面：{result['dimensions']['header']['width']}×{result['dimensions']['header']['height']}")
        print(f"   分享封面：{result['dimensions']['share']['width']}×{result['dimensions']['share']['height']}")
        
        print("\n" + "="*60)
        print("💡 提示：将提示词复制到豆包 AI 即可生成封面")
        print("="*60 + "\n")
    
    def _list_themes(self, category: str = None):
        """显示主题列表"""
        print("\n" + "="*60)
        print("🎨 主题列表")
        print("="*60)
        
        themes = self.theme_loader.list_themes(category)
        
        if category == 'classic' or category is None:
            print("\n📚 经典主题:")
            for theme in [t for t in themes if t['category'] == 'classic']:
                print(f"   • {theme['id']:25} - {theme['name']} ({theme['description'][:20]}...)")
        
        if category == 'macaron' or category is None:
            print("\n🍬 马卡龙主题:")
            for theme in [t for t in themes if t['category'] == 'macaron']:
                print(f"   • {theme['id']:25} - {theme['name']}")
        
        print("\n" + "="*60)
        print("💡 提示：说\"分析文章：xxx\"可以获取主题推荐")
        print("="*60 + "\n")
    
    def _check_config(self):
        """检查配置状态"""
        from config_loader import check_api_keys
        
        print("\n" + "="*60)
        print("🔧 配置检查")
        print("="*60)
        
        api_status = check_api_keys()
        
        print("\n📋 API Key 状态:")
        for name, status in api_status.items():
            icon = "✅" if status else "❌"
            print(f"  {icon} {name}: {'已配置' if status else '未配置'}")
        
        print("\n" + "="*60)
        if all(api_status.values()):
            print("✅ 所有配置正常！")
        else:
            print("⚠️  部分配置缺失，请检查 config.json 或环境变量")
        print("="*60 + "\n")
    
    def _validate_content(self, content_file: str):
        """验证内容"""
        print("\n" + "="*60)
        print("✅ 内容验证")
        print("="*60)
        
        if not content_file or not os.path.exists(content_file):
            print("❌ 请提供文章内容文件路径")
            return
        
        with open(content_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        facts = self.validator.identify_facts_to_verify(content)
        
        if not facts:
            print("\n✅ 未发现需要验证的内容")
        else:
            print(f"\n⚠️  发现 {len(facts)} 个需要验证的事实:")
            for fact in facts[:5]:
                print(f"   - {fact['text']} ({fact['type']})")
            
            # 如果有 Tavily，自动验证
            if self.config.is_configured('tavily_api_key'):
                try:
                    from tavily import TavilyClient
                    client = TavilyClient(api_key=self.config.get('tavily_api_key'))
                    
                    print("\n🔍 正在验证...")
                    for fact in facts[:3]:
                        response = client.search(fact['text'], max_results=2)
                        results = response.get('results', [])
                        print(f"   {'✅' if results else '❌'} {fact['text']}")
                        for r in results[:2]:
                            print(f"      来源：{r.get('url')}")
                except:
                    pass
        
        print("\n" + "="*60 + "\n")
    
    def _preview(self):
        """打开预览页面"""
        import subprocess
        
        preview_file = os.path.join(script_dir, '..', 'preview_enhanced.html')
        if os.path.exists(preview_file):
            subprocess.run(['open', preview_file])
            print("\n✅ 预览页面已打开")
        else:
            print("\n❌ 预览页面不存在")
        print()
    
    def _start_interactive(self):
        """启动交互式写作"""
        print("\n" + "="*60)
        print("📝 启动交互式写作模式")
        print("="*60)
        print("\n交互式写作模式将帮你:")
        print("   1. 逐步确定主题和标题")
        print("   2. 生成并修改大纲")
        print("   3. 分步生成正文内容")
        print("   4. 生成和调整配图提示词")
        print("   5. 选择排版主题")
        print("   6. 预览和导出文章")
        print("\n每一步都可以修改和调整，确保文章符合你的要求。\n")
        
        from interactive_writer import InteractiveWriter
        writer = InteractiveWriter()
        writer.start()
    
    def _show_help(self):
        """显示帮助信息"""
        print("\n" + "="*60)
        print("📖 自然语言指令集")
        print("="*60)
        
        print("""
你可以用自然语言描述需求，例如：

📊 分析文章
   • "分析这篇文章：臀肌挛缩康复指南"
   • "推荐适合的主题"
   • "看看这篇文章适合什么主题"

🖼️  生成封面
   • "生成封面提示词：康复训练指南"
   • "帮我生成医疗风格的封面"
   • "画图：AI 发展趋势"

🎨 查看主题
   • "有哪些主题？"
   • "显示全部主题"
   • "只看马卡龙主题"

✅ 内容验证
   • "验证这篇文章的内容"
   • "检查事实准确性"

🔧 配置检查
   • "检查配置状态"
   • "API Key 都配置好了吗？"

📱 预览
   • "打开预览页面"
   • "预览文章"

📝 交互模式
   • "交互式写作"
   • "一步步生成文章"
   • "我要逐步审核文章和配图"

💡 帮助
   • "帮助"
   • "怎么用？"
   • "有哪些功能？"

---
提示：直接说文章标题也会自动分析
例如："臀肌挛缩不用开刀？这份康复指南"
""")
        
        print("="*60 + "\n")


def main():
    """主函数"""
    interface = NaturalLanguageInterface()
    
    if len(sys.argv) < 2:
        interface._show_help()
        return
    
    # 组合所有参数作为用户输入
    user_input = ' '.join(sys.argv[1:])
    
    # 解析并执行
    command = interface.parse_command(user_input)
    interface.execute(command)


if __name__ == '__main__':
    main()
