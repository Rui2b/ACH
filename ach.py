import sys
import os
import platform
import subprocess
import locale
import getpass
import re

def get_sys_info():
    """环境自动侦测"""
    os_type = platform.system()
    os_ver = platform.release()
    # 强制获取控制台编码，防止中文环境下执行命令乱码
    system_encoding = locale.getpreferredencoding()
    shell = os.environ.get('SHELL', 'cmd' if os_type == "Windows" else "bash")
    return os_type, os_ver, system_encoding, shell

def clean_ai_command(raw_text, current_user):
    """防呆过滤：剔除所有可能导致执行失败的杂质"""
    # 1. 移除 Markdown 代码块标记、反引号和转义符
    clean = re.sub(r'```[a-zA-Z]*', '', raw_text)
    clean = clean.replace('`', '').replace('\\', '/') if platform.system() != "Windows" else clean.replace('`', '')
    
    # 2. 只取有效的第一行（防止 AI 后面写一堆解释）
    lines = [l.strip() for l in clean.split('\n') if l.strip()]
    if not lines: return ""
    command = lines[0]

    # 3. 关键修复：自动纠正用户名占位符 (防止 AI 乱写 YourUsername)
    command = command.replace('YourUsername', current_user).replace('<YourUsername>', current_user)
    
    return command

def check_ollama():
    """预防性检查：确保 Ollama 在后台运行"""
    try:
        # 尝试静默运行命令，检查返回码
        subprocess.run(['ollama', '--version'], capture_output=True, check=True)
        return True
    except:
        return False

def run_ach():
    os_type, os_ver, encoding, shell = get_sys_info()
    current_user = getpass.getuser()

    # 1. 无参数运行提示 (增加 input 防止闪退)
    if len(sys.argv) < 2:
        print(f"--- ACH AI 助手 (v1.3 铁甲版) ---")
        print(f"环境: {os_type} | 用户: {current_user} | 编码: {encoding}")
        print("\n用法举例: ach 帮我在桌面创建一个测试文件夹")
        if os_type == "Windows":
            input("\n按回车退出...")
        return

    # 2. Ollama 状态检查
    if not check_ollama():
        print("\n[!] 错误: 未检测到 AI 引擎 (Ollama)")
        print("请确保 Ollama 已启动（右下角有小羊驼图标）。")
        if os_type == "Windows":
            input("按回车退出...")
        sys.exit(1)

    user_query = " ".join(sys.argv[1:])
    
    # 3. Prompt 深度优化：强制 AI 闭嘴只给命令，并明确用户路径
    prompt = (f"Context: {os_type} {os_ver}, User {current_user}, Shell {shell}. "
              f"Task: {user_query}. "
              f"Instruction: Output ONLY the one-line raw command. "
              f"No markdown, no quotes, no explanations.")

    try:
        print("AI 思考中...", end="\r")
        # 增加 15 秒超时控制
        result = subprocess.run(
            ['ollama', 'run', 'qwen2.5-coder:0.5b', prompt],
            capture_output=True, text=True, encoding='utf-8', timeout=15
        )
        
        command = clean_ai_command(result.stdout, current_user)

        if not command:
            print("\n[!] AI 生成了空命令，请换个描述试试。")
            return

        print(f"\n[AI 建议]: {command}")
        confirm = input("确认执行? (y/n): ").lower()
        
        if confirm == 'y':
            # 4. 最终执行：使用 shell=True 以确保能运行系统内置命令
            process = subprocess.run(command, shell=True)
            if process.returncode == 0:
                print("\n[√] 执行成功")
            else:
                print(f"\n[!] 执行失败，错误代码: {process.returncode}")
        else:
            print("已取消。")
            
    except subprocess.TimeoutExpired:
        print("\n[!] 错误: AI 响应超时，请检查 Ollama 状态。")
    except Exception as e:
        print(f"\n[!] 发生未知错误: {e}")
        if os_type == "Windows": input("按回车退出...")

if __name__ == "__main__":
    run_ach()