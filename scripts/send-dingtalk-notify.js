#!/usr/bin/env node

/**
 * 钉钉通知脚本
 * 用法：node send-dingtalk-notify.js "消息内容"
 */

const https = require('https');

const CONFIG = {
  clientId: 'dingoanmhskwhpb6hr4l',
  clientSecret: 'GWi4BlzVudLN06E8a9Iq-ATa-aDWrSRLX18Mmv65UkrZXdJmrVPEXBnemi6s5b4K',
  userId: '033618275733117496',
};

const DINGTALK_API = 'https://api.dingtalk.com';

async function getAccessToken() {
  return new Promise((resolve, reject) => {
    const data = JSON.stringify({
      appKey: CONFIG.clientId,
      appSecret: CONFIG.clientSecret,
    });

    const options = {
      hostname: 'api.dingtalk.com',
      port: 443,
      path: '/v1.0/oauth2/accessToken',
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Content-Length': data.length,
      },
    };

    const req = https.request(options, (res) => {
      let body = '';
      res.on('data', (chunk) => body += chunk);
      res.on('end', () => {
        try {
          const result = JSON.parse(body);
          resolve(result.accessToken);
        } catch (e) {
          reject(new Error('Failed to parse access token response'));
        }
      });
    });

    req.on('error', reject);
    req.write(data);
    req.end();
  });
}

async function sendTextMessage(accessToken, userId, text) {
  return new Promise((resolve, reject) => {
    const postData = {
      robotCode: CONFIG.clientId,
      userIds: [userId],  // 必须是数组
      msgKey: 'sampleText',
      msgParam: JSON.stringify({ content: text }),
    };
    const data = JSON.stringify(postData);
    
    console.log(`📝 POST data: ${data}`);

    const options = {
      hostname: 'api.dingtalk.com',
      port: 443,
      path: '/v1.0/robot/oToMessages/batchSend',
      method: 'POST',
      headers: {
        'x-acs-dingtalk-access-token': accessToken,
        'Content-Type': 'application/json',
        'Content-Length': Buffer.byteLength(data),
      },
    };

    const req = https.request(options, (res) => {
      let body = '';
      res.on('data', (chunk) => body += chunk);
      res.on('end', () => {
        console.log(`📥 Response: ${body}`);
        try {
          const result = JSON.parse(body);
          if (result.processQueryKey) {
            resolve({ success: true, processQueryKey: result.processQueryKey });
          } else {
            reject(new Error(result.message || 'Unknown error'));
          }
        } catch (e) {
          reject(new Error(`Failed to parse response: ${e.message}`));
        }
      });
    });

    req.on('error', reject);
    req.write(data);
    req.end();
  });
}

async function main() {
  const message = process.argv.slice(2).join(' ') || '测试通知';
  
  console.log(`📬 发送钉钉通知：${message}`);
  
  try {
    const token = await getAccessToken();
    console.log(`✅ 获取 access token 成功`);
    
    const result = await sendTextMessage(token, CONFIG.userId, message);
    console.log(`✅ 钉钉通知发送成功！processQueryKey: ${result.processQueryKey}`);
  } catch (error) {
    console.error(`❌ 发送失败：${error.message}`);
    process.exit(1);
  }
}

main();
