#!/bin/bash
echo "正在安装 Ollama..."
curl -fsSL https://ollama.com/install.sh | sh
echo "拉取 AI 模型..."
ollama pull qwen2.5-coder:0.5b
echo "安装完成！"