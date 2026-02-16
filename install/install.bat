@echo off
echo 正在检查并安装 AI 核心 (Ollama)...
powershell -Command "iex (iwr -useb https://ollama.com/install.ps1)"
echo 正在下载超轻量模型...
ollama pull qwen2.5-coder:0.5b
echo 安装完成！现在你可以直接在命令行使用 ach 命令了。
pause