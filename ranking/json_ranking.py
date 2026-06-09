from typing import List, Dict

class JSONRanking:
    """
    根据 JSON 存储的节点数据计算分数
    """
    @staticmethod
    def rank(results: List[Dict]) -> List[Dict]:
        def calc_score(r: Dict) -> float:
            delay_score = max(0, 100 - r.get("delay_ms", 9999)/10)
            speed_score = min(r.get("speed_mbps", 0), 100)
            loss_score = max(0, 100 - r.get("packet_loss", 100))
            jitter_score = max(0, 100 - r.get("jitter_ms", 100))
            stability_score = r.get("stability", 0)

            return round(delay_score*0.25 +
                         speed_score*0.35 +
                         loss_score*0.15 +
                         jitter_score*0.10 +
                         stability_score*0.15, 2)

        for r in results:
            r["score"] = calc_score(r)

        results.sort(key=lambda x: x["score"], reverse=True)
        return results
