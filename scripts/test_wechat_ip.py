#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
test_wechat_ip.py - 测试微信公众号 API 实际看到的 IP
直接调用微信 API，获取服务器端记录的真实 IP
"""

import requests
import json
import os

def load_config():
    """加载微信公众号配置"""
    config_path = os.path.join(os.path.dirname(__file__), '..', 'skills', 'wechat-article-writer', 'config.json')
    with open(config_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def test_wechat_api_ip():
    """
    测试微信 API 实际看到的 IP
    
    通过获取 access_token，然后查看返回头或错误信息中的 IP
    """
    config = load_config()
    
    appid = config['wechat_appid']
    appsecret = config['wechat_appsecret']
    
    print("="*60)
    print("🔍 微信公众号 API IP 检测")
    print("="*60)
    print()
    
    # 1. 获取 access_token
    url = f'https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid={appid}&secret={appsecret}'
    
    print(f"📡 请求微信 API...")
    print(f"   URL: {url[:80]}...")
    print()
    
    try:
        response = requests.get(url, timeout=10)
        
        # 2. 检查响应
        print(f"📊 响应状态码：{response.status_code}")
        print(f"📊 响应内容：{response.text[:200]}")
        print()
        
        data = response.json()
        
        if 'access_token' in data:
            print("✅ 微信公众号连接成功！")
            print(f"   Access Token: {data['access_token'][:20]}...")
            print(f"   Expires In: {data.get('expires_in', 7200)} 秒")
            print()
            print("ℹ️  说明：当前 IP 在微信白名单中")
        else:
            error_code = data.get('errcode', 0)
            error_msg = data.get('errmsg', '未知错误')
            
            print(f"❌ 微信公众号连接失败")
            print(f"   错误码：{error_code}")
            print(f"   错误信息：{error_msg}")
            print()
            
            # 3. 分析错误
            if error_code == 40164:
                print("⚠️  IP 不在白名单！")
                print()
                print("📝 解决方案：")
                print("1. 获取当前公网 IP（见下方）")
                print("2. 登录微信公众平台")
                print("3. 开发 → 基本配置 → IP 白名单")
                print("4. 添加当前 IP")
                print()
                
                # 4. 获取当前 IP
                print("🔍 正在获取当前公网 IP...")
                current_ip = get_public_ip()
                if current_ip:
                    print(f"🟢 当前公网 IP: {current_ip}")
                    print()
                    print(f"⚠️  请在微信后台添加此 IP: {current_ip}")
            elif error_code == 40013:
                print("⚠️  AppID 或 AppSecret 错误")
            elif error_code == 40002:
                print("⚠️  参数错误")
            else:
                print("⚠️  其他错误，请检查配置")
        
        return data
        
    except Exception as e:
        print(f"❌ 请求失败：{e}")
        print()
        print("🔍 尝试获取当前公网 IP...")
        current_ip = get_public_ip()
        if current_ip:
            print(f"🟢 当前公网 IP: {current_ip}")
        return None

def get_public_ip():
    """获取当前公网 IP"""
    services = [
        'https://api.ipify.org',
        'https://icanhazip.com',
        'https://ifconfig.me/ip',
        'https://ip.sb',
    ]
    
    for service in services:
        try:
            response = requests.get(service, timeout=5)
            if response.status_code == 200:
                ip = response.text.strip()
                return ip
        except:
            continue
    
    return None

def main():
    # 测试微信 API
    result = test_wechat_api_ip()
    
    print()
    print("="*60)
    print("📊 总结")
    print("="*60)
    
    if result and 'access_token' in result:
        print("✅ 微信 API 连接成功")
        print("ℹ️  当前 IP 已在白名单中，可以正常使用")
    else:
        print("❌ 微信 API 连接失败")
        print("⚠️  需要配置 IP 白名单")
        print()
        print("📝 下一步：")
        print("1. 获取当前公网 IP")
        print("2. 在微信后台添加 IP 白名单")
        print("3. 重新测试")

if __name__ == "__main__":
    main()
