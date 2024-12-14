import subprocess
import schedule
import time
from datetime import datetime

# 定义Python解释器和main.py的完整路径
python_interpreter = '../../venv3/bin/python'
main_py_path = 'main.py'
# /Users/vktia/dev/SCAS/moneyBomb/moneyBombTest/moneyBombTest/loop.py
# /Users/vktia/dev/SCAS/moneyBomb/venv3/bin/python

# 运行main.py函数
def run_main_py():
    global run_count  # 使用全局变量来记录运行次数
    print(f"正在运行 main.py - 今日已运行 {run_count + 1} 次")
    subprocess.run([python_interpreter, main_py_path])
    run_count += 1

# 初始化运行次数
run_count = 0

# 立即运行main.py一次
run_main_py()

# 计划任务，每分钟运行一次main.py
schedule.every(1).minutes.do(run_main_py)

# 主循环
while True:
    schedule.run_pending()
    time.sleep(1)