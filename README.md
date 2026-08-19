# 快捷启动（Disk Link）

一个用于管理和启动移动硬盘内 Windows 程序的命令行工具。程序会保存应用名称与相对路径，因此移动硬盘盘符发生变化后，已登记的应用仍可通过名称启动。

## 运行环境

- Windows
- Python 3
- 与本项目位于同一磁盘的 `.exe` 程序

## 安装

建议在项目专用虚拟环境中安装依赖：

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

## 启动

```powershell
python disk_link.py
```

启动后可输入命令，也可以直接输入已经登记的应用名称来运行程序。

## 常用示例

登记一个应用：

```text
append vscode at F:\Software\Microsoft VS Code\Code.exe
```

随后可直接输入应用名称启动：

```text
vscode
```

查看或删除已登记的应用：

```text
list
del vscode
```

## 命令说明

| 命令 | 作用 |
| --- | --- |
| `language cn` | 切换为中文 |
| `language en` | 切换为英文 |
| `help` | 显示全部帮助 |
| `help <命令或应用名>` | 查看指定命令或应用信息 |
| `append <应用名> at <exe路径>` | 登记应用 |
| `del <应用名>` | 删除已登记的应用 |
| `list` | 列出全部应用及路径 |
| `jump <应用名>` | 在文件资源管理器中打开应用所在目录 |
| `check` | 检查并尝试修复必要的数据文件 |
| `quit` | 退出程序 |

应用名称不能与命令重名；登记目标必须是与本项目位于同一磁盘的 `.exe` 文件。

## 项目结构

- `disk_link.py`：程序入口和主要功能。
- `errors.py`：数据文件检查与错误修复。
- `output.py`：彩色终端输出。
- `lang/`：中英文提示文本。
- `appls.json`：已登记应用的数据文件。
- `errors.txt`：错误记录文件。
- `快捷启动.py`：用于特定硬盘目录结构的快捷入口，使用前需按实际安装路径调整。

## 说明

`appls.json` 和 `errors.txt` 属于本地运行数据，默认不会提交到 Git。建议定期备份 `appls.json`，避免登记信息丢失。

原作者：[ALAN-yichihann](https://github.com/ALAN-yichihann)
