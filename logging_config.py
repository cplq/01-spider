from loguru import logger
from pathlib import Path
import os

class LoggingConfig:
    def __init__(self, log_name="runtime", compression="zip"):
        self.log_dir = "logs"
        self.log_name = log_name
        self.max_size = "10 MB"  # 每个日志文件最大10MB
        self.rotation = "1 day"  # 每天轮转一次
        self.retention = "30 days"  # 保留30天日志
        self.compression = compression  # 压缩格式：zip/gz/bz2
        self._setup_logger()

    def _setup_logger(self):
        # 创建日志目录
        Path(self.log_dir).mkdir(exist_ok=True)
        
        # 配置日志并保存logger引用
        self.logger = logger
        # 移除默认logger处理器避免重复输出
        logger.remove()
        
        # 按级别分离日志文件
        levels = ["INFO", "WARNING", "ERROR"]
        for level in levels:
            logger.add(
                os.path.join(self.log_dir, f"{self.log_name}_{level.lower()}_{{time}}.log"),
                rotation=self.rotation,
                retention=self.retention,
                compression=self.compression,
                enqueue=True,
                backtrace=True,
                diagnose=True,
                level=level,
                format="{time:YYYY-MM-DD HH:mm:ss.SSS} | {level: <8} | {extra[request_id]} | {extra[trace_id]} | {message}",
                filter=lambda record, lvl=level: record["level"].name == lvl  # 精确级别过滤
            )
        
        # 添加上下文处理器
        self.context_processors = []
        
        def get_processors():
            return self.context_processors
            
        def process_record(record):
            for processor in get_processors():
                record["extra"].update(processor())
            return record
            
        # 初始化logger并应用所有绑定
        self.logger = logger.patch(process_record).bind(trace_id="default")

# 初始化日志配置(保持默认配置向后兼容)
logging_config = LoggingConfig()
