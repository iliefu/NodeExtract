"""
README: checker 模块架构

此模块负责代理节点的获取、解析、验证、过滤和性能测试。
"""

## 📦 模块结构

### 核心流程
```
subscription.fetch()
    ↓ (获取订阅)
dispatcher.dispatch()
    ├─ parser.parse_node() (解析)
    ├─ normalizer.normalize() (规范化)
    ├─ validator.validate() (验证)
    └─ dispatcher.filter_proxy() (过滤) [可选]
    ↓
scheduler.Scheduler.dispatch()
    ├─ worker_pool.WorkerPool (轮询分配Worker)
    └─ benchmark.BenchmarkRunner (性能测试)
        ├─ speedtest.SpeedTester (速度测试)
        └─ worker.Worker (Mihomo控制)
            └─ mihomo_client.MihomoClient (HTTP接口)
```

## 📄 文件说明

### 基础工具
- **base.py** ⚠️ 已废弃 → 迁移到 `parsers/base.py`
- **parsers/base.py** - 统一工具库（Base64、URL解析等）
- **exceptions.py** - 自定义异常

### 解析层
- **parser.py** - 协议路由分发
- **registry.py** - 协议处理器注册表
- **parsers/** - 各协议解析器（vmess、vless、trojan等）

### 处理层
- **normalizer.py** - 字段规范化
- **validator.py** - 字段验证
- **dispatcher.py** - 流程编排（**已集成filter_proxy**）
- **schema.py** ⚠️ 已废弃 → 功能迁移到 `dispatcher.py`

### 订阅层
- **subscription.py** - 订阅获取与Base64解码

### 测试层
- **worker.py** - 单工作者（管理单个Mihomo实例）
- **worker_pool.py** - 工作者池（轮询分配）
- **scheduler.py** - 并发调度器
- **benchmark.py** - 性能基准测试
- **speedtest.py** - 速度测试实现
- **mihomo_client.py** - Mihomo HTTP客户端

### 其他
- **example.py** - 使用示例

## 🔄 使用流程

### 完整示例
```python
import asyncio
from checker.subscription import fetch
from checker.dispatcher import dispatch
from checker.scheduler import Scheduler

async def main():
    # 1. 获取订阅
    lines = fetch("https://subscription-url")
    
    # 2. 解析并验证
    nodes = [
        dispatch(line, filter_empty=True).node
        for line in lines
        if dispatch(line).ok
    ]
    
    # 3. 并发测试
    scheduler = Scheduler(
        workers=["http://mihomo1:9090", "http://mihomo2:9090"],
        concurrency=50
    )
    results = await scheduler.dispatch(nodes)
    
    # 4. 处理结果
    for r in results:
        if r.success:
            print(f"{r.node['name']}: {r.score}分")

asyncio.run(main())
```

## 🎯 关键改进

### 最近的重构
1. ✅ 统一Base64处理 → `parsers/base.py`
2. ✅ 集成过滤功能 → `dispatcher.py`
3. ✅ 修复worker_pool → 支持URL列表自动转换
4. ✅ 增强类型注解 → 改善IDE支持
5. ✅ 完善文档注释 → 提高可维护性

### 已删除的冗余代码
- `queue_manager.py` - 功能重复于 `asyncio.Queue`
- `scorer.py` - 被 `benchmark.py` 的 `calc_score()` 替代
- `models.py` - 定义未使用

## ⚠️ 废弃通知

| 文件 | 替代方案 | 迁移方式 |
|------|---------|---------|
| base.py | parsers/base.py | 更新导入语句 |
| schema.py | dispatcher.py | 使用 `filter_proxy()` 或 `dispatch(..., filter_empty=True)` |

更多详见各文件的废弃说明。

## 🚀 快速开始

1. 查看 `example.py` 获得完整示例
2. 根据需要调整 `Scheduler` 的 `workers` 和 `concurrency` 参数
3. 修改订阅URL和输出方式
4. 运行示例代码

```bash
python -m checker.example
```
