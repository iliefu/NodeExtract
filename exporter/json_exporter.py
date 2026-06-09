import json
from pathlib import Path
from typing import List, Dict
import yaml

def export_json(nodes: List[Dict], path: str):
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    with p.open("w", encoding="utf-8") as f:
        json.dump(nodes, f, ensure_ascii=False, indent=2)

def export_yaml(nodes: List[Dict], path: str):
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    with p.open("w", encoding="utf-8") as f:
        yaml.safe_dump({"proxies": nodes}, f, allow_unicode=True)
