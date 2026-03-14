#!/usr/bin/env python3
"""
交互式写作模式
支持分步生成、逐步审核、多轮对话调整
"""

import sys
import os
import json
from pathlib import Path
from datetime import datetime

# 添加脚本目录到路径
script_dir = os.path.dirname(__file__)
sys.path.insert(0, script_dir)

from config_loader import get_config
from session_manager import SessionManager
from image_manager import ImageManager
from prompt_optimizer import PromptOptimizer


class InteractiveWriter:
    """交互式写作助手"""
    
    def __init__(self):
        self.config = get_config()
        self.article_id = None
        self.session_manager = None
        self.image_manager = None
        self.session = {
            'title': '',
            'topic': '',
            'style': '',
            'outline': [],
            'content': '',
            'images': [],
            'theme': 'warm_artistic'
        }
        self.locked = False
    
    def start(self):
        """开始交互式写作"""
        print("\n" + "="*60)
        print("📝 微信公众号交互式写作")
        print("="*60)
        print("\n欢迎使用交互式写作模式！")
        print("我会一步步帮你完成文章创作，每一步都可以修改和调整。\n")
        
        # 初始化会话管理器
        self.article_id = datetime.now().strftime('%Y-%m-%d_%H%M%S')
        self.session_manager = SessionManager(self.article_id)
        self.image_manager = ImageManager(self.article_id)
        
        # 步骤 1：确定主题和标题
        print("\n💡 提示：输入 'test' 使用测试数据快速完成流程\n")
        self._step1_topic()
        
        # 步骤 2：生成大纲
        self._step2_outline()
        
        # 步骤 3：生成正文
        self._step3_content()
        
        # 步骤 4：生成配图
        self._step4_images()
        
        # 步骤 5：选择主题
        self._step5_theme()
        
        # 步骤 6：预览和导出
        self._step6_export()
    
    def _step1_topic(self):
        """步骤 1：确定主题和标题"""
        print("\n" + "="*60)
        print("📌 步骤 1：确定文章主题和标题")
        print("="*60)
        
        print("\n请告诉我：")
        print("1. 你想写什么主题的文章？（例如：康复训练、AI 技术、旅行攻略）")
        print("2. 目标读者是谁？（例如：患者、技术人员、普通大众）")
        print("3. 文章字数大概多少？（例如：2000 字、3000 字）\n")
        
        while True:
            topic = input("👉 请输入主题：").strip()
            if topic:
                self.session['topic'] = topic
                break
        
        while True:
            title = input("👉 请输入标题（不超过 25 字）：").strip()
            if title:
                if len(title) > 25:
                    print(f"⚠️  标题太长（{len(title)}字），请精简到 25 字以内")
                    continue
                self.session['title'] = title
                
                # 记录到会话日志
                self.session_manager.update_metadata('title', title)
                self.session_manager.update_metadata('topic', topic)
                self.session_manager.log_step('topic_selection', {
                    'topic': topic,
                    'title': title
                }, confirmed=True)
                
                break
        
        print(f"\n✅ 已确认:")
        print(f"   主题：{self.session['topic']}")
        print(f"   标题：{self.session['title']}")
        
        if self._confirm():
            return
        else:
            self._step1_topic()
    
    def _step2_outline(self):
        """步骤 2：生成大纲"""
        print("\n" + "="*60)
        print("📋 步骤 2：生成文章大纲")
        print("="*60)
        
        print("\n正在生成大纲...\n")
        
        # 调用 AI 生成大纲
        outline = self._generate_outline()
        
        print("📝 文章大纲:")
        print("-" * 60)
        for i, section in enumerate(outline, 1):
            print(f"{i}. {section}")
        print("-" * 60)
        
        print("\n💡 提示:")
        print("   - 输入 'm' 修改某个章节（例如：m2 修改第 2 章）")
        print("   - 输入 'a' 添加新章节")
        print("   - 输入 'd' 删除某个章节（例如：d3 删除第 3 章）")
        print("   - 直接回车确认大纲\n")
        
        while True:
            choice = input("👉 请输入操作：").strip().lower()
            
            if not choice:  # 直接回车，确认
                self.session['outline'] = outline
                print("\n✅ 大纲已确认")
                return
            
            elif choice.startswith('m') and len(choice) > 1:  # 修改章节
                try:
                    idx = int(choice[1:]) - 1
                    if 0 <= idx < len(outline):
                        new_content = input(f"👉 请输入新的第{idx+1}章内容：").strip()
                        outline[idx] = new_content
                        print(f"✅ 已修改第{idx+1}章")
                    else:
                        print("⚠️  章节编号不对")
                except:
                    print("⚠️  输入格式不对，例如：m2")
            
            elif choice.startswith('a'):  # 添加章节
                new_section = input("👉 请输入新章节内容：").strip()
                outline.append(new_section)
                print("✅ 已添加新章节")
            
            elif choice.startswith('d') and len(choice) > 1:  # 删除章节
                try:
                    idx = int(choice[1:]) - 1
                    if 0 <= idx < len(outline):
                        removed = outline.pop(idx)
                        print(f"✅ 已删除第{idx+1}章：{removed}")
                    else:
                        print("⚠️  章节编号不对")
                except:
                    print("⚠️  输入格式不对，例如：d3")
            
            else:
                print("⚠️  无效操作，请重新输入")
            
            # 显示更新后的大纲
            print("\n📝 更新后的大纲:")
            print("-" * 60)
            for i, section in enumerate(outline, 1):
                print(f"{i}. {section}")
            print("-" * 60 + "\n")
    
    def _step3_content(self):
        """步骤 3：生成正文"""
        print("\n" + "="*60)
        print("✍️  步骤 3：生成文章正文")
        print("="*60)
        
        print("\n正在根据大纲生成正文...\n")
        print("(这个过程可能需要几分钟)\n")
        
        # 调用 AI 生成正文
        content = self._generate_content()
        self.session['content'] = content
        
        print("✅ 正文生成完成！")
        print(f"   字数：{len(content)} 字")
        
        print("\n📋 操作选项:")
        print("   1. 查看完整内容")
        print("   2. 调整某个章节")
        print("   3. 重新生成")
        print("   4. 继续下一步\n")
        
        while True:
            choice = input("👉 请选择操作 (1-4):").strip()
            
            if choice == '1':
                print("\n" + "="*60)
                print(content)
                print("="*60 + "\n")
            
            elif choice == '2':
                print("\n⚠️  章节调整功能开发中...")
                print("   你可以手动编辑生成的文章文件\n")
            
            elif choice == '3':
                print("\n正在重新生成...\n")
                content = self._generate_content()
                self.session['content'] = content
                print("✅ 重新生成完成！\n")
            
            elif choice == '4':
                print("\n✅ 正文已确认")
                return
            
            else:
                print("⚠️  无效操作，请重新输入\n")
    
    def _step4_images(self):
        """步骤 4：生成配图并保存"""
        print("\n" + "="*60)
        print("🖼️  步骤 4：生成配图")
        print("="*60)
        
        print("\n正在分析文章内容，生成配图...\n")
        
        # 调用 AI 生成配图提示词
        image_prompts = self._generate_images()
        self.session['images'] = image_prompts
        
        # 优化提示词（确保与文章主旨匹配）
        print("🔍 正在优化提示词，确保与文章主旨匹配...\n")
        optimized_prompts = self._optimize_image_prompts(image_prompts)
        
        # 使用图片管理器生成并保存图片
        print(f"✅ 生成了 {len(optimized_prompts)} 个优化后的配图提示词")
        print(f"🎨 开始调用豆包 API 生成图片...\n")
        
        # 批量生成图片
        generated_images = self.image_manager.batch_generate(optimized_prompts)
        
        # 记录到会话日志
        for img in generated_images:
            self.session_manager.update_asset('image', img['path'], img)
        
        self.session_manager.update_metadata('images_count', len(generated_images))
        
        print(f"\n✅ 配图已生成并保存：{len(generated_images)} 张")
        print(f"📂 保存位置：{self.image_manager.image_dir}")
        
        for i, img in enumerate(images, 1):
            print(f"📷 配图 {i}:")
            print(f"   位置：{img.get('position', '文章中')}")
            print(f"   描述：{img.get('description', '无')}")
            print(f"   提示词：{img.get('prompt', '无')[:100]}...")
            print()
        
        print("💡 提示:")
        print("   - 输入 'v' 查看某个提示词详情（例如：v2 查看第 2 个）")
        print("   - 输入 'r' 重新生成某个提示词（例如：r1 重新生成第 1 个）")
        print("   - 输入 'a' 添加新提示词")
        print("   - 直接回车确认\n")
        
        while True:
            choice = input("👉 请输入操作：").strip().lower()
            
            if not choice:  # 直接回车，确认
                print("\n✅ 配图提示词已确认")
                return
            
            elif choice.startswith('v') and len(choice) > 1:  # 查看详情
                try:
                    idx = int(choice[1:]) - 1
                    if 0 <= idx < len(images):
                        img = images[idx]
                        print(f"\n📷 配图 {idx+1} 详情:")
                        print(f"   位置：{img.get('position')}")
                        print(f"   描述：{img.get('description')}")
                        print(f"   完整提示词：{img.get('prompt')}")
                        print(f"   风格：{img.get('style', '默认')}")
                        print()
                    else:
                        print("⚠️  编号不对\n")
                except:
                    print("⚠️  输入格式不对\n")
            
            elif choice.startswith('r') and len(choice) > 1:  # 重新生成
                try:
                    idx = int(choice[1:]) - 1
                    if 0 <= idx < len(images):
                        print(f"\n正在重新生成第{idx+1}个提示词...\n")
                        images[idx] = self._regenerate_image_prompt(images[idx])
                        print(f"✅ 已重新生成第{idx+1}个提示词\n")
                    else:
                        print("⚠️  编号不对\n")
                except:
                    print("⚠️  输入格式不对\n")
            
            elif choice.startswith('a'):  # 添加
                desc = input("👉 请输入新配图的描述：").strip()
                images.append({
                    'position': '自定义',
                    'description': desc,
                    'prompt': self._generate_prompt_from_desc(desc)
                })
                print("✅ 已添加新配图提示词\n")
            
            else:
                print("⚠️  无效操作，请重新输入\n")
    
    def _step5_theme(self):
        """步骤 5：选择排版主题"""
        print("\n" + "="*60)
        print("🎨 步骤 5：选择文章排版主题")
        print("="*60)
        
        # 读取可用主题
        from theme_loader import ThemeLoader
        loader = ThemeLoader()
        
        print("\n📚 经典主题:")
        classic_themes = loader.list_themes('classic')
        for i, theme in enumerate(classic_themes[:5], 1):
            print(f"   {i}. {theme['id']} - {theme['name']} ({theme['description'][:20]}...)")
        
        print("\n🍬 马卡龙主题:")
        macaron_themes = loader.list_themes('macaron')
        for i, theme in enumerate(macaron_themes[:5], 1):
            print(f"   {i+len(classic_themes)}. {theme['id']} - {theme['name']}")
        
        print("\n💡 提示:")
        print("   - 输入主题 ID 选择（例如：warm_artistic）")
        print("   - 输入 'l' 查看更多主题")
        print("   - 直接回车使用推荐主题\n")
        
        # 根据内容推荐主题
        keywords = self._extract_keywords()
        recommended = loader.recommend_theme(keywords)
        print(f"🌟 AI 推荐主题：{recommended}\n")
        
        while True:
            choice = input("👉 请选择主题：").strip()
            
            if not choice:  # 直接回车，使用推荐
                self.session['theme'] = recommended
                print(f"\n✅ 已选择推荐主题：{recommended}")
                return
            
            elif choice == 'l':  # 查看更多
                print("\n所有主题:")
                all_themes = loader.list_themes()
                for theme in all_themes:
                    print(f"   • {theme['id']:25} - {theme['name']}")
                print()
            
            else:  # 选择主题
                theme = loader.get_theme(choice)
                if theme:
                    self.session['theme'] = choice
                    print(f"\n✅ 已选择主题：{theme['name']}")
                    return
                else:
                    print("⚠️  主题不存在，请重新输入\n")
    
    def _step6_export(self):
        """步骤 6：预览和导出"""
        print("\n" + "="*60)
        print("💾 步骤 6：预览和导出")
        print("="*60)
        
        print("\n📋 文章信息:")
        print(f"   标题：{self.session['title']}")
        print(f"   主题：{self.session['theme']}")
        print(f"   字数：{len(self.session['content'])} 字")
        print(f"   配图：{len(self.session['images'])} 张")
        
        print("\n💡 下一步操作:")
        print("   1. 保存文章到本地")
        print("   2. 打开预览页面")
        print("   3. 导出为微信公众号格式")
        print("   4. 推送到微信草稿箱（需要配置）")
        print("   5. 退出（不保存）\n")
        
        while True:
            choice = input("👉 请选择操作 (1-5):").strip()
            
            if choice == '1':
                self._save_article()
            
            elif choice == '2':
                self._open_preview()
            
            elif choice == '3':
                self._export_wechat()
            
            elif choice == '4':
                self._push_wechat()
            
            elif choice == '5':
                print("\n⚠️  确定要退出吗？未保存的内容将丢失。")
                confirm = input("👉 确认退出？(y/n):").strip().lower()
                if confirm == 'y':
                    print("\n👋 再见！")
                    sys.exit(0)
            
            else:
                print("⚠️  无效操作，请重新输入\n")
    
    def _generate_outline(self):
        """生成大纲（调用 AI）"""
        # TODO: 调用 AI 生成大纲
        # 这里先返回示例大纲
        return [
            "引言：引出主题，吸引读者兴趣",
            "背景：介绍相关背景知识",
            "核心内容：详细讲解主要知识点",
            "案例分析：通过实际案例说明",
            "总结：回顾要点，给出建议"
        ]
    
    def _generate_content(self):
        """生成正文（调用 AI）"""
        # TODO: 调用 AI 生成正文
        return "这里是文章正文内容..."
    
    def _generate_images(self):
        """生成配图提示词（调用 AI）"""
        # TODO: 调用 AI 生成配图
        return [
            {
                'position': '引言后',
                'description': '康复训练场景',
                'prompt': '医疗康复训练场景，专业教练指导患者进行训练，温暖明亮的环境，高清摄影风格',
                'style': 'medical'
            },
            {
                'position': '核心内容',
                'description': '肌肉解剖图',
                'prompt': '人体肌肉解剖示意图，标注关键肌肉群，医学插画风格，清晰专业',
                'style': 'medical'
            },
            {
                'position': '案例分析',
                'description': '训练前后对比',
                'prompt': '康复训练前后对比图，展示改善效果，真实照片风格',
                'style': 'medical'
            }
        ]
    
    def _extract_keywords(self):
        """提取关键词"""
        import re
        content = self.session['content'][:1000]
        words = re.findall(r'[\u4e00-\u9fa5]{2,}', content)
        return list(set(words))[:10]
    
    def _regenerate_image_prompt(self, image):
        """重新生成配图提示词"""
        # TODO: 调用 AI 重新生成
        return image
    
    def _generate_prompt_from_desc(self, desc):
        """从描述生成提示词"""
        # TODO: 调用 AI 生成
        return f"根据描述生成：{desc}"
    
    def _optimize_image_prompts(self, prompts):
        """
        优化配图提示词，确保与文章主旨匹配
        
        Args:
            prompts: 原始提示词列表
        
        Returns:
            list: 优化后的提示词列表
        """
        # 临时保存提示词到文件，供优化器使用
        temp_prompts_file = os.path.join(script_dir, 'output', 'temp_prompts.json')
        os.makedirs(os.path.dirname(temp_prompts_file), exist_ok=True)
        
        with open(temp_prompts_file, 'w', encoding='utf-8') as f:
            json.dump(prompts, f, ensure_ascii=False, indent=2)
        
        # 创建临时图片元数据
        temp_metadata = []
        for i, prompt in enumerate(prompts, 1):
            temp_metadata.append({
                'type': 'image',
                'index': i,
                'description': prompt.get('description', ''),
                'prompt': prompt.get('prompt', ''),
                'position': prompt.get('position', '')
            })
        
        temp_meta_file = os.path.join(script_dir, 'output', 'temp_metadata.json')
        with open(temp_meta_file, 'w', encoding='utf-8') as f:
            json.dump(temp_metadata, f, ensure_ascii=False, indent=2)
        
        # 使用优化器分析
        article_path = os.path.join(script_dir, 'output', 'articles', f'article_{self.article_id}.md')
        
        # 查找文章文件
        if not os.path.exists(article_path):
            articles_dir = os.path.join(script_dir, 'output', 'articles')
            for f in os.listdir(articles_dir):
                if self.article_id in f and f.endswith('.md'):
                    article_path = os.path.join(articles_dir, f)
                    break
        
        if os.path.exists(article_path):
            optimizer = PromptOptimizer(article_path, os.path.join(script_dir, 'output', 'images', self.article_id))
            
            # 获取优化建议
            report = optimizer.analyze_current_prompts()
            
            if report['suggestions']:
                print(f"💡 发现 {len(report['suggestions'])} 个提示词需要优化\n")
                
                # 应用优化
                optimized_prompts = prompts.copy()
                for suggestion in report['suggestions']:
                    idx = int(suggestion['filename'].split('_')[1]) - 1
                    if 0 <= idx < len(optimized_prompts):
                        optimized_prompts[idx]['prompt'] = suggestion['optimized']
                        print(f"   ✅ 配图{idx+1}: {suggestion['reason']}")
                
                print()
                return optimized_prompts
        
        # 如果没有优化建议，返回原始提示词
        return prompts
    
    def _save_article(self):
        """保存文章"""
        # 使用规范化命名
        safe_title = self.session['title'][:20].replace('/', '_').replace('\\', '_')
        filename = f"{self.article_id}_{safe_title}.md"
        filepath = os.path.join(script_dir, 'output', 'articles', filename)
        
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(f"# {self.session['title']}\n\n")
            f.write(f"_创作于 {datetime.now().strftime('%Y-%m-%d %H:%M')}_\n\n")
            f.write(self.session['content'])
        
        print(f"\n✅ 文章已保存到：{filepath}")
        
        # 记录到会话日志
        self.session_manager.update_asset('markdown', filepath, {
            'words': len(self.session['content']),
            'title': self.session['title']
        })
        self.session_manager.update_metadata('words', len(self.session['content']))
        
        # 创建版本快照
        self.session_manager.create_version_snapshot('final')
        
        # 完成会话
        self.session_manager.complete_session(locked=self.locked)
    
    def _open_preview(self):
        """打开预览页面"""
        import subprocess
        preview_file = os.path.join(script_dir, '..', 'preview_enhanced.html')
        if os.path.exists(preview_file):
            subprocess.run(['open', preview_file])
            print("\n✅ 预览页面已打开")
        else:
            print("\n❌ 预览页面不存在")
    
    def _simple_export(self, html_output):
        """简单 HTML 导出"""
        html_content = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>{self.session['title']}</title>
</head>
<body>
    <h1>{self.session['title']}</h1>
    {self.session['content'].replace(chr(10), '<br/>')}
</body>
</html>
"""
        with open(html_output, 'w', encoding='utf-8') as f:
            f.write(html_content)
        print(f"✅ 简单 HTML 已导出：{html_output}")
    
    def _export_wechat(self):
        """导出为微信格式"""
        print("\n" + "="*60)
        print("📤 导出微信公众号格式")
        print("="*60)
        
        # 调用 export_wechat.py
        import subprocess
        
        # 先找到刚保存的 Markdown 文件
        markdown_file = self.session_manager.get_assets()['markdown']['path']
        html_output = os.path.join(
            script_dir, 'output', 'drafts',
            f"{self.article_id}_{self.session['title'][:20]}.html"
        )
        
        print(f"\n🔄 正在导出 HTML...")
        print(f"   源文件：{markdown_file}")
        print(f"   输出：{html_output}\n")
        
        # 调用导出脚本
        export_script = os.path.join(script_dir, 'export_wechat.py')
        if os.path.exists(export_script):
            result = subprocess.run([
                'python3', export_script,
                '--input', markdown_file,
                '--output', html_output,
                '--article-id', self.article_id
            ], capture_output=True, text=True)
            
            if result.returncode == 0:
                print("✅ HTML 导出成功！")
                
                # 记录 HTML 文件到会话日志
                self.session_manager.update_asset('html', html_output)
                
                print(f"\n📄 HTML 文件：{html_output}")
            else:
                print(f"❌ 导出失败：{result.stderr}")
        else:
            print("⚠️  export_wechat.py 不存在，使用基础导出")
            # 简单导出
            self._simple_export(html_output)
    
    def _push_wechat(self):
        """推送到微信"""
        print("\n⚠️  微信推送功能开发中...")
        print("   需要先配置微信 API\n")
    
    def _confirm(self):
        """确认操作"""
        confirm = input("\n👉 确认吗？(y/n):").strip().lower()
        return confirm == 'y'


def main():
    """主函数"""
    writer = InteractiveWriter()
    writer.start()


if __name__ == '__main__':
    main()
