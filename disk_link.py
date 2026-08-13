import os
import sys
import json

from output import print_info, print_warning, print_error, input_confirm
from typing import List, Any
from datetime import datetime

from storage import Storage

class DiskLink:
    """管理程序的类"""
    def __init__(self):
        """初始化"""

        # 输出提示语
        print("这是此硬盘中程序的快捷启动程序。")
        print("要将语言设置为中文，请输入 “language cn”。")
        print("要获得帮助，请输入 “help”。\n")
        print("This is a convenient program for running applications in the disk.")
        print("""To set the language English, enter "language en".""")
        print("""To get help, enter "help".\n""")
        print("正在初始化...")
        print("Initializing...\n")

        self.STORAGE = Storage()

        # 设置中英文提示语
        self.CN_PROMPTS = self.STORAGE.CN_PROMPTS
        self.EN_PROMPTS = self.STORAGE.EN_PROMPTS

        # 设置中英文命令提示语
        self.COMMAND_HELPS_CN = self.STORAGE.COMMAND_HELPS_CN
        self.COMMAND_HELPS_EN = self.STORAGE.COMMAND_HELPS_EN

        # 设置中英文全部命令提示语
        self.ALL_HELPS_CN = self.STORAGE.ALL_HELPS_CN
        self.ALL_HELPS_EN = self.STORAGE.ALL_HELPS_EN

        # 默认语言为中文
        self.language = "cn"
        self.prompts = self.CN_PROMPTS
        self.command_helps = self.COMMAND_HELPS_CN
        self.all_helps = self.ALL_HELPS_CN

        # 设置命令
        self.COMMANDS = ('language', 'quit', 'help', "append", "del", "list", "jump", "check")

        # 获取各种文件路径
        if getattr(sys, 'frozen', False):
            application_path = os.path.dirname(sys.executable)
            path_list = application_path.split(os.path.sep)
            path_list.pop(0)
        else:
            application_path = os.path.dirname(__file__)
            path_list = application_path.split(os.path.sep)
            path_list.pop(0)

        self.APPL_JSON_ROUTE = "\\".join(path_list) + '\\appls.json'
        self.ERROR_TXT_ROUTE = "\\".join(path_list) + '\\errors.txt'
        # print(path_list)
        # print(self.appl_txt_route)

        # 获取路径和硬盘名称
        self.DISK_NAME = application_path.split('\\')[0]

        # 输出程序位置
        print_info("当前程序位置:\nPresent Program Directory:\n" + application_path)

        self.ERROR_LIST = (
            "01010101(1)", # 应用文件丢失，无法修复
            "01010101(2)", # 应用文件丢失，可以修复
            "01010102(1)", # 读取错误，无法修复
            "01010102(2)", # 读取错误，可以修复
            "01010201", # 错误文件丢失
        )
        self.HANDLE_LIST = (
            (17, 20),
            (17, 25),
            (18, 20),
            (18, 25),
            (19, 21),
        )

        # 读取存储的应用和路径
        self.read_texts(True)

        # 备份
        self.create_save()

        # 设置质问的初数
        self.fun_num = 0

        # 删除无用变量
        del application_path
        del path_list

    def mainloop(self):
        """主进程"""
        while True:
            # 获取用户输入
            self.read_usr()

            # 检测是否输出质问
            if len(self.usr) == 0:
                self.funny_prompt()
                continue

            # 启动程序
            elif len(self.usr) == 1 and self.usr[0] in self.appls:
                self.fun_num = 0
                self.run_appl()

            # 执行命令
            elif len(self.usr) >= 1 and self.usr[0] in self.COMMANDS:
                self.fun_num = 0
                self.run_command()

            # 输出报错
            else:
                self.fun_num = 0
                print_warning(self.prompts[1])

    def read_texts(self, first_time=False):
        """读取应用和路径"""
        # 检查必要文件
        self.check_vitals(first_time)

        # 读取文件
        try:
            with open(self.DISK_NAME + "\\" + self.APPL_JSON_ROUTE) as f1:
                self.appls = json.load(f1)

        # 读取出错
        except json.decoder.JSONDecodeError:
            # 刚启动时无法修复
            if first_time:
                self.error_inform("01010102(1)")
                self.handle_error("01010102(1)")
            # 启动后可通过备份修复
            else:
                self.error_inform("01010102(2)")
                self.handle_error("01010101(2)")

    def run_appl(self):
        try:
            os.startfile(self.DISK_NAME + self.appls[self.usr[0]])
        except FileNotFoundError:
            print_warning(self.prompts[27])

    def run_command(self):
        """执行命令"""
        # 语言命令
        if self.usr[0] == self.COMMANDS[0] and len(self.usr) == 2:
            self.sub_language()

        # 退出命令
        elif self.usr[0] == self.COMMANDS[1] and len(self.usr) == 1:
            sys.exit(0)

        # 输出帮助
        elif self.usr[0] == self.COMMANDS[2]:
            self.print_help()

        # 添加软件
        elif self.usr[0] == self.COMMANDS[3]:
            self.append_appl()

        # 删除软件
        elif self.usr[0] == self.COMMANDS[4] and len(self.usr) == 2:
            self.del_appl()

        # 输出软件
        elif self.usr[0] == self.COMMANDS[5] and len(self.usr) == 1:
            self.list_appl()

        # 跳转文管
        elif self.usr[0] == self.COMMANDS[6] and len(self.usr) == 2:
            self.jump_route()

        # 自检问题
        elif self.usr[0] == self.COMMANDS[7] and len(self.usr) == 1:
            self.check_vitals(command=True)

        # 输出报错
        else:
            print(self.prompts[1])

    def _max_len(self):
        """求列表中所有字符串最长值，默认值10"""
        max = 0
        for key in self.appls.keys():
            if len(key) > max:
                max = len(key)
        if max < 10:
            max = 10
        return max

    def _print_appls(self, max):
        """输出所有应用"""
        for key in self.appls.keys():
            # 输出程序名
            print_info(key, end='')

            # 输出合适数量的空格
            for j in range(max - len(key)):
                print_info(' ', end='')

            # 输出应用路径
            print_info('| ', end='')
            print_info(self.DISK_NAME + self.appls[key])

    def _print_appl(self, key):
        """输出特定程序路径"""
        print_info(key + " | " + self.DISK_NAME + self.appls[key])

    def funny_prompt(self):
        """检测是否输出质问"""
        # 逐个递增
        self.fun_num += 1

        # 连续十次就输出并归零
        if self.fun_num == 10:
            print_warning(self.prompts[3])
            self.fun_num = 0

    def read_usr(self):
        """读取和分割用户输入"""
        self.usr = input(self.prompts[0])

        # 列表化用户输入
        usr = list(self.usr)

        # 初始化编辑后内容
        usr_edited: List[Any] = []

        # 当前编辑
        current = ''

        # 初始化标志
        flag = False # 是否需要添加
        exit_flag = False # 是否需要退出总循环

        # 遍历每个字符
        for i in range(len(usr)):

            # 非空格则加到当前编辑字符串
            if usr[i] != ' ':
                current += usr[i]
                flag = True

            # 是空格则添加并重置当前编辑字符串和标志
            elif flag:
                usr_edited.append(current)
                current = ''
                flag = False

            # 若有at存在，保护其后内容
            if len(usr_edited) > 1:
                if usr_edited[-1] == 'at':

                    # 遍历找到at后第一个非空格字符
                    for j in range(len(usr) - i - 1):
                        if usr[j + i + 1] != ' ':

                            # 从此位置开始保护
                            protect = j + i + 1
                            protected = ''.join(usr[protect:])
                            usr_edited.append(protected)

                            # 退出寻找循环和总字符循环
                            exit_flag = True
                            break

            # 退出总字符循环
            if exit_flag:
                break

        # 若当前编辑内容不是空，则添加
        if current != '':
            usr_edited.append(current)

        # 重置为编辑后列表
        self.usr = usr_edited

        # 测试语句
        # print(self.usr)

    def sub_language(self):
        """切换语言"""
        # 中文
        if self.usr[1] == 'cn':
            self.language = "cn"
            self.prompts = self.CN_PROMPTS
            self.command_helps = self.COMMAND_HELPS_CN
            self.all_helps = self.ALL_HELPS_CN
            print_info(self.prompts[2])

        # 英文
        elif self.usr[1] == 'en':
            self.language = "en"
            self.prompts = self.EN_PROMPTS
            self.command_helps = self.COMMAND_HELPS_EN
            self.all_helps = self.ALL_HELPS_EN
            print_info(self.prompts[2])

        # 报错
        else:
            print_warning(self.prompts[1])

    def print_help(self):
        """输出帮助"""
        # 输出全部帮助
        if len(self.usr) == 1:
            # 输出
            print_info(self.all_helps)

        # 输出单个命令帮助
        elif len(self.usr) == 2 and self.usr[1] in self.COMMANDS:
            print_info(self.command_helps[self.COMMANDS.index(self.usr[1])])

        # 输出单个程序及位置
        elif len(self.usr) == 2 and self.usr[1] in self.appls.keys():
            self._print_appl(self.usr[1])

        # 报错
        else:
            print_warning(self.prompts[1])

    def append_appl(self):
        """添加程序快捷方式"""
        # 检查格式 append [appl] at [dir]
        if not len(self.usr) == 4 or not self.usr[2] == "at":
            print_warning(self.prompts[1])

        # 处理
        else:
            # 获得新应用名与地址
            new_appl = self.usr[1]
            new_dir = self.usr[3]

            # 获得已有路径
            exist_dir = []
            for key in self.appls.keys():
                exist_dir.append((self.DISK_NAME + self.appls[key]))

            # 检查程序是否存在
            if not os.path.exists(new_dir):
                print_warning(self.prompts[5])

            # 程序必须在硬盘中
            elif new_dir.split('\\')[0] != self.DISK_NAME:
                print_warning(self.prompts[7])

            # 后缀必须为.exe
            elif new_dir.split('\\')[-1][-3:] != "exe":
                print_warning(self.prompts[9])

            # 不准重名
            elif new_appl in self.appls.keys():
                print_warning(self.prompts[4])

            elif new_appl in self.COMMANDS:
                print_warning(self.prompts[22])

            # 不准重复路径
            elif new_dir in exist_dir:
                print_warning(self.prompts[6])

            # 添加
            else:
                # 询问是否添加
                confirm = input_confirm(self.prompts[8])

                # 确认
                if confirm == "Y":
                    # 去掉盘符
                    new_dir = new_dir[2:]

                    # 写入JSON
                    self.appls[new_appl] = new_dir
                    try:
                        with open(self.DISK_NAME + "\\" + self.APPL_JSON_ROUTE, "w", encoding="utf-8") as f1:
                            json.dump(self.appls, f1)
                        self.create_save()
                    except FileNotFoundError:
                        self.check_vitals()

                    # 提示并重新读取
                    print_info("已添加程序:" + new_dir)

                # 取消
                elif confirm == "n":
                    pass

                # 报错
                else:
                    print_warning(self.prompts[1])

    def del_appl(self):
        """删除程序快捷方式"""
        # 在已有程序中
        if self.usr[1] in self.appls.keys():

            # 询问确认删除
            confirm = input_confirm(self.prompts[14])

            # 确认
            if confirm == "Y":
                # 弹出应用与路径
                del self.appls[self.usr[1]]

                # 重写JSON
                try:
                    with open(self.DISK_NAME + "\\" + self.APPL_JSON_ROUTE, "w", encoding="utf-8") as f:
                        json.dump(self.appls, f)
                    self.create_save()
                except FileNotFoundError:
                    self.check_vitals()

                # 提示成功
                print_info(self.prompts[13])

            # 取消
            elif confirm == "n":
                print_info(self.prompts[15])

        # 不在已有程序中
        else:
            print_warning(self.prompts[12])

    def list_appl(self):
        """列出所有程序"""
        if len(self.appls) != 0:
            print_info(self.prompts[16])
            self._print_appls(self._max_len())
        else:
            print_info(self.prompts[23])

    def jump_route(self):
        """打开对应文件资源管理器页面"""
        if self.usr[1] in self.appls.keys():
            route = self.appls[self.usr[1]].split("\\")
            route.pop(-1)
            route = "\\".join(route)
            command = '"' + self.DISK_NAME + route + '"'
            print(command)
            try:
                os.system("explorer " + command)
            except FileNotFoundError:
                print_warning(self.prompts[27])
        else:
            print(self.prompts[12])

    def create_save(self):
        """备份"""
        self.save = self.appls.copy()

    def check_vitals(self, first_time=False, command=False):
        error = False
        if self._missing_errors():
            error = True
            self.error_inform("01010201")
            self.handle_error("01010201")
        if first_time:
            if self._missing_appls():
                error = True
                self.error_inform("01010101(1)")
                self.handle_error("01010101(1)")
        else:
            if self._missing_appls():
                error = True
                self.error_inform("01010101(2)")
                self.handle_error("01010101(2)")
        if command and not error:
            print_info(self.prompts[26])



    def _missing_appls(self):
        """检查应用文件"""
        appls_missing = True
        if os.path.exists(self.DISK_NAME + "\\" + self.APPL_JSON_ROUTE):
            appls_missing = False
        return appls_missing

    def _missing_errors(self):
        error_missing = True
        if os.path.exists(self.DISK_NAME + "\\" + self.ERROR_TXT_ROUTE):
            error_missing = False
        return error_missing

    def error_inform(self, code, method = "inform"):
        """告知错误"""
        if method == "inform":
            print_error(self.CN_PROMPTS[self.HANDLE_LIST[self.ERROR_LIST.index(code)][0]])
            print_error(self.EN_PROMPTS[self.HANDLE_LIST[self.ERROR_LIST.index(code)][0]])
        elif method == "solved":
            print_warning(self.CN_PROMPTS[self.HANDLE_LIST[self.ERROR_LIST.index(code)][1]])
            print_warning(self.EN_PROMPTS[self.HANDLE_LIST[self.ERROR_LIST.index(code)][1]])

    def handle_error(self, code):
        """处理错误"""
        if code == self.ERROR_LIST[0]:# 应用文件丢失，无法修复
            with open(self.DISK_NAME + "\\" + self.APPL_JSON_ROUTE, "a", encoding="utf-8") as f:
                json.dump({}, f)
            self.appls = {}
        elif code == self.ERROR_LIST[1]:# 应用文件丢失，可以修复
            with open(self.DISK_NAME + "\\" + self.APPL_JSON_ROUTE, "a", encoding="utf-8") as f:
                json.dump(self.save, f)
        elif code == self.ERROR_LIST[2]:# 读取错误，无法修复
            with open(self.DISK_NAME + "\\" + self.APPL_JSON_ROUTE, "a", encoding="utf-8") as f:
                json.dump({}, f)
            self.appls = {}
        elif code == self.ERROR_LIST[3]:# 读取错误，可以修复
            with open(self.DISK_NAME + "\\" + self.APPL_JSON_ROUTE, "a", encoding="utf-8") as f:
                json.dump(self.save, f)
        elif code == self.ERROR_LIST[4]:# 错误文件丢失
            with open(self.DISK_NAME + "\\" + self.ERROR_TXT_ROUTE, "a", encoding="utf-8"):
                pass

        self.record_error(code)
        self.error_inform(code, "solved")

    def record_error(self, code):
        now = str(datetime.now().strftime('%Y/%m/%d %H:%M:%S'))
        with open(self.DISK_NAME + "\\" + self.ERROR_TXT_ROUTE, "a", encoding="utf-8") as e:
            e.write("code:" + code + " time:" + now + "\n")
        del now

if __name__ == '__main__':
    DL = DiskLink()
    DL.mainloop()

# 测试语句
# append rnd at F:\Memory\Software\Rand_Num\随机学号.exe
# append pcl at F:\Memory\Software\Minecraft\Plain Craft Launcher 2.exe
"""
        self.ERROR_LIST = (
            "01010101(1)", # 应用文件丢失，无法修复
            "01010101(2)", # 应用文件丢失，可以修复
            "01010102(1)", # 读取错误，无法修复
            "01010102(2)", # 读取错误，可以修复
            "01010201", # 错误文件丢失
        )
        self.HANDLE_LIST = (
            (17, 20),
            (17, 25),
            (18, 20),
            (18, 25),
            (19, 21),
        )"""