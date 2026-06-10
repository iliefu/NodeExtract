"""
checker 模块示例使用

此示例演示如何使用 checker 模块获取、解析和测试代理节点。
"""

import asyncio
from checker.subscription import fetch
from checker.dispatcher import dispatch
from checker.scheduler import Scheduler


# 1. 获取订阅
SUB_URL = "https://your-subscription-url.com/subscribe"

async def main():
    """
    主程序：获取→解析→验证→过滤→测试
    """
    print("Step 1: 获取订阅...")
    lines = fetch(SUB_URL)
    print(f"  获取 {len(lines)} 行配置")
    
    # 2. 解析和验证节点
    print("\nStep 2: 解析和验证节点...")
    nodes = []
    for line in lines:
        r = dispatch(line, filter_empty=True)
        if r.ok:
            nodes.append(r.node)
        else:
            print(f"  ✗ {r.error}")
    
    print(f"  成功解析 {len(nodes)} 个节点")
    
    # 3. 创建调度器并并发测试
    print("\nStep 3: 并发测速...")
    scheduler = Scheduler(
        workers=[
            "http://mihomo1:9090",
            "http://mihomo2:9090",
            "http://mihomo3:9090"
        ],
        concurrency=50,
        mixed_port=7890
    )
    
    results = await scheduler.dispatch(nodes)
    
    # 4. 统计结果
    print("\nStep 4: 测试结果统计")
    success_count = sum(1 for r in results if r.success)
    print(f"  成功: {success_count}/{len(results)}")
    
    # 显示前5个结果
    print("\nTop 5 结果:")
    for i, r in enumerate(sorted(results, key=lambda x: x.score, reverse=True)[:5], 1):
        print(f"  {i}. {r.node.get('name', 'unknown')} "
              f"延迟: {r.delay_ms}ms 速度: {r.speed_mbps}Mbps 分数: {r.score}")


if __name__ == "__main__":
    asyncio.run(main())
