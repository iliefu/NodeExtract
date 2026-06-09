import asyncio
from checker.subscription import fetch_all
from checker.dispatcher import dispatch
from checker.scheduler import Scheduler
from storage.json_storage import JSONStorage
from ranking.json_ranking import JSONRanking
from exporter.json_exporter import export_json, export_yaml

async def main():
    storage = JSONStorage("runtime/cache.json")
    
    # 1. 获取节点订阅
    lines = fetch_all()
    
    # 2. 解析节点
    nodes = [dispatch(line) for line in lines if dispatch(line).ok]
    
    # 3. 并发测速
    scheduler = Scheduler(workers=[], concurrency=50, mixed_port=7891)  # 替换 workers
    results = await scheduler.dispatch(nodes)
    
    # 4. 排名
    ranked = JSONRanking.rank(results)
    
    # 5. 保存历史
    for r in ranked:
        storage.save_node_result(r["node"], r)
    
    # 6. 导出 top100
    top_nodes = storage.get_top_nodes(100)
    export_json(top_nodes, "output/top100.json")
    export_yaml(top_nodes, "output/top100.yaml")

if __name__ == "__main__":
    asyncio.run(main())
