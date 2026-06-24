import re

# 适配你的日志：
# INFO 2026-06-24 23:04:18 - message

log_pattern = re.compile(
    r"(\w+)\s+([\d\-: ]+)\s+-\s+(.*)"
)


def parse_line(line: str):
    """
    解析当前真实日志格式
    """

    match = log_pattern.match(line)

    if not match:
        return None

    level = match.group(1)
    timestamp = match.group(2)
    message = match.group(3)

    return {
        "timestamp": timestamp,
        "level": level,
        "service": "local-service",  # 临时补齐字段（避免 analyzer 崩）
        "method": "N/A",
        "endpoint": "N/A",
        "status": 200 if level == "INFO" else 500,
        "latency": 0,
        "request_id": "N/A",
        "message": message
    }
