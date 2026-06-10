import base64
import requests
import logging


def fetch(url: str):
    """
    从URL获取订阅配置，支持Base64自动解码
    
    Args:
        url: 订阅URL
        
    Returns:
        节点配置行列表
    """
    try:
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        text = response.text.strip()
    except requests.RequestException as e:
        logging.error(f"Failed to fetch subscription from {url}: {e}")
        return []
    
    # 尝试Base64解码
    try:
        # 适当补齐Base64填充符
        padding = len(text) % 4
        if padding:
            text = text + "=" * (4 - padding)
        text = base64.b64decode(text).decode()
    except (ValueError, UnicodeDecodeError):
        # 解码失败，使用原始文本
        pass
    
    return [x.strip() for x in text.splitlines() if x.strip()]
