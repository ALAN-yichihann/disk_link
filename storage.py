class Storage:
    def __init__(self):
        # 设置中英文提示语
        self.CN_PROMPTS = (
            "请输入你想要执行的硬盘内程序或命令:",
            "此程序或命令不存在，或命令格式不正确。",
            "已修改语言为中文。",
            "你觉得这样很好玩？",
            "此程序名已存在，请更换注册名称。",
            "此路径下找不到指定程序。",
            "此路径与已有路径冲突。",
            "此路径不在硬盘中。",
            "您是否确认添加程序快捷方式？(Y/n):",
            "文件后缀应为.exe。",
            "成功添加应用程序。",
            "添加终止。",
            "此程序不存在。",
            "成功删除应用程序快捷方式。",
            "您是否确认删除该程序快捷方式？(Y/n):",
            "删除终止。",
            "以下是可使用的程序列表及对应路径:",
            "找不到应用文件！",
            "存储数据读取错误！",
            "找不到错误记录文件！",
            "已修复，需要重新添加所有快捷方式。",
            "已修复，但丢失了之前所有错误记录。",
            "程序名不得与命令名冲突。",
            "当前无任何快捷方式。",
            "应用与路径存储出现错误！",
            "已修复，并恢复至备份状态。请输入“list”查看受损情况。",
            "必要文件无问题。",
            "程序不存在，路径可能已经被修改或移动。请输入“list”查看各程序路径，并依次用“del”和“append”删除和添加快捷方式。"
        )
        self.EN_PROMPTS = (
            "Please enter the application or command you'd like to run in the disk:",
            "The application or command do not exist, or the format is incorrect.",
            "Language set English.",
            "You think this funny?",
            "The application name already exists, please choose another name.",
            "The application does not exist in the directory.",
            "The directory conflicts with an existing directory.",
            "The directory is not in the disk.",
            "Are you sure to append the application shortcut?(Y/n):",
            "The filename extension should be .exe .",
            "Application appended successfully.",
            "Aborted.",
            "The application does not exist.",
            "Application shortcut successfully deleted.",
            "Are you sure to delete the application shortcut?(Y/n):",
            "Aborted.",
            "These are usable programs and their routes respectively:",
            "Cannot find application file!",
            "Error while reading storage!",
            "Cannot find error recording file!",
            "Repaired and requiring adding all applications again.",
            "Repaired but all previous error records are lost.",
            "Application name must not conflict with any command.",
            "No shortcuts added.",
            "Error in application and directory storage!",
            """Repaired and recovered to saved state. Please enter "list" to check the damage.""",
            "No problem with necessary files.",
            """Program does not exist. The route could have been modified or moved. Please  enter "list" to check routes of applications, and use "del" and "append" to delete and append shortcuts successively."""
        )

        # 设置中英文命令提示语
        self.COMMAND_HELPS_CN = (
            "language [lang] | 设置语言，cn为中文，en为英文。",
            "quit | 退出程序。",
            "help [ /cmd/appl] | 获取帮助。",
            "append [appl] at [dir] | 添加新程序快捷方式。",
            "del [appl] | 删除程序快捷方式。",
            "list | 列出所有程序及路径。",
            "jump [appl] | 跳到对应文件资源管理器页面。",
            "check | 检查必要文件是否缺失。"
        )
        self.COMMAND_HELPS_EN = (
            "language [lang] | Set language, cn for Chinese, en for English.",
            "quit | Exit program.",
            "help [ /cmd/appl] | Get help.",
            "append [appl] at [dir] | Append new application shortcut.",
            "del [appl] | Delete application shortcut.",
            "list | List all applications and routes.",
            "jump [appl] | Open explorer page of the application.",
            "check | Check if vital files are lost."
        )

        # 设置中英文全部命令提示语
        self.ALL_HELPS_CN = """以下是可用命令及输入格式:
        language [lang]        | 设置语言，cn为中文，en为英文。
        quit                   | 退出程序。
        help [ /cmd/appl]      | 获取帮助。
        append [appl] at [dir] | 添加新程序快捷方式。
        del [appl]             | 删除程序快捷方式。
        list                   | 列出所有程序及路径。
        jump [appl]            | 跳到此程序对应文件资源管理器页面。
        check                  | 检查必要文件是否缺失。"""
        self.ALL_HELPS_EN = """These are usable commands and input formats:
        language [lang]        | Set language, cn for Chinese, en for English.
        quit                   | Exit program.
        help [ /cmd/appl]      | Get help.
        append [appl] at [dir] | Append new application shortcut.
        del [appl]             | Delete application shortcut.
        list                   | List all applications and routes.
        jump [appl]            | Open explorer page of the application.
        check                  | Check if vital files are lost."""