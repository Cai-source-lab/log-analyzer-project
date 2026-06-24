import time
import os
import random
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer

# =========================
# 日志路径初始化
# =========================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
LOG_DIR = os.path.join(BASE_DIR, "logs")
os.makedirs(LOG_DIR, exist_ok=True)

LOG_FILE = os.path.join(LOG_DIR, "app.log")

# =========================
# 服务状态
# =========================
SERVICE_STATUS = {
    "status": "RUNNING"
}

# =========================
# 写日志
# =========================
def write_log(level, message):
    log = f"{level} {time.strftime('%Y-%m-%d %H:%M:%S')} - {message}\n"

    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(log)

    print(log.strip())

# =========================
# 业务模拟
# =========================
def business_logic():
    while True:
        time.sleep(2)

        event = random.randint(1, 10)

        if event <= 6:
            write_log("INFO", "request processed successfully")

        elif event <= 8:
            write_log("WARNING", "slow response detected")

        else:
            write_log("ERROR", "database connection failed")

# =========================
# 故障注入
# =========================
def fault_injector():
    while True:
        time.sleep(8)

        fault = random.randint(1, 10)

        if fault <= 2:
            SERVICE_STATUS["status"] = "DEGRADED"
            write_log("ERROR", "SERVICE DEGRADED")

        elif fault == 3:
            SERVICE_STATUS["status"] = "DOWN"
            write_log("ERROR", "SERVICE CRASHED")

        else:
            SERVICE_STATUS["status"] = "RUNNING"
            write_log("INFO", "SERVICE HEALTHY")

# =========================
# HTTP服务
# =========================
class SimpleHandler(BaseHTTPRequestHandler):

    def do_GET(self):

        if self.path == "/health":
            write_log("INFO", "health check requested")
            self.send_response(200)
            self.end_headers()
            self.wfile.write(str(SERVICE_STATUS).encode())
            return

        if self.path == "/":
            write_log("INFO", "GET / request received")
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b"Service is running")
            return

        if self.path == "/error":
            write_log("ERROR", "manual error triggered")
            self.send_response(500)
            self.end_headers()
            self.wfile.write(b"Internal Server Error")
            return

        write_log("WARNING", f"unknown endpoint: {self.path}")
        self.send_response(404)
        self.end_headers()
        self.wfile.write(b"Not Found")

# =========================
# 启动服务
# =========================
def start_server():
    server = HTTPServer(("0.0.0.0", 8080), SimpleHandler)
    write_log("INFO", "HTTP server started on port 8080")
    server.serve_forever()

# =========================
# 主入口
# =========================
if __name__ == "__main__":
    write_log("INFO", "SERVICE BOOT STARTED")

    threading.Thread(target=business_logic, daemon=True).start()
    threading.Thread(target=fault_injector, daemon=True).start()

    start_server()
