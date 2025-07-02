@echo off
chcp 65001 > nul
title MMFC-VIDEO

echo.
echo =====================================
echo 🎬 现代化视频播放器 v2.0
echo =====================================
echo.

echo 正在检查Python环境...
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ 错误: 未找到Python，请先安装Python 3.8或更高版本
    echo 下载地址: https://www.python.org/downloads/
    pause
    exit /b 1
)

echo ✅ Python环境检查通过
echo.

echo 正在启动现代化视频播放器...
python run_mmfc_video.py

echo.
echo 播放器已关闭，感谢使用！
pause 