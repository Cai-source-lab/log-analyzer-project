import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


import subprocess
import time


from parser import parse_line
from analyzer import LogAnalyzer
from realtime.stream_monitor import stream_monitor


# =========================
# Step 1: 运行 app.py（可选）
# =========================
def start_app():
    """
    启动日志生产服务（模拟真实系统）
    """
    print("🚀 Starting app.py ...")

    # 如果你有 app.py，就启动它
    # 没有也可以注释掉
    return subprocess.Popen(
        ["python", "app.py"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )


# =========================
# Step 2: 批处理分析
# =========================
def run_batch_analyzer():
    """
    读取 ../logs/logs/app.log → analyzer → report.json
    """

    print("📊 Running batch analyzer...")

    log_file = "logs/app.log"
    output_file = "../output/report.json"
    
    os.makedirs("../output", exist_ok=True)

    analyzer = LogAnalyzer()

    if not os.path.exists(log_file):
        print("❌ log file not found")
        return

    with open(log_file, "r", encoding="utf-8") as f:
        for line in f:

            parsed = parse_line(line.strip())

            if not parsed:
                continue

            analyzer.process(parsed)

    result = analyzer.get_report()

    with open(output_file, "w", encoding="utf-8") as f:
        import json
        json.dump(result, f, indent=4, ensure_ascii=False)

    print("✅ batch analysis done:", output_file)


# =========================
# Step 3: 实时监控
# =========================
def start_realtime_monitor():
    """
    启动实时日志监控（tail -f）
    """
    print("📡 Starting realtime monitor...")

    stream_monitor()


# =========================
# 主流程控制
# =========================
def main():

    print("===================================")
    print(" LOG ANALYSIS SYSTEM STARTING ")
    print("===================================")

    # =========================
    # 可选：启动日志生成
    # =========================
    # app_process = start_app()

    time.sleep(1)

    # =========================
    # 1. 启动实时监控（后台运行）
    # =========================
    # 如果你想先跑实时监控，可以打开
    # start_realtime_monitor()

    # =========================
    # 2. 跑离线分析（主功能）
    # =========================
    run_batch_analyzer()

    print("===================================")
    print(" SYSTEM FINISHED ")
    print("===================================")


if __name__ == "__main__":
    main()
