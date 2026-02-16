import sys
import os
import platform
import subprocess
import locale
import getpass
import re

def get_sys_info():
    os_type = platform.system()
    os_ver = platform.release()
    try:
        # 自动识别系统区域设置，防止中文系统报错
        lang = locale.getdefaultlocale()[0] or "en_US"
    except:
        lang = "en_US"
    shell = os.environ.get('SHELL', 'cmd' if os_type == "Windows" else "bash")
    return os_type, os_ver, lang, shell

def clean_command(raw_text, current_user):
    """【核心预防】彻底清理 AI 输出的干扰项"""
    # 1. 移除 Markdown 代码块标记（```cmd 等）
    text = re.sub(r'```[a-zA-Z]*', '', raw_text)
    # 2. 移除反引号
    text = text.replace('`', '').strip()
    
    # 3. 只取第一行有效内容（防止 AI 在后面写解释说明）
    lines = [line.strip() for line in text.split('\n') if line.strip()]
    if not lines: return ""
    
    cmd = lines[0]
    # 4. 【关键修复】自动将 AI 瞎编的用户名占位符替换为你的真实用户名 (例如 fang)
    cmd = cmd.replace('YourUsername', current_user).replace('<YourUsername>', current_user)
    return cmd

def run_ach():
    os_type, os_ver, lang, shell = get_sys_info()
    current_user = getpass.getuser()

    # 无参数运行保护：显示信息并防止双击直接关窗
    if len(sys.argv) < 2:
        print(f"--- ACH AI 助手 v1.2 (防御增强版) ---")
        print(f"当前系统: {os_type} | 登录用户: {current_user}")
        print("\n用法举例: ach 帮我在桌面创建一个测试文件夹")
        if os_type == "Windows": 
            input("\n按回车退出...")
        return

    # 检测 Ollama 引擎状态
    try:
        subprocess.run(['ollama', '--version'], capture_output=True, check=True)
    except:
        print("\n[!] 错误: 未检测到 Ollama 引擎。")
        print("请确保已安装 Ollama 并且右下角托盘中有“小羊驼”图标运行。")
        if os_type == "Windows": input("按回车退出...")
        sys.exit(1)

    query = " ".join(sys.argv[1:])
    
    # 精简 Prompt 约束 AI，只输出命令
    prompt = (f"System: {os_type}. User: {current_user}. Task: {query}. "
              "Rule: Output ONLY the raw executable command string. No markdown, no explanation.")

    try:
        print("AI 正在思考并生成命令...", end="\r")
        # 调用本地 0.5b 模型
        res = subprocess.run(
            ['ollama', 'run', 'qwen2.5-coder:0.5b', prompt],
            capture_output=True, text=True, encoding='utf-8', timeout=20
        )
        
        final_cmd = clean_command(res.stdout, current_user)

        if not final_cmd:
            print("\n[!] AI 没能生成有效命令，请尝试描述得更具体。")
            return

        print(f"\n[AI 建议执行]: {final_cmd}")
        confirm = input("是否执行? (y/n): ").lower()
        
        if confirm == 'y':
            # 【终极修复】使用 shell=True 确保命令直接在 Windows CMD 环境中生效
            # 这能解决“只弹出 PowerShell 窗口却不执行具体动作”的问题
            subprocess.run(final_cmd, shell=True)
            print("\n[√] 命令执行请求已发送。")
        else:
            print("已取消执行。")
            
    except Exception as e:
        print(f"\n[!] 运行时报错: {e}")
        if os_type == "Windows": input("按回车退出...")

if __name__ == "__main__":
    run_ach()
