# 测试脚本：验证 bug3（写入OSError兜底）+ bug4（FileNotFoundError兜底）
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

# 不可写路径（父目录不存在，open("w") 会抛 FileNotFoundError，是 OSError 子类）
BAD_ROUTE = Path("d:/nonexistent_dir_xyz/appls.json")
BAD_ERROR_ROUTE = Path("d:/nonexistent_dir_xyz/errors.txt")

try:
    # 构造测试对象（不跑 __init__，避免交互）
    dl = DiskLink.__new__(DiskLink)
    dl.DISK_NAME = "d:"
    dl.APPL_JSON_ROUTE = appls_path
    dl.ERROR_TXT_ROUTE = errors_path
    dl.save = {"test": r"\Memory\test.exe"}
    dl.appls = dl.save.copy()
    with open(root / "lang/zh-CN.json", encoding="utf-8") as f:
        dl.prompts = json.load(f)["PROMPTS"]
    dl.errors = Errors(dl)

    # ===== 测试1: 正常修复路径回归 =====
    appls_path.write_text("invalid{", encoding="utf-8")
    dl.errors.handle_error(["01010102(2)"])
    disk_content = json.loads(appls_path.read_text(encoding="utf-8"))
    assert disk_content == dl.save, "FAIL: 正常修复未覆写"
    assert dl.appls == dl.save, "FAIL: 内存未同步"
    print("测试1 正常修复: 通过")

    # ===== 测试2: 写入失败不崩溃、不同步内存、不谎报已修复 =====
    dl.appls = {"keep": r"\Memory\keep.exe"}  # 标记当前内存状态
    dl.APPL_JSON_ROUTE = BAD_ROUTE
    dl.errors.handle_error(["01010101(1)"])  # 应打印错误提示，不抛异常
    assert dl.appls == {"keep": r"\Memory\keep.exe"}, "FAIL: 写入失败时内存被错误同步"
    print("测试2 写入失败兜底: 通过（应看到红色错误提示，无黄色已修复提示）")

    # ===== 测试3: record_error 写入失败静默 =====
    dl.ERROR_TXT_ROUTE = BAD_ERROR_ROUTE
    dl.errors.record_error("01010102(1)")  # 不应抛异常
    print("测试3 错误日志写入失败静默: 通过")

    # ===== 测试4: bug4 闭环——修复失败后 read_texts 不崩溃 =====
    dl.ERROR_TXT_ROUTE = errors_path  # 恢复，保证 check_vitals 不误报
    dl.errors.handle_error(["01010101(1)"])  # 修复失败（BAD_ROUTE 不可写）
    dl.read_texts(True)  # check_vitals 修复失败 → open 抛 FileNotFoundError → 兜底
    assert dl.appls == {}, "FAIL: FileNotFoundError 兜底未生效"
    print("测试4 FileNotFoundError 兜底: 通过")
finally:
    # 恢复真实数据文件
    dl_route = getattr(dl, "APPL_JSON_ROUTE", None) if "dl" in dir() else None
    appls_path.write_text(appls_backup, encoding="utf-8")
    errors_path.write_text(errors_backup, encoding="utf-8")
    print("已恢复 appls.json 和 errors.txt")
