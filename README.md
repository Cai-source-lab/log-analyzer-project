📊 LogInsight · 日志批处理与异常检测工具链

🚀 项目简介
这是一个模拟真实运维场景的日志分析系统，用于实现：

日志实时监听（类似 tail -f）
批量日志分析
日志级别统计（INFO / WARNING / ERROR）
简单根因分析
Docker 一键部署

整体结构模拟了生产环境中常见的 日志采集 → 解析 → 分析 → 输出报告 流程。



🧱 系统架构

日志生成模块（Log Generator / app.py）

日志数据源（app.log）

批处理分析模块（Batch Analyzer / analyzer.py）
实时监控模块（Stream Monitor / stream_monitor.py）

分析结果输出（report.json）

可视化 / 告警展示层

⚙️ 技术栈
Python 3
Linux（Ubuntu）
Docker / Docker Compose
正则表达式日志解析
dict 数据统计分析
文件流监听（tail -f 模拟）


📁 项目结构
src 目录包含主程序入口 main.py、日志解析模块 parser.py、批处理分析模块 analyzer.py

realtime 目录包含实时监控模块 stream_monitor.py

logs 目录包含日志生成服务 app.py，以及日志文件 logs/app.log

output 目录用于存放分析结果 report.json

根目录包含 Dockerfile 和 docker-compose.yml，用于容器化部署与环境编排


🔍 功能说明
1. 日志解析（parser.py）

负责把一行日志解析成结构化数据：

包含字段：

时间戳
日志级别
服务名称
请求路径
状态码
延迟
消息内容
2. 批量分析（analyzer.py）

功能：

统计 INFO / WARNING / ERROR 数量
统计模块访问情况
识别高频异常
生成 report.json
3. 实时监控（stream_monitor.py）

功能：

实时读取日志新增内容
模拟 Linux tail -f
实时分类日志
简单告警机制（错误次数阈值）
4. Docker 支持

实现一键运行环境：

docker-compose up --build

保证在不同机器上运行一致环境。


🐳 Docker 运行方式
1. 启动项目
docker-compose up --build
2. 进入容器
docker exec -it log-analyzer-system bash
3. 运行程序
python3 src/main.py
📊 输出结果示例
{
  "error_count": 12,
  "warning_count": 5,
  "info_count": 120,
  "top_modules": ["auth", "payment"],
  "root_cause": "payment service latency spike"
}


🧠 项目亮点
✔ 1. 类生产环境日志链路设计

模拟：日志生成 → 解析 → 分析 → 输出

✔ 2. 双模式设计
批处理（batch）
实时流处理（stream）
✔ 3. Linux 思维
tail -f 模拟
文件流监听
✔ 4. Docker 环境隔离
一键运行
跨机器一致性
✔ 5. 数据结构设计
dict 统计日志指标
简单根因分析逻辑
📌 可优化方向（加分项）
接入 Elasticsearch
加 Prometheus 监控指标
Web 可视化面板（Flask/FastAPI）
异常检测算法升级


👨‍💻 项目总结
这是一个用于练习 Linux 运维 + Python + Docker 的日志分析系统，模拟真实生产环境中的日志处理流程。
