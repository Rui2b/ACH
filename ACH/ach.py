import sys
import os
import platform
import getpass
import re
import subprocess
from llama_cpp import Llama  # 核心：直接在进程内运行 AI

def get_model_path():
    """获取模型路径，适配 PyInstaller 打包后的路径"""
    if getattr(sys, 'frozen', False):
        # 如果是打包后的 exe/binary，模型在内部临时文件夹
        base_path = sys._MEIPASS
    else:
        # 如果是直接运行脚本，模型在当前目录
        base_path = os.path.dirname(__file__)
    
    return os.path.join(base_path, "model.gguf")

def clean_command(raw_text, current_user, os_type):
    """清洗 AI 输出的垃圾字符"""
    # 移除 Markdown 代码块标记
    text = re.sub(r'```[a-zA-Z]*', '', raw_text)
    text = text.replace('`', '').strip()
    
    # 只取第一行非空内容
    lines = [line.strip() for line in text.split('\n') if line.strip()]
    if not lines: return ""
    cmd = lines[0]
    
    # 针对中文常有的“创建”指令误判为“cd”的修复 (跨平台适配)
    if "创建" in sys.argv[1:].__str__() and cmd.lower().startswith("cd "):
        if os_type == "Windows":
            cmd = cmd.replace("cd ", "md ", 1)
        else:
            cmd = cmd.replace("cd ", "mkdir -p ", 1)
        
    # 替换通用的占位符
    cmd = cmd.replace('YourUsername', current_user).replace('<YourUsername>', current_user)
    return cmd

def run_ach():
    current_user = getpass.getuser()
    os_type = platform.system() # Windows, Linux, Darwin
    model_path = get_model_path()

    if not os.path.exists(model_path):
        print(f"[!] 错误: 找不到模型文件 {model_path}")
        if os_type == "Windows": input("按回车退出..."); 
        return

    if len(sys.argv) < 2:
        print(f"--- ACH AI 助手 (跨平台离线版) ---")
        print(f"系统: {os_type} | 用户: {current_user} | 模型: Qwen 0.5B")
        print(f"用法: ach <你的指令>")
        if os_type == "Windows": input("\n按回车退出...")
        return

    query = " ".join(sys.argv[1:])
    
    # 根据系统动态生成专家身份
    shell_name = "Windows CMD" if os_type == "Windows" else "Linux Bash"
    path_example = "C:\\Users\\name" if os_type == "Windows" else "/home/name"
    
    # 【全平台防傻补丁版 Prompt】
    prompt = (
        f"<|im_start|>system\n"
        f"You are a {shell_name} expert. Current User: {current_user}. OS: {os_type}.\n"
        f"Strict Rules to prevent mistakes:\n"
        f"1. DIRECT COMMAND ONLY: Output only the raw command string. No markdown, no intro.\n"
        f"2. NO DESTRUCTIVE PRE-STEPS: Never use 'rm' or 'del' before creating something unless explicitly asked.\n"
        f"3. SPACE HANDLING: Always wrap paths in double quotes (e.g., \"{path_example}\\folder name\").\n"
        f"4. NO PLACEHOLDERS: Use the actual User: {current_user} or the absolute path. Never use <User>.\n"
        f"5. NATIVE COMMANDS: If Windows, use 'dir', 'move', 'copy'. If Linux, use 'ls', 'mv', 'cp'.\n"
        f"6. NO EXPLANATION: If unsure, output nothing. Do not ask for clarification.\n"
        f"7. SINGLE LINE: Do not use line breaks. Output a single executable string.<|im_end|>\n"
        f"<|im_start|>user\nTask: {query}<|im_end|>\n"
        f"<|im_start|>assistant\n"
    )

    try:
        # 初始化内置模型
        print(f"AI 引擎启动中 ({os_type})...", end="\r")
        llm = Llama(model_path=model_path, n_ctx=512, verbose=False)
        
        print("AI 正在思考命令...            ", end="\r")
        output = llm(prompt, max_tokens=100, stop=["<|im_end|>", "\n"], echo=False)
        raw_res = output['choices'][0]['text']
        
        final_cmd = clean_command(raw_res, current_user, os_type)

        if not final_cmd:
            print("\n[!] AI 没能理解指令或指令可能不安全。")
            return

        print(f"\n[AI 建议]: {final_cmd}")
        confirm = input("确认执行? (y/n): ").lower()
        
        if confirm == 'y':
            # 执行命令
            result = subprocess.run(final_cmd, shell=True)
            if result.returncode == 0:
                print("\n[√] 任务已完成。")
            else:
                print(f"\n[!] 执行返回错误码: {result.returncode}")
        else:
            print("操作已取消。")
            
    except Exception as e:
        print(f"\n[!] 运行异常: {e}")
        if os_type == "Windows": input("按回车退出...")

if __name__ == "__main__":
    run_ach()
