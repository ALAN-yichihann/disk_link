# 临时测试脚本：验证 errors.py 可修复分支（测试会修改真实数据文件，结束自动恢复）
print("========== 测试开始：01010102(2) ==========\n")

import json
import sys
from pathlib import Path

# 将项目根目录加入模块搜索路径
root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(root))

from disk_link import DiskLink
from errors import Errors

# 备份真实数据文件
appls_path = root / "appls.json"
errors_path = root / "errors.txt"
appls_backup = appls_path.read_text(encoding="utf-8")
errors_backup = errors_path.read_text(encoding="utf-8")

try:
    # 构造测试对象（不跑 __init__，避免交互）
    dl = DiskLink.__new__(DiskLink)
    dl.BASE_DIR = root
    dl.DISK_NAME = Path(__file__).resolve().parent.drive
    dl.APPL_JSON_ROUTE = appls_path
    dl.ERROR_TXT_ROUTE = errors_path
    dl.save = {"test": r"\Memory\test.exe"}
    dl.appls = dl.save.copy()
    with open(root / "lang/zh-CN.json", encoding="utf-8") as f:
        dl.prompts = json.load(f)["PROMPTS"]
    dl.errors = Errors(dl)

    # 预置损坏文件
    appls_path.write_text("invalid{", encoding="utf-8")

    print("----------以下为程序输出:\n")

    # 触发可修复分支（读取错误，可修复）
    dl.errors.handle_error(["01010102(2)"])

    print("\n----------程序输出完毕。\n")

    # 验证磁盘文件被覆写为备份内容（而非追加）
    disk_content = json.loads(appls_path.read_text(encoding="utf-8"))
    print("磁盘文件内容:", repr(disk_content))
    assert disk_content == dl.save, "FAIL: 磁盘文件未覆写为备份"
    assert dl.appls == dl.save, "FAIL: 内存未同步"
    print("可修复分支: 覆写成功, 内存同步")
finally:
    # 恢复真实数据文件
    appls_path.write_text(appls_backup, encoding="utf-8")
    errors_path.write_text(errors_backup, encoding="utf-8")
    print("已恢复 appls.json 和 errors.txt")
