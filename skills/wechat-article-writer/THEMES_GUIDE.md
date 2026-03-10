# 微信公众号排版主题说明

## ✅ 兼容性保证

**已验证支持的特性：**

| CSS 属性 | 公众号支持 | 说明 |
|---------|-----------|------|
| `border-left` | ✅ 支持 | 用于标题左侧边框 |
| `background` | ✅ 支持 | 用于引用块背景色 |
| `border-radius` | ✅ 支持 | 圆角效果 |
| `box-shadow` | ✅ 支持 | 图片阴影 |
| `style` 内联 | ✅ 支持 | **关键：必须内联到每个元素** |
| CSS 变量 | ❌ 不支持 | 不能使用 `:root` 和 `var()` |
| `<style>` 标签 | ❌ 不支持 | 公众号会过滤掉 |

---

## 🎨 三个主题样式

### 1. 🔴 经典红（default）

**适用场景：** 通用、生活、情感、资讯

**配色方案：**
- 主色：`#ff6b6b`（红色）
- 背景：`#ffe3e3`（浅红）
- 特点：醒目、活力

**样式示例：**
```html
<h2 style="border-left: 4px solid #ff6b6b;">标题</h2>
<blockquote style="background: #ffe3e3; border-left: 4px solid #ff6b6b;">引用</blockquote>
```

---

### 2. 🟢 医疗专业（medical）

**适用场景：** 医疗、健康、康复、科普

**配色方案：**
- 主色：`#07c160`（微信绿）
- 背景：`#e8f7f0`（浅绿）
- 特点：专业、信任、健康感

**样式示例：**
```html
<h2 style="border-left: 4px solid #07c160;">标题</h2>
<blockquote style="background: #e8f7f0; border-left: 4px solid #07c160;">引用</blockquote>
```

---

### 3. 🔵 科技蓝（tech）

**适用场景：** 科技、互联网、AI、数码

**配色方案：**
- 主色：`#1890ff`（科技蓝）
- 背景：`#e6f7ff`（浅蓝）
- 特点：理性、专业、科技感

**样式示例：**
```html
<h2 style="border-left: 4px solid #1890ff;">标题</h2>
<blockquote style="background: #e6f7ff; border-left: 4px solid #1890ff;">引用</blockquote>
```

---

## 📋 使用方法

### 方法一：导出 HTML 后复制粘贴（推荐）

```bash
# 生成医疗主题
python3 scripts/export_wechat.py --input articles/article_xxx.md --theme medical

# 生成科技主题
python3 scripts/export_wechat.py --input articles/article_xxx.md --theme tech

# 生成经典红主题
python3 scripts/export_wechat.py --input articles/article_xxx.md --theme default
```

**操作步骤：**
1. 运行上面的命令生成 HTML 文件
2. 用浏览器打开生成的 HTML 文件
3. 全选（Cmd+A）→ 复制（Cmd+C）
4. 在微信公众号后台编辑器粘贴（Cmd+V）

---

### 方法二：一键发布（待配置）

需要先配置微信公众号 AppID 和 Secret：

```bash
python3 scripts/publish_draft.py --article article_xxx.md --theme medical
```

---

## ✨ 样式内联化说明

**为什么要内联化？**

微信公众号编辑器不支持：
- ❌ 外部 CSS 文件
- ❌ `<style>` 标签
- ❌ CSS 变量（`:root` / `var()`）

**解决方案：**

将所有样式直接写到每个 HTML 元素的 `style` 属性中：

```html
<!-- ❌ 错误写法（公众号不支持） -->
<style>
  h2 { border-left: 4px solid #07c160; }
</style>
<h2>标题</h2>

<!-- ✅ 正确写法（内联化） -->
<h2 style="border-left: 4px solid #07c160;">标题</h2>
```

---

## 🧪 测试建议

**在正式发布前，建议：**

1. **发送预览到手机** - 检查移动端显示效果
2. **测试不同设备** - iOS / Android 微信客户端
3. **检查图片加载** - 确保图片链接有效
4. **验证样式** - 边框、背景色是否正确显示

---

## 📁 生成的文件

每次导出会生成 3 个 HTML 文件：

```
scripts/output/articles/
├── article_xxx_medical_wechat_20260310_071540.html  # 医疗主题
├── article_xxx_tech_wechat_20260310_071545.html     # 科技主题
└── article_xxx_default_wechat_20260310_071545.html  # 经典红主题
```

---

## 🎯 最佳实践

1. **优先使用医疗主题** - 你的文章是康复健康类，医疗主题最匹配
2. **保持简洁** - 避免过于复杂的样式
3. **图片压缩** - 确保每张图片 < 100KB（已自动处理）
4. **预览测试** - 发布前务必发送预览到手机查看

---

_最后更新：2026-03-10_
