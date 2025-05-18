# 日志系统使用指南

## 基本配置

```python
from logging_config import LoggingConfig

# 使用默认配置
config = LoggingConfig()
logger = config.logger
logger.info("Default configuration")
```

## 高级功能

### 1. 按级别分离日志
自动创建不同级别的日志文件(INFO/WARNING/ERROR)

### 2. 压缩日志
支持zip/gz/bz2压缩格式

```python
# 使用gzip压缩
config = LoggingConfig(compression="gz")
```

### 3. 结构化日志
```python
logger = config.logger.bind(request_id="tx123")
logger.info("Structured log", amount=100)
```

### 4. 添加上下文
```python
config.context_processors.append(lambda: {
    'trace_id': 'trace123',
    'service': 'payment'
})
```

## 日志格式
```
时间戳 | 日志级别 | request_id | trace_id | 消息
```

## 示例输出
```
2025-05-18 22:03:30.747 | INFO     | req500 | default | Final compressed log
```
