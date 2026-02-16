# 🚀 ACH (AI Command Helper) 
**让命令行说“人话”。**

ACH 是一个超轻量级的命令行工具，专为小白设计。你只需用自然语言描述你想干什么，ACH 就会自动为你生成并运行对应的系统命令。

---

## ✨ 核心特性

* 🆓 **完全免费**：不调用任何收费 API，基于 Ollama 本地运行，一分钱都不用花。
* 🔒 **隐私安全**：所有指令都在你本地电脑处理，不会上传到任何服务器。
* 🌍 **智能识别**：
    * 自动识别操作系统（Windows, Linux, macOS, FreeBSD, ChromeOS）。
    * 自动识别系统语言（中文、英文等）。
    * 自动匹配终端类型（CMD, PowerShell, Bash, Zsh）。
* 🪶 **极其轻量**：采用 0.5b 级 AI 模型，仅需约 300MB 内存即可流畅运行。

---

## 🛠️ 快速安装

### 第一步：安装 AI 引擎 (Ollama)
ACH 需要 Ollama 引擎来驱动本地 AI。
* **Windows/macOS**: 前往 [Ollama.com](https://ollama.com) 下载并安装。
* **Linux**: 执行 `curl -fsSL https://ollama.com/install.sh | sh`

### 第二步：下载 ACH
从本项目的 [Releases](../../releases) 页面下载对应系统的压缩包：
* **Windows**: 下载 `ach_windows.exe` 并将其放入 `C:\Windows`。
* **Linux/macOS**: 下载 `ach_linux` 或 `ach_macos`，运行 `sudo mv ach /usr/local/bin/ach`。

---

## 📖 使用指南

在任何终端（黑窗口）输入 `ach` 加上你想做的事。

### 常用例子：
| 输入示例 | AI 动作 (自动适配你的系统) |
| :--- | :--- |
| `ach 查看当前目录下最大的文件` | 生成 `du` 或 `dir` 命令并排序 |
| `ach 把这个文件夹打包成 zip` | 调用 `zip` 或 `Compress-Archive` |
| `ach 查找并杀死占用 8080 端口的进程` | 自动查找 PID 并执行 `kill` 或 `taskkill` |
| `ach 更新系统所有软件` | 自动识别 `apt`, `brew` 或 `dnf` |
| `ach 修改系统 IP 地址为静态` | 生成复杂的网络配置命令 |

---

## 📊 操作系统支持 (Operation Manual)

| 操作系统 | 架构支持 | 自动语言识别 | 依赖要求 |
| :--- | :--- | :--- | :--- |
| **Windows 10/11** | x86/ARM | ✅ 支持 | Ollama Windows |
| **macOS (Intel/M1/M2)** | Universal | ✅ 支持 | Ollama Mac |
| **Linux (All Distros)** | x86/ARM/RISC-V | ✅ 支持 | Ollama Linux |
| **FreeBSD** | x86 | ✅ 支持 | pkg install ollama |
| **Chrome OS** | Linux Mode | ✅ 支持 | Ollama (Linux) |

---

## 👨‍💻 开发与编译
如果你想自行编译，请确保已安装 Python 3.11+：

```bash
# 安装打包工具
pip install pyinstaller

# 编译单文件
pyinstaller --onefile --name ach ach.py