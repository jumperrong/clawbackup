#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
monitor_ip.py - 监控公网 IP 变化
检测 IP 变化后通过飞书发送通知
"""

import requests
import json
import os
from datetime import datetime

# 配置文件路径
IP_RECORD_FILE = os.path.expanduser('~/.openclaw/workspace/logs/last_ip.txt')
NOTIFY_FILE = os.path.expanduser('~/.openclaw/workspace/logs/pending-notify.txt')

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
                print(f"✅ 从 {service} 获取 IP: {ip}")
                return ip
        except Exception as e:
            print(f"❌ {service} 失败：{e}")
            continue
    
    return None

def load_last_ip():
    """读取上次记录的 IP"""
    if os.path.exists(IP_RECORD_FILE):
        with open(IP_RECORD_FILE, 'r', encoding='utf-8') as f:
            return f.read().strip()
    return None

def save_ip(ip):
    """保存当前 IP"""
    os.makedirs(os.path.dirname(IP_RECORD_FILE), exist_ok=True)
    with open(IP_RECORD_FILE, 'w', encoding='utf-8') as f:
        f.write(ip)
    print(f"💾 IP 已保存：{ip}")

def send_notify(new_ip, old_ip):
    """发送 IP 变化通知"""
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    message = f"""🌐 公网 IP 变化通知

📅 检测时间：{timestamp}

🔴 旧 IP：{old_ip}
🟢 新 IP：{new_ip}

⚠️ 请在微信公众号后台更新 IP 白名单：
1. 登录 https://mp.weixin.qq.com
2. 开发 → 基本配置 → IP 白名单
3. 添加新 IP：{new_ip}
4. 删除旧 IP：{old_ip}

📝 配置完成后测试发布功能。
"""
    
    # 写入通知文件（heartbeat 时会通过飞书发送）
    os.makedirs(os.path.dirname(NOTIFY_FILE), exist_ok=True)
    with open(NOTIFY_FILE, 'w', encoding='utf-8') as f:
        f.write(message)
    
    print(f"📬 通知已写入：{NOTIFY_FILE}")
    print("\n" + message)

def main():
    print("="*60)
    print("🌐 公网 IP 监控")
    print("="*60)
    print()
    
    # 获取当前 IP
    current_ip = get_public_ip()
    
    if not current_ip:
        print("❌ 无法获取公网 IP")
        return
    
    # 读取上次记录的 IP
    last_ip = load_last_ip()
    
    print(f"📊 上次记录 IP: {last_ip if last_ip else '无记录'}")
    print(f"📊 当前公网 IP: {current_ip}")
    print()
    
    # 检测 IP 是否变化
    if last_ip and current_ip != last_ip:
        print("⚠️  IP 发生变化！")
        print()
        
        # 发送通知
        send_notify(current_ip, last_ip)
        
        # 更新 IP 记录
        save_ip(current_ip)
        
        print("\n✅ IP 监控完成（检测到变化）")
    else:
        if not last_ip:
            print("ℹ️  首次运行，记录当前 IP")
            save_ip(current_ip)
        else:
            print("✅ IP 未发生变化")
        
        print("\n✅ IP 监控完成")

if __name__ == "__main__":
    main()
