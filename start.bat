@echo off
REM 运行生成图像
modal run app.py::run_sd3 --prompt "A dog" --width 768 --height 768 --steps 28

REM 下载结果到本地并覆盖
modal volume get sd3-model-cache /output.png ./output.png --force


