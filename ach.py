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
        # 如果是打包后的 exe，模型在内部临时文件夹
        base_path = sys._MEIPASS
    else:
        # 如果是直接运行脚本，模型在当前目录
        base_path = os.path.dirname(__file__)
    
    return os.path.join(base_path, "model.gguf")

def clean_command(raw_text, current_user):
    # 这里的过滤逻辑保持不变
    text = re.sub(r'```[a-zA-Z]*', '', raw_text)
    text = text.replace('`', '').strip()
    lines = [line.strip() for line in text.split('\n') if line.strip()]
    if not lines: return ""
    cmd = lines[0]
    if "创建" in sys.argv[1:].__str__() and cmd.lower().startswith("cd "):
        cmd = cmd.replace("cd ", "md ", 1)
    cmd = cmd.replace('YourUsername', current_user).replace('<YourUsername>', current_user)
    return cmd

def run_ach():
    current_user = getpass.getuser()
    model_path = get_model_path()

    if not os.path.exists(model_path):
        print(f"[!] 错误: 找不到模型文件 {model_path}")
        if platform.system() == "Windows": input("按回车退出..."); 
        return

    if len(sys.argv) < 2:
        print(f"--- ACH AI 助手 (一体化离线版) ---")
        print(f"用户: {current_user} | 模型: Qwen 0.5B 内置")
        if platform.system() == "Windows": input("\n按回车退出...")
        return

    query = " ".join(sys.argv[1:])
    
    prompt = (f"<|im_start|>system\nYou are a Windows CMD expert. User: {current_user}. "
              "Output ONLY the one-line raw command. No markdown.<|im_end|>\n"
              f"<|im_start|>user\nTask: {query}<|im_end|>\n"
              "<|im_start|>assistant\n")

    try:
        # 初始化内置模型
        print("AI 引擎启动中 (首次运行可能较慢)...", end="\r")
        llm = Llama(model_path=model_path, n_ctx=512, verbose=False)
        
        print("AI 正在思考命令...            ", end="\r")
        output = llm(prompt, max_tokens=64, stop=["<|im_end|>"], echo=False)
        raw_res = output['choices'][0]['text']
        
        final_cmd = clean_command(raw_res, current_user)

        if not final_cmd:
            print("\n[!] AI 没能理解指令。")
            return

        print(f"\n[AI 建议]: {final_cmd}")
        confirm = input("确认执行? (y/n): ").lower()
        
        if confirm == 'y':
            subprocess.run(final_cmd, shell=True)
            print("\n[√] 任务已处理。")
        else:
            print("已取消。")
            
    except Exception as e:
        print(f"\n[!] 发生错误: {e}")
        if platform.system() == "Windows": input("按回车退出...")

if __name__ == "__main__":
    run_ach()
