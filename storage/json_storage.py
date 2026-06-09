import json
from pathlib import Path
from typing import List, Dict
import time
import hashlib

class JSONStorage:
    def __init__(self, path: str = "runtime/cache.json"):
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        if not self.path.exists():
            self._dump({"history": [], "top_nodes": [], "nodes": {}})

        self.data = self._load()

    def _load(self) -> Dict:
        try:
            with self.path.open("r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return {"history": [], "top_nodes": [], "nodes": {}}

    def _dump(self, data: Dict):
        with self.path.open("w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    def save_node_result(self, node: dict, result: dict):
        """保存单个节点的最新测试结果"""
        node_hash = self._hash_node(node)
        timestamp = int(time.time())
        entry = {"timestamp": timestamp, "result": result, "node": node}

        # 更新节点历史
        self.data["history"].append(entry)
        # 保留最近 50 条历史记录
        self.data["history"] = self.data["history"][-5000:]

        # 更新节点缓存
        self.data["nodes"][node_hash] = {"score": result.get("score", 0),
                                        "updated": timestamp,
                                        "node": node}

        self._dump(self.data)

    def get_top_nodes(self, top_n: int = 100) -> List[dict]:
        """获取 top_n 节点"""
        nodes_list = list(self.data["nodes"].values())
        nodes_list.sort(key=lambda x: x.get("score", 0), reverse=True)
        return [n["node"] for n in nodes_list[:top_n]]

    def _hash_node(self, node: dict) -> str:
        """生成节点唯一 hash"""
        s = f"{node.get('server','')}_{node.get('port','')}_{node.get('uuid','')}"
        return hashlib.sha256(s.encode()).hexdigest()
