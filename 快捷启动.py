import os
import sys

disk_name = os.path.abspath(__file__).split('\\')[0]

if getattr(sys, 'frozen', False):
    application_path = os.path.dirname(sys.executable)
else:
    application_path = os.path.dirname(__file__)
disk_name = application_path.split('\\')[0]

os.system(disk_name + r"\Memory\Software\Disklink\dist\disk_link.exe")

sys.exit(0)