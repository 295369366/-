@echo off
chcp 65001 >nul
echo 🚀 Cursor Agents 自动填写脚本快速启动
echo ==================================

REM 检查Python是否安装
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ 错误: 未找到Python，请先安装Python
    pause
    exit /b 1
)

REM 检查pip是否安装
pip --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ 错误: 未找到pip，请先安装pip
    pause
    exit /b 1
)

echo ✅ Python 和 pip 已安装

REM 安装依赖
echo 📦 正在安装Python依赖...
pip install -r requirements.txt

if %errorlevel% neq 0 (
    echo ❌ 依赖安装失败，请检查网络连接或手动安装
    pause
    exit /b 1
)

echo ✅ 依赖安装完成

REM 检查配置文件
if not exist ".env" (
    echo 📝 未找到.env配置文件，正在创建...
    if exist ".env.example" (
        copy ".env.example" ".env" >nul
        echo ✅ 已创建.env文件，请编辑此文件填入你的真实信息
        echo 💡 提示: 使用记事本或其他文本编辑器编辑.env文件
    ) else (
        echo ❌ 未找到.env.example文件
        pause
        exit /b 1
    )
) else (
    echo ✅ 找到.env配置文件
)

echo.
echo 🎯 配置完成！现在你可以运行以下命令：
echo.
echo 基础版本:
echo   python auto_fill_cursor_agents.py
echo.
echo 高级版本:
echo   python advanced_auto_filler.py
echo.
echo 高级版本选项:
echo   python advanced_auto_filler.py --browser firefox
echo   python advanced_auto_filler.py --headless
echo.
echo 📖 更多信息请查看 README.md 文件
echo 🔧 如有问题，请检查日志文件 cursor_agents_auto.log
echo.
pause