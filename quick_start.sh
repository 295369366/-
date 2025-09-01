#!/bin/bash

echo "🚀 Cursor Agents 自动填写脚本快速启动"
echo "=================================="

# 检查Python是否安装
if ! command -v python3 &> /dev/null; then
    echo "❌ 错误: 未找到Python3，请先安装Python3"
    exit 1
fi

# 检查pip是否安装
if ! command -v pip3 &> /dev/null; then
    echo "❌ 错误: 未找到pip3，请先安装pip3"
    exit 1
fi

echo "✅ Python3 和 pip3 已安装"

# 安装依赖
echo "📦 正在安装Python依赖..."
pip3 install -r requirements.txt

if [ $? -ne 0 ]; then
    echo "❌ 依赖安装失败，请检查网络连接或手动安装"
    exit 1
fi

echo "✅ 依赖安装完成"

# 检查配置文件
if [ ! -f ".env" ]; then
    echo "📝 未找到.env配置文件，正在创建..."
    if [ -f ".env.example" ]; then
        cp .env.example .env
        echo "✅ 已创建.env文件，请编辑此文件填入你的真实信息"
        echo "💡 提示: 使用 'nano .env' 或 'vim .env' 编辑文件"
    else
        echo "❌ 未找到.env.example文件"
        exit 1
    fi
else
    echo "✅ 找到.env配置文件"
fi

echo ""
echo "🎯 配置完成！现在你可以运行以下命令："
echo ""
echo "基础版本:"
echo "  python3 auto_fill_cursor_agents.py"
echo ""
echo "高级版本:"
echo "  python3 advanced_auto_filler.py"
echo ""
echo "高级版本选项:"
echo "  python3 advanced_auto_filler.py --browser firefox"
echo "  python3 advanced_auto_filler.py --headless"
echo ""
echo "📖 更多信息请查看 README.md 文件"
echo "🔧 如有问题，请检查日志文件 cursor_agents_auto.log"