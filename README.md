# Cursor Agents 页面自动填写脚本

这个项目提供了自动化脚本来帮助你在 [Cursor Agents 页面](https://cursor.com/cn/agents) 上自动填写表单信息。

## 功能特性

- 🚀 自动填写表单字段（姓名、邮箱、公司、电话、留言等）
- 🌐 支持多种浏览器（Chrome、Firefox、Edge）
- ⚙️ 可配置的表单数据和设置
- 📸 自动截图保存
- 🔒 隐藏自动化特征，避免被检测
- 📝 详细的日志记录
- 🎯 智能表单元素识别

## 文件说明

- `auto_fill_cursor_agents.py` - 基础版本自动化脚本
- `advanced_auto_filler.py` - 高级版本，支持多种浏览器和更好配置
- `requirements.txt` - Python依赖包
- `.env.example` - 环境变量配置示例
- `config.json.example` - JSON配置文件示例
- `README.md` - 使用说明文档

## 安装步骤

### 1. 安装Python依赖

```bash
pip install -r requirements.txt
```

### 2. 配置个人信息

#### 方法1：使用环境变量（推荐）

复制 `.env.example` 为 `.env` 并修改：

```bash
cp .env.example .env
```

编辑 `.env` 文件，填入你的真实信息：

```env
CURSOR_NAME=你的真实姓名
CURSOR_EMAIL=your.real.email@example.com
CURSOR_COMPANY=你的公司名称
CURSOR_PHONE=你的真实电话号码
CURSOR_MESSAGE=我想了解更多关于Cursor Agents的信息
```

#### 方法2：使用JSON配置文件

复制 `config.json.example` 为 `config.json` 并修改：

```bash
cp config.json.example config.json
```

编辑 `config.json` 文件，填入你的真实信息。

## 使用方法

### 基础版本

```bash
python auto_fill_cursor_agents.py
```

### 高级版本

#### 基本使用
```bash
python advanced_auto_filler.py
```

#### 选择浏览器
```bash
# 使用Chrome（默认）
python advanced_auto_filler.py --browser chrome

# 使用Firefox
python advanced_auto_filler.py --browser firefox

# 使用Edge
python advanced_auto_filler.py --browser edge
```

#### 无头模式（不显示浏览器窗口）
```bash
python advanced_auto_filler.py --headless
```

#### 使用自定义配置文件
```bash
python advanced_auto_filler.py --config my_config.json
```

## 配置选项

### 环境变量配置

| 变量名 | 说明 | 默认值 |
|--------|------|--------|
| `CURSOR_NAME` | 姓名 | 张三 |
| `CURSOR_EMAIL` | 邮箱 | test@example.com |
| `CURSOR_COMPANY` | 公司 | 测试公司 |
| `CURSOR_PHONE` | 电话 | 13800138000 |
| `CURSOR_MESSAGE` | 留言 | 我想了解更多关于Cursor Agents的信息 |

### JSON配置文件选项

| 选项 | 说明 | 默认值 |
|------|------|--------|
| `url` | 目标页面URL | https://cursor.com/cn/agents |
| `wait_timeout` | 等待超时时间（秒） | 10 |
| `page_load_delay` | 页面加载延迟（秒） | 3 |
| `field_delay` | 字段填写间隔（秒） | 0.5 |
| `submit_delay` | 提交后等待时间（秒） | 3 |
| `close_delay` | 关闭前等待时间（秒） | 5 |

## 注意事项

1. **浏览器要求**：确保你的系统已安装Chrome、Firefox或Edge浏览器
2. **网络连接**：需要稳定的网络连接访问目标页面
3. **反爬虫检测**：脚本已包含反检测机制，但某些网站可能有额外保护
4. **个人信息安全**：不要在公共代码库中提交包含真实个人信息的配置文件

## 故障排除

### 常见问题

1. **ChromeDriver错误**
   - 脚本会自动下载ChromeDriver，如果失败请手动安装

2. **找不到表单元素**
   - 检查页面是否完全加载
   - 查看日志文件了解详细信息
   - 可能需要调整等待时间

3. **浏览器启动失败**
   - 确保浏览器已正确安装
   - 检查是否有其他程序占用浏览器

### 日志文件

脚本运行时会生成 `cursor_agents_auto.log` 日志文件，包含详细的运行信息。

## 高级用法

### 自定义表单字段选择器

如果需要支持特定的表单结构，可以修改脚本中的 `selectors` 字典：

```python
selectors = {
    'custom_field': [
        'input[name="custom_name"]',
        'input[class="custom_class"]'
    ]
}
```

### 添加新的表单字段

1. 在配置文件中添加新字段
2. 在脚本中添加相应的选择器
3. 更新表单填写逻辑

## 许可证

本项目仅供学习和个人使用，请遵守相关网站的使用条款。

## 贡献

欢迎提交Issue和Pull Request来改进这个项目！

## 免责声明

本脚本仅用于自动化测试和学习目的。使用者需要：
- 遵守目标网站的使用条款
- 不用于恶意目的
- 承担使用风险

请合理使用，不要对目标网站造成过大负担。