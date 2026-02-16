# 🚀 ACH (AI Command Helper)

**Make the command line speak "human language".**

ACH is an ultra-lightweight command-line tool designed for beginners. Simply describe what you want to do in natural language, and ACH will automatically generate and run the corresponding system commands for you.

---

## ✨ Core Features

* 🆓 **Completely Free**: It doesn't call any paid APIs, runs locally on Ollama, and costs absolutely nothing.

* 🔒 **Privacy and Security**: All commands are processed on your local computer and are not uploaded to any server.

* 🌍 **Intelligent Recognition**:

* Automatically recognizes the operating system (Windows, Linux, macOS, FreeBSD, ChromeOS).

* Automatically recognizes the system language (Chinese, English, etc.).

* Automatically matches the terminal type (CMD, PowerShell, Bash, Zsh).

* **Extremely Lightweight:** Utilizing a 0.5b level AI model, it runs smoothly with only approximately 300MB of memory.

---

## 🛠️ Quick Installation

### Step 1: Install the AI ​​Engine (Ollama)

ACH requires the Ollama engine to drive the local AI.

* **Windows/macOS**: Go to [Ollama.com](https://ollama.com) to download and install it.

* **Linux**: Execute `curl -fsSL https://ollama.com/install.sh | sh`

### Step 2: Download ACH Download the compressed package corresponding to your system from the [Releases](../../releases) page of this project:

* **Windows**: Download `ach_windows.exe` and place it in `C:\Windows`.

* **Linux/macOS**: Download `ach_linux` or `ach_macos`, and run `sudo mv ach /usr/local/bin/ach`.

---

## 📖 Usage Guide

In any terminal (black window), type `ach` followed by the command you want to execute.

### Common Examples:

| Input Example | AI Action (Automatically Adapts to Your System) |

| :--- | :--- |

| `ach` View the largest file in the current directory | Generate `du` or `dir` commands and sort them |

| `ach` Package this folder into a zip file | Invoke `zip` or `Compress-Archive` |

| `ach` Find and kill processes using port 8080 | Automatically find the PID and execute `kill` or `taskkill` |

| `ach` Update all system software | Automatically identify `apt`, `brew`, or `dnf` |

| `ach` Change the system IP address to static | Generate complex network configuration commands |

---

## 📊 Operating System Support (Operation Manual)

| Operating System | Architecture Support | Automatic Language Recognition | Dependency Requirements |

| :--- | :--- | :--- | :--- |

| **Windows 10/11** | x86/ARM | ✅ Supported | Ollama Windows |

| **macOS (Intel/M1/M2)** | Universal | ✅ Supported | Ollama Mac |

| **Linux (All Distros)** | x86/ARM/RISC-V | ✅ Supported | Ollama Linux |

| **FreeBSD** | x86 | ✅ Supported | pkg install ollama |

| **Chrome OS** | Linux Mode | ✅ Supported | Ollama (Linux) |

---

## 👨‍💻 Development and Compilation

If you want to compile it yourself, please ensure that Python 3.11+ is installed:

```bash

# Install packaging tools

pip install pyinstaller

# Compile a single file

pyinstaller --onefile --name ach ach.py