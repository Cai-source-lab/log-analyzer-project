import time
import os

# =========================
# 日志文件路径
# =========================
LOG_FILE = "logs/app.log"

# =========================
# 阈值配置（可调）
# =========================
ERROR_THRESHOLD = 5


# =========================
# tail -f 实现
# =========================
def follow(file):
    """
    模拟 Linux tail -f
    持续读取新增日志
    """

    file.seek(0, os.SEEK_END)

    while True:
        line = file.readline()

        if not line:
            time.sleep(0.5)
            continue

        yield line.strip()


# =========================
# 日志解析（轻量版）
# =========================
def parse_stream_line(line: str):
    """
    从实时日志中提取关键字段
    这里不做完整 parser（避免重复 analyzer）
    """

    lower_line = line.lower()

    level = "INFO"
    if "error" in lower_line:
        level = "ERROR"
    elif "warning" in lower_line:
        level = "WARN"

    return {
        "raw": line,
        "level": level,
        "is_error": level == "ERROR"
    }


# =========================
# 实时监控主逻辑
# =========================
def stream_monitor():
    """
    实时日志监控 + 简单告警
    """

    print("=== START STREAM MONITOR ===")

    result = {
        "ERROR": 0,
        "WARN": 0,
        "INFO": 0
    }

    try:
        with open(LOG_FILE, "r", encoding="utf-8") as f:

            for line in follow(f):

                log = parse_stream_line(line)

                level = log["level"]

                # =========================
                # 统计
                # =========================
                result[level] += 1

                # =========================
                # 输出关键事件
                # =========================
                if level == "ERROR":
                    print("🚨 ERROR:", log["raw"])

                elif level == "WARN":
                    print("⚠️ WARN:", log["raw"])

                # INFO 默认不刷屏（避免污染控制台）

                # =========================
                # 实时状态输出
                # =========================
                print("CURRENT STATS:", result)

                # =========================
                # 告警逻辑（核心运维点）
                # =========================
                if result["ERROR"] > ERROR_THRESHOLD:
                    print("🚨 ALERT: HIGH ERROR RATE!")

    except FileNotFoundError:
        print(f"❌ LOG FILE NOT FOUND: {LOG_FILE}")
        print("请先启动 app.py 生成日志")


# =========================
# 入口
# =========================
if __name__ == "__main__":
    stream_monitor()
