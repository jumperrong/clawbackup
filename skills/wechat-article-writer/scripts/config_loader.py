#!/usr/bin/env python3
"""
配置加载工具
优先从环境变量读取，其次从 config.json 读取
"""

import os
import json
from pathlib import Path
from typing import Optional, Dict


class ConfigLoader:
    """配置加载器"""
    
    def __init__(self, config_file: Optional[str] = None):
        if config_file is None:
            config_file = os.path.join(os.path.dirname(__file__), '..', 'config.json')
        self.config_file = Path(config_file)
        self.config = {}
        self._load_config()
    
    def _load_config(self):
        """加载配置"""
        # 优先从环境变量读取
        self.config = {
            'bailian_api_key': os.environ.get('BAILIAN_API_KEY'),
            'bailian_base_url': os.environ.get('BAILIAN_BASE_URL', 'https://coding.dashscope.aliyuncs.com/v1'),
            'writing_model': os.environ.get('WRITING_MODEL', 'qwen3-max-2026-01-23'),
            'image_model': os.environ.get('IMAGE_MODEL', 'qwen3.5-plus'),
            'fast_model': os.environ.get('FAST_MODEL', 'glm-4.7'),
            'agent_model': os.environ.get('AGENT_MODEL', 'glm-5'),
            'doubao_api_key': os.environ.get('DOUBAO_API_KEY'),
            'wechat_appid': os.environ.get('WECHAT_APP_ID'),
            'wechat_appsecret': os.environ.get('WECHAT_APP_SECRET'),
            'tavily_api_key': os.environ.get('TAVILY_API_KEY'),
        }
        
        # 如果环境变量不存在，从 config.json 读取（兼容旧配置）
        if self.config_file.exists():
            try:
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    file_config = json.load(f)
                
                # 只填充环境变量中不存在的值
                for key, value in file_config.items():
                    if self.config.get(key) is None:
                        self.config[key] = value
            except Exception as e:
                print(f"⚠️  警告：读取 config.json 失败：{e}")
    
    def get(self, key: str, default=None):
        """获取配置值"""
        return self.config.get(key, default)
    
    def __getitem__(self, key: str):
        """获取配置值（字典方式）"""
        return self.config[key]
    
    def __contains__(self, key: str):
        """检查配置是否存在"""
        return key in self.config
    
    def is_configured(self, key: str) -> bool:
        """检查某个配置是否已设置"""
        value = self.config.get(key)
        return value is not None and value != '' and not value.startswith('your-')
    
    def check_required(self, required_keys: list) -> bool:
        """检查必需配置是否都存在"""
        missing = []
        for key in required_keys:
            if not self.is_configured(key):
                missing.append(key)
        
        if missing:
            print(f"❌ 缺少必需配置：{', '.join(missing)}")
            print(f"   请设置环境变量或编辑 config.json")
            return False
        return True


# 全局配置实例
_config: Optional[ConfigLoader] = None


def get_config() -> ConfigLoader:
    """获取全局配置实例"""
    global _config
    if _config is None:
        _config = ConfigLoader()
    return _config


def check_api_keys() -> Dict[str, bool]:
    """检查所有 API Key 的配置状态"""
    config = get_config()
    return {
        'bailian': config.is_configured('bailian_api_key'),
        'doubao': config.is_configured('doubao_api_key'),
        'wechat': config.is_configured('wechat_appid') and config.is_configured('wechat_appsecret'),
        'tavily': config.is_configured('tavily_api_key'),
    }


def main():
    """测试配置加载"""
    print("🔧 配置检查\n")
    
    config = get_config()
    api_status = check_api_keys()
    
    print("📋 API Key 状态:")
    for name, status in api_status.items():
        icon = "✅" if status else "❌"
        print(f"  {icon} {name}: {'已配置' if status else '未配置'}")
    
    print("\n📊 当前配置:")
    for key, value in config.config.items():
        if value and not key.endswith('_key') and not key.endswith('_secret'):
            print(f"  {key}: {value}")
        elif value:
            # 隐藏敏感信息
            masked = value[:6] + '***' + value[-4:] if len(value) > 10 else '***'
            print(f"  {key}: {masked}")


if __name__ == '__main__':
    main()
