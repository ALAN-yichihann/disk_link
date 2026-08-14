from datetime import datetime
import json
import os

from output import print_error, print_warning, print_info, input_confirm

class Errors():
    """管理错误处理的类"""
    def __init__(self, DL):
        """错误模块初始化"""

        self.DL = DL
        
        # 错误处理列表
        self.ERROR_MAP = {
            "01010101(1)": ("FILE_NOT_FOUND_PROMPT", "FIX_NEEDED_PROMPT", self.deal_file_not_found(False)), # 应用文件丢失，无法修复
            "01010101(2)": ("FILE_NOT_FOUND_PROMPT", "FIX_RESTORED_PROMPT", self.deal_file_not_found()), # 应用文件丢失，可以修复
            "01010102(1)": ("DATA_READ_ERROR_PROMPT", "FIX_NEEDED_PROMPT", self.deal_data_read_error(False)), # 读取错误，无法修复
            "01010102(2)": ("DATA_READ_ERROR_PROMPT", "FIX_RESTORED_PROMPT", self.deal_data_read_error()), # 读取错误，可以修复
            "01010201": ("ERROR_LOG_NOT_FOUND_PROMPT", "FIX_WITH_RECORD_LOSS_PROMPT", self.deal_error_not_found()), # 错误文件丢失
        }

    def check_vitals(self, first_time=False, command=False):
        """检查必要文件是否存在，若不存在则提示并尝试修复"""
        errors = []
        if self._missing_errors():
            errors.append("01010201")
            self.error_inform("01010201")
        if self._missing_appls():
            errors.append("01010101(1)" if first_time else "01010101(2)")
            self.error_inform("01010101(1)" if first_time else "01010101(2)")

        if command and not errors:
            print_info(self.DL.prompts["NECESSARY_FILES_OK_PROMPT"])
            return 0
        
        self.handle_error(errors)

    def error_inform(self, code, method = "inform"):
        """告知错误"""
        key = self.ERROR_MAP[code][0 if method == "inform" else 1]
        if method == "inform":
            print_error(self.DL.prompts[key])
        elif method == "solved":
            print_warning(self.DL.prompts[key])

    def handle_error(self, errors):
        """处理错误"""
        for code in errors:
            self.ERROR_MAP[code][2] # 调用对应处理函数
            print_info(self.DL.prompts[self.ERROR_MAP[code][1]])

    def deal_file_not_found(self, fixable=True):
        """处理appls.json丢失的情况"""
        route = self.DL.DISK_NAME + "\\" + self.DL.APPL_JSON_ROUTE
        if fixable:
            with open(route, "w", encoding="utf-8") as f:
                json.dump(self.DL.save, f)
        else:
            with open(route, "w", encoding="utf-8") as f:
                json.dump({}, f)

    def deal_error_not_found(self):
        """处理error.txt丢失的情况"""
        route = self.DL.DISK_NAME + "\\" + self.DL.ERROR_TXT_ROUTE
        self.record_error("01010201")

    def deal_data_read_error(self, fixable=True):
        """处理读取错误的情况"""
        route = self.DL.DISK_NAME + "\\" + self.DL.APPL_JSON_ROUTE
        if fixable:
            with open(route, "w", encoding="utf-8") as f:
                json.dump(self.DL.save, f)
        else:
            with open(route, "w", encoding="utf-8") as f:
                json.dump({}, f)

    def record_error(self, code):
        """记录错误"""
        now = str(datetime.now().strftime('%Y/%m/%d %H:%M:%S'))
        with open(self.DL.DISK_NAME + "\\" + self.DL.ERROR_TXT_ROUTE, "a", encoding="utf-8") as e:
            e.write("code:" + code + " time:" + now + "\n")
        del now

    def _missing_appls(self):
        """检查应用文件"""
        return True if not os.path.exists(self.DL.DISK_NAME + "\\" + self.DL.APPL_JSON_ROUTE) else False

    def _missing_errors(self):
        """检查错误文件"""
        return True if not os.path.exists(self.DL.DISK_NAME + "\\" + self.DL.ERROR_TXT_ROUTE) else False
        