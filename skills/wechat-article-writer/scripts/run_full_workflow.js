#!/usr/bin/env node
/**
 * run_full_workflow.js - 完整工作流封装
 * 一键执行：写文 → 生图 → 配图 → 压缩 → 转换 → 发布
 */

const { execSync } = require('child_process');
const path = require('path');
const fs = require('fs');

const SCRIPTS_DIR = __dirname;
const OUTPUT_DIR = path.join(SCRIPTS_DIR, 'output');

function runCommand(cmd, description) {
    console.log(`\n🚀 ${description}`);
    console.log(`执行：${cmd}`);
    try {
        const output = execSync(cmd, { encoding: 'utf-8', stdio: 'inherit' });
        return output;
    } catch (error) {
        console.error(`❌ ${description} 失败`);
        throw error;
    }
}

function parseArgs() {
    const args = process.argv.slice(2);
    const parsed = {
        topic: '',
        style: '干货',
        layout: '暖色'
    };
    
    for (let i = 0; i < args.length; i++) {
        if (args[i] === '--topic' && args[i + 1]) {
            parsed.topic = args[i + 1];
            i++;
        } else if (args[i] === '--style' && args[i + 1]) {
            parsed.style = args[i + 1];
            i++;
        } else if (args[i] === '--layout' && args[i + 1]) {
            parsed.layout = args[i + 1];
            i++;
        }
    }
    
    return parsed;
}

function main() {
    const args = parseArgs();
    
    if (!args.topic) {
        console.error('❌ 请提供文章主题 --topic "主题内容"');
        process.exit(1);
    }
    
    console.log('='.repeat(50));
    console.log('📝 微信公众号全自动发文工作流');
    console.log('='.repeat(50));
    console.log(`主题：${args.topic}`);
    console.log(`风格：${args.style}`);
    console.log(`排版：${args.layout}`);
    
    // 步骤 1: 生成文章
    const articleOutput = runCommand(
        `python3 ${path.join(SCRIPTS_DIR, 'write_article.py')} --topic "${args.topic}" --style "${args.style}"`,
        '步骤 1/6: 生成文章'
    );
    
    // 从输出中提取文章路径（简化处理，实际应该解析输出）
    const articlesDir = path.join(OUTPUT_DIR, 'articles');
    const articleFiles = fs.readdirSync(articlesDir).filter(f => f.endsWith('.md'));
    const latestArticle = articleFiles[articleFiles.length - 1];
    const articlePath = path.join(articlesDir, latestArticle);
    
    // 步骤 2: 生成封面图
    runCommand(
        `python3 ${path.join(SCRIPTS_DIR, 'generate_image.py')} --topic "${args.topic}" --style "${args.style}"`,
        '步骤 2/6: 生成封面图'
    );
    
    // 步骤 3: 智能配图
    runCommand(
        `python3 ${path.join(SCRIPTS_DIR, 'add_article_images.py')} --article "${articlePath}" --topic "${args.topic}" --style "${args.style}"`,
        '步骤 3/6: 智能配图'
    );
    
    // 步骤 4: 压缩图片
    const imagesDir = path.join(OUTPUT_DIR, 'images');
    runCommand(
        `python3 ${path.join(SCRIPTS_DIR, 'compress_image.py')} --input "${imagesDir}"`,
        '步骤 4/6: 压缩图片'
    );
    
    // 步骤 5: 格式转换
    runCommand(
        `python3 ${path.join(SCRIPTS_DIR, 'format_article.py')} --input "${articlePath}"`,
        '步骤 5/6: 格式转换'
    );
    
    const htmlPath = articlePath.replace('.md', '.html');
    
    // 步骤 6: 发布草稿
    const coverImage = path.join(imagesDir, fs.readdirSync(imagesDir).filter(f => f.startsWith('cover_'))[0]);
    runCommand(
        `python3 ${path.join(SCRIPTS_DIR, 'publish_draft.py')} --html "${htmlPath}" --cover "${coverImage}"`,
        '步骤 6/6: 发布草稿箱'
    );
    
    console.log('\n' + '='.repeat(50));
    console.log('✅ 全部完成！请前往公众号草稿箱查看');
    console.log('='.repeat(50));
}

main();
