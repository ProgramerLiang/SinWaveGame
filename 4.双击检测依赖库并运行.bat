@echo off
title 游戏环境自动部署工具
color 0B
echo "=========================================="
echo "|                Developed by Corripo                    |"
echo "|  Please read README.md before running  |"
echo "| Double-click 双击运行.bat to run program |"
echo "=========================================="
echo ====== 游戏环境初始化 ======
echo 当前时间：%date% %time%
echo.

:: 检测Python环境
where python >nul 2>&1
if %errorlevel% neq 0 (
    echo [错误] 未检测到Python环境！
    echo 请访问 https://www.python.org/downloads/ 安装Python3.x
    echo 安装时务必勾选"Add Python to PATH"选项
    pause
    exit /b
)

:: 验证pip可用性
python -m pip --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [警告] pip包管理器未正确安装
    echo 正在尝试修复pip环境...
    python -m ensurepip --default-pip
)

:: 配置镜像源加速（清华大学源）
python -m pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple
python -m pip config set global.trusted-host pypi.tuna.tsinghua.edu.cn

:: 安装游戏依赖库（示例安装Pygame）
echo 正在检测游戏依赖库...
python -c "import pygame" >nul 2>&1
if %errorlevel% neq 0 (
    echo 正在安装游戏引擎组件...
    call python -m pip install pygame==2.5.0 --user
    if %errorlevel% neq 0 (
        echo [错误] 依赖库安装失败！
        pause
        exit /b
    )
)

:: 启动游戏主程序
echo ====== 正在启动游戏 ======
start "" python main.py
exit
