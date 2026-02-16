import sys
import os
import platform
import subprocess
import locale
import getpass

def get_sys_info():
    """获取系统信息，适配 Python 3.11+"""
    os_type = platform.system()
    os_ver = platform.release()
    
    try:
        # 优先使用新版 getlocale，失败则回退
        lang = locale.getlocale()[0] or "en_US"
    except:
        lang = "en_US"
        
    shell = os.environ.get('SHELL', 'cmd' if os_type == 'Windows' else 'bash')
    return os_type, os_ver, lang, shell

def check_and_install_ollama(os_type):
    """检测 Ollama 状态，若未安装则阻止运行并提示"""
    try:
        subprocess.run(['ollama', '--version'], capture_output=True, check=True)
    except (FileNotFoundError, subprocess.CalledProcessError):
        print("\n" + "!"*40)
        print("[错误] 未检测到 AI 引擎 (Ollama)")
        print("-" * 40)
        if os_type == "Windows":
            print("1. 请确保已安装并启动 Ollama: https://ollama.com")
            print("2. 如果刚安装好，请重启 CMD 窗口或重启电脑。")
        elif os_type == "Darwin":
            print("请下载并运行 Mac 版 Ollama: https://ollama.com")
        else:
            print("请运行: curl -fsSL https://ollama.com/install.sh | sh")
        print("!"*40 + "\n")
        
        # 如果是双击运行的，留住窗口让用户看清楚错误
        if len(sys.argv) == 1:
            input("按回车键退出...")
        sys.exit(1)

def run_ach():
    os_type, os_ver, lang, shell = get_sys_info()
    
    # 基础用法提示
    if len(sys.argv) < 2:
        print(f"--- ACH AI 助手 (已就绪) ---")
        print(f"系统: {os_type} | 语言: {lang} | 环境: {shell}")
        print(f"\n用法举例:")
        print(f"  ach 帮我创建一个名为 '我的文档' 的文件夹")
        print(f"  ach 查找当前目录下所有大的图片文件")
        
        # 防止双击闪退
        input("\n按回回车键退出...")
        return

    # 检查 AI 引擎
    check_and_install_ollama(os_type)
    
    user_query = " ".join(sys.argv[1:])
    
    # 构造强力 Prompt，强制 AI 遵守规则
    prompt = (f"You are a system expert for {os_type} {os_ver}. Current user is '{getpass.getuser()}'. "
              f"System Language: {lang}. Shell: {shell}. "
              f"Task: {user_query}. "
              f"IMPORTANT: Output ONLY the raw shell command. "
              f"No explanations, no Markdown code blocks (```), no backticks.")

    try:
        print("AI 思考中...", end="\r")
        # 调用本地轻量模型
        result = subprocess.run(
            ['ollama', 'run', 'qwen2.5-coder:0.5b', prompt],
            capture_output=True, text=True, encoding='utf-8'
        )
        
        # 1. 过滤掉 AI 可能会带出的 Markdown 标记和杂质
        raw_output = result.stdout.strip()
        command = raw_output.replace('```cmd', '').replace('```', '').replace('`', '').strip()
        
        # 2. 如果 AI 输出了多行（可能带了解释），只取第一行有效命令
        command = command.split('\n')[0]

        # 3. 自动纠正常见的占位符错误
        command = command.replace('YourUsername', getpass.getuser())
        command = command.replace('<YourUsername>', getpass.getuser())

        if not command:
            print("AI 没能给出有效的命令，请换一种说法。")
            return

        # 显示建议（不带颜色代码以防旧版 CMD 乱码）
        print(f"\n[AI 建议命令]: {command}")
        
        confirm = input("是否立即执行? (y/n): ").lower()
        if confirm == 'y':
            # 执行命令
            os.system(command)
        else:
            print("已取消。")
            
    except Exception as e:
        print(f"\n发生错误: {e}")
        if len(sys.argv) == 1:
            input("按回车键退出...")

if __name__ == "__main__":
    run_ach()