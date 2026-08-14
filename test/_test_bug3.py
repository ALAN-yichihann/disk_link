# 临时测试脚本：验证 bug3 修复
import json
from disk_link import DiskLink
from errors import Errors

print('=== 测试开始:01010102 ===')

# 构造测试对象（不跑 __init__，避免交互）
dl = DiskLink.__new__(DiskLink)
dl.DISK_NAME = 'd:'
dl.APPL_JSON_ROUTE = r'programs\disk_link\appls.json'
dl.ERROR_TXT_ROUTE = r'programs\disk_link\errors.txt'
dl.errors = Errors(dl)
dl.save = {'test': r'\Memory\test.exe'}
dl.appls = {'test': r'\Memory\test.exe'}
with open('lang/zh-CN.json', encoding='utf-8') as f:
    dl.prompts = json.load(f)['PROMPTS']

# 预置损坏文件
with open('appls.json', 'w', encoding='utf-8') as f:
    f.write('invalid{')

# 触发可修复分支（读取错误，可修复）
dl.errors.handle_error('01010102(2)')

# 验证磁盘文件被覆写为备份内容（而非追加）
with open('appls.json', encoding='utf-8') as f:
    disk_content = f.read()
print('磁盘文件内容:', repr(disk_content))
assert disk_content == json.dumps(dl.save), 'FAIL: 磁盘文件未覆写为备份'
assert dl.appls == dl.save, 'FAIL: 备份未同步'
print('可修复分支: 覆写成功, 内存同步')
