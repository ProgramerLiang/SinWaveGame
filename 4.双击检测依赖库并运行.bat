@echo off
title ��Ϸ�����Զ����𹤾�
color 0B
echo "=========================================="
echo "|                Developed by Corripo                    |"
echo "|  Please read README.md before running  |"
echo "| Double-click ˫������.bat to run program |"
echo "=========================================="
echo ====== ��Ϸ������ʼ�� ======
echo ��ǰʱ�䣺%date% %time%
echo.

:: ���Python����
where python >nul 2>&1
if %errorlevel% neq 0 (
    echo [����] δ��⵽Python������
    echo ����� https://www.python.org/downloads/ ��װPython3.x
    echo ��װʱ��ع�ѡ"Add Python to PATH"ѡ��
    pause
    exit /b
)

:: ��֤pip������
python -m pip --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [����] pip��������δ��ȷ��װ
    echo ���ڳ����޸�pip����...
    python -m ensurepip --default-pip
)

:: ���þ���Դ���٣��廪��ѧԴ��
python -m pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple
python -m pip config set global.trusted-host pypi.tuna.tsinghua.edu.cn

:: ��װ��Ϸ�����⣨ʾ����װPygame��
echo ���ڼ����Ϸ������...
python -c "import pygame" >nul 2>&1
if %errorlevel% neq 0 (
    echo ���ڰ�װ��Ϸ�������...
    call python -m pip install pygame==2.5.0 --user
    if %errorlevel% neq 0 (
        echo [����] �����ⰲװʧ�ܣ�
        pause
        exit /b
    )
)

:: ������Ϸ������
echo ====== ����������Ϸ ======
start "" python main.py
exit
