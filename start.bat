@echo off
setlocal enabledelayedexpansion
set PYTHONIOENCODING=utf-8
chcp 65001 >nul

set PROMPT=A dity dog
set WIDTH=768
set HEIGHT=768
set STEPS=28

:: 推理（输出交给 PowerShell 转码，避免 GBK 炸掉）
modal run app.py::run_sd3 --prompt "%PROMPT%" --width %WIDTH% --height %HEIGHT% --steps %STEPS% 2>&1 | powershell -Command "$input | Out-String"

:: 下载最新结果
modal volume get sd3-model-cache /output.png ./output.png --force

echo 生成完成，已保存到 output.png
pause




