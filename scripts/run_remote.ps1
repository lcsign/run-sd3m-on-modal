# 切换到脚本所在目录
Set-Location -Path (Split-Path -Parent $MyInvocation.MyCommand.Definition)

Write-Host "🚀 部署到 Modal..."
modal deploy ../app.py

Write-Host "🎨 运行 Stable Diffusion 3 Medium 推理..."
modal run ../app.py::run_sd3 --prompt "a futuristic cityscape at sunset" --steps 30 --width 1024 --height 1024
