import sys
import os
import platform
import subprocess
import locale

def get_sys_info():
    """获取系统信息：修复了 Python 3.15 的兼容性问题"""
    os_type = platform.system() # Windows, Linux, Darwin (Mac)
    os_ver = platform.release()
    
    # 修复 DeprecationWarning，适配新版 Python
    try:
        lang = locale.getlocale()[0] or "en_US"
    except:
        lang = "en_US"
        
    shell = os.environ.get('SHELL', 'cmd' if os_type == 'Windows' else 'bash')
    return os_type, os_ver, lang, shell

def check_and_install_ollama(os_type):
    """自动检测并指导安装，确保小白上手即用"""
    try:
        # 尝试静默检查版本
        subprocess.run(['ollama', '--version'], capture_output=True, check=True)
    except (FileNotFoundError, subprocess.CalledProcessError):
        print("\n[!] 错误：未检测到 AI 引擎 (Ollama)")
        print("-" * 40)
        if os_type == "Windows":
            print("1. 请前往官网下载安装包: https://ollama.com/download/windows")
            print("2. 安装完成后重新打开此窗口。")
        elif os_type == "Darwin":
            print("1. 请下载 Mac 版: https://ollama.com/download/mac")
            print("2. 解压并拖入应用程序文件夹。")
        else: # Linux / FreeBSD / ChromeOS
            print("请执行以下命令安装：")
            print("curl -fsSL https://ollama.com/install.sh | sh")
        print("-" * 40)
        sys.exit(1)

def run_ach():
    os_type, os_ver, lang, shell = get_sys_info()
    
    if len(sys.argv) < 2:
        print(f"--- ACH AI 助手 ---")
        print(f"系统: {os_type} {os_ver} | 语言: {lang} | 终端: {shell}")
        print(f"\n用法举例:")
        print(f"  ach 帮我把当前目录下的所有 png 转换成 jpg")
        print(f"  ach 查找超过 100MB 的文件并列出来")
        return

    check_and_install_ollama(os_type)
    user_query = " ".join(sys.argv[1:])
    
    # 构造针对该操作系统的专属 Prompt
    prompt = (f"You are a CLI expert for {os_type} ({os_ver}). Current shell: {shell}. "
              f"User language: {lang}. "
              f"Goal: {user_query}. "
              f"Instruction: Output ONLY the raw command. No explanations, no markdown code blocks.")

    try:
        # 使用 Qwen2.5-Coder 0.5B: 极其轻量 (约 300MB), 针对代码优化
        print("AI 正在思考中...", end="\r")
        result = subprocess.run(
            ['ollama', 'run', 'qwen2.5-coder:0.5b', prompt],
            capture_output=True, text=True, encoding='utf-8'
        )
        command = result.stdout.strip()
        
        if not command or "Error" in command:
            print("AI 无法理解该请求，请尝试换种说法。")
            return

        print(f"\n[建议命令]: \033[1;32m{command}\033[0m") # 绿色显示命令
        confirm = input("是否执行? (y/n): ").lower()
        if confirm == 'y':
            os.system(command)
            
    except Exception as e:
        print(f"\n运行出错: {e}")

if __name__ == "__main__":
    run_ach()
