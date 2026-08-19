# 测试脚本：验证 Path 优化的路径校验与裁剪逻辑
from pathlib import Path

# ===== append_appl 校验逻辑 =====
# 小写盘符 + 正斜杠 + 大写后缀，均应通过规范化
p = Path(r"f:/Memory/Software/test.EXE")
assert p.drive.lower() == "f:", p.drive
assert p.suffix.lower() == ".exe", p.suffix

# 去盘符裁剪（按 drive 实际长度）
new_dir = str(p)[len(p.drive):]
assert new_dir == r"\Memory\Software\test.EXE", repr(new_dir)
print("裁剪结果:", repr(new_dir))

# 重复路径小写比较
exist = [r"d:\memory\software\test.exe".lower()]
assert str(Path(r"d:\Memory\Software\test.exe")).lower() in exist

# ===== jump_route 父目录计算 =====
route = str(Path("d:" + new_dir).parent)
assert route == r"d:\Memory\Software", repr(route)
print("父目录:", repr(route))

# ===== 拒绝场景 =====
# 相对路径无盘符
assert Path(r"Memory\a.exe").drive == ""
# 无后缀
assert Path(r"f:\Memory\a").suffix == ""
# 非exe后缀
assert Path(r"f:\Memory\a.txt").suffix.lower() != ".exe"

print("全部断言通过")
