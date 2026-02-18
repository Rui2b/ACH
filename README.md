# 🤖 ACH (AI Command Helper) - Make Your Terminal Understand Human Language

Chinese Version ---> [README](https://github.com/Rui2b/ACH/blob/main/readme/zh_cn-README.md)

**ACH** is a native AI command-line tool designed for efficiency (and laziness). It encapsulates a **500 million-parameter AI brain** directly within the program.

No Python environment installation required, no complex Ollama configuration needed, no internet connection required. With just a single binary file, you can command your Windows, Linux, or macOS to perform system tasks using "natural language."

---

## 🌟 Key Highlights: Why Choose ACH?

* **📦 Zero Dependencies, Double-Click to Use**: No runtime libraries or environments need to be installed; truly "unzip and use."

* **🔒 Privacy First**: 100% local inference. Your commands, paths, and private filenames never leave your computer.

* **🧠 Built-in Brain**: Integrates the lightweight `Qwen2.5-0.5B` model, specifically tuned for system commands.

* **⚡ Extremely Lightweight**: Requires only about 500MB of memory to run smoothly, even on older computers.

* **🌍 Cross-Platform Support**: One codebase works on three platforms.

---

## 🛠️ Installation and Usage Guide

### 1. Download the Program
Go to the [Releases](https://github.com/Rui2b/ACH/releases) page to download the latest compressed package suitable for your system:

* **Windows**: `ach-windows.zip`

* **Linux**: `ach-ubuntu.zip`

* **macOS**: `ach-macos.zip`

### 2. Quick Start

#### **Windows (CMD / PowerShell)** After decompression, you will get `ach.exe`.

`cmd ach` creates a "Test" folder on my desktop.

Linux / macOS (Terminal) After downloading, you need to grant execute permissions (only once):

Bash
## Grant permissions
chmod +x ach_linux # macOS users please replace with ach_macos

## Run command
./ach_linux "Find all video files larger than 100MB in the current directory"

## ⚠️ Pitfalls and Precautions

Loading Wait: Because the AI ​​model needs to be loaded from the hard drive into memory, there may be no response for the first 3-5 seconds after the program starts. This is normal, please wait a moment.

File Size: Because we have packaged the entire AI model file, the program size is around 400MB - 500MB. Although this is large, it brings the ultimate convenience of "offline usability".

Second Confirmation: AI is not omnipotent. Before pressing 'y' to execute, please be sure to check whether the AI-suggested commands are safe to avoid accidentally deleting important data.


Model limitations: The built-in 0.5B model excels at file handling, directory operations, and system status queries. However, it may struggle with complex Python scripts due to insufficient processing power.




