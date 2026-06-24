class LogAnalyzer:
    def __init__(self):

        # =========================
        # 1. level统计
        # =========================
        self.level_stats = {
            "INFO": 0,
            "WARN": 0,
            "ERROR": 0
        }

        # =========================
        # 2. endpoint统计
        # =========================
        self.endpoint_stats = {}

        # =========================
        # 3. module统计
        # =========================
        self.module_stats = {}

        # =========================
        # 4. keyword统计
        # =========================
        self.keyword_stats = {
            "timeout": 0,
            "failed": 0,
            "connection": 0,
            "refused": 0
        }

    # =========================
    # 处理单条日志
    # =========================
    def process(self, log):

        # ---- level统计 ----
        level = log["level"]
        if level in self.level_stats:
            self.level_stats[level] += 1

        # ---- endpoint统计 ----
        endpoint = log["endpoint"]
        status = log["status"]

        if endpoint not in self.endpoint_stats:
            self.endpoint_stats[endpoint] = {"count": 0, "error": 0}

        self.endpoint_stats[endpoint]["count"] += 1

        if status >= 400:
            self.endpoint_stats[endpoint]["error"] += 1

        # ---- module统计（简单规则）----
        module = self._detect_module(log)

        if module not in self.module_stats:
            self.module_stats[module] = 0

        self.module_stats[module] += 1

        # ---- keyword统计 ----
        message = log["message"].lower()

        for k in self.keyword_stats:
            if k in message:
                self.keyword_stats[k] += 1

    # =========================
    # 简单模块识别规则
    # =========================
    def _detect_module(self, log):
        endpoint = log["endpoint"]
        message = log["message"].lower()

        if "auth" in endpoint:
            return "auth"
        if "pay" in endpoint:
            return "payment"
        if "db" in message:
            return "db"

        return "other"

    # =========================
    # 生成最终报告
    # =========================
    def get_report(self):

        # root cause（错误最多的模块）
        root_cause = max(self.module_stats, key=self.module_stats.get)

        return {
            "level_stats": self.level_stats,
            "endpoint_stats": self.endpoint_stats,
            "module_stats": self.module_stats,
            "keyword_stats": self.keyword_stats,
            "root_cause": root_cause
        }
