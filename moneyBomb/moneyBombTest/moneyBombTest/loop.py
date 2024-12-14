import subprocess
import schedule
import time
from datetime import datetime

# 定义Python解释器和脚本路径
python_interpreter = '../../venv/bin/python'
main_py_path = 'main.py'
update_klines_path = 'updateStockKLines.py'

# 运行main.py函数
def run_main_py():
    global main_run_count
    print(f"正在运行 main.py - 今日已运行 {main_run_count + 1} 次")
    subprocess.run([python_interpreter, main_py_path])
    main_run_count += 1

# 运行updateStockKLines.py函数
def run_update_klines():
    global klines_run_count
    print(f"正在运行 updateStockKLines.py - 今日已运行 {klines_run_count + 1} 次")
    subprocess.run([python_interpreter, update_klines_path])
    klines_run_count += 1

# 初始化运行次数
main_run_count = 0
klines_run_count = 0

# 立即运行main.py一次
run_main_py()

# 立即运行updateStockKLines.py一次
run_update_klines()

# 计划任务
schedule.every(1).minutes.do(run_main_py)  # 每分钟运行一次main.py
schedule.every(1).hours.do(run_update_klines)  # 每小时运行一次updateStockKLines.py

# 主循环
while True:
    schedule.run_pending()
    time.sleep(1)