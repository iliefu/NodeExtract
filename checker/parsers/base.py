import base64
from urllib.parse import (
    urlparse,
    parse_qs,
    unquote
)

from checker.exceptions import (
    MissingFieldError
)


def b64decode_auto(data: str) -> bytes:
    """
    自动补齐Base64填充符并解码
    
    Args:
        data: Base64编码的字符串
        
    Returns:
        解码后的字节数据
    """
    padding = "=" * (-len(data) % 4)
    return base64.b64decode(data + padding)


def b64decode_safe(data: str) -> str:
    """
    安全的Base64解码，失败时返回原始字符串
    
    Args:
        data: 可能是Base64编码的字符串
        
    Returns:
        解码后的字符串，或原始字符串（如果解码失败）
    """
    try:
        padding = len(data) % 4
        if padding:
            data = data + "=" * (4 - padding)
        return base64.b64decode(data).decode()
    except (ValueError, UnicodeDecodeError):
        return data


def parse_query(url: str) -> dict:
    """
    解析URL查询参数
    
    Args:
        url: URL字符串
        
    Returns:
        查询参数字典
    """
    parsed = urlparse(url)
    q = parse_qs(parsed.query)
    return {k: v[0] for k, v in q.items()}


def parse_name(url: str) -> str:
    """
    从URL片段中提取名称
    
    Args:
        url: URL字符串
        
    Returns:
        URL片段中的名称，未编码
    """
    parsed = urlparse(url)
    if parsed.fragment:
        return unquote(parsed.fragment)
    return ""


def require(data: dict, field: str):
    """
    检查字典中是否存在必需字段
    
    Args:
        data: 字典
        field: 字段名
        
    Returns:
        字段值
        
    Raises:
        MissingFieldError: 字段不存在
    """
    if field not in data:
        raise MissingFieldError(f"{field} required")
    return data[field]


def boolify(v):
    """
    将任意值转换为布尔值
    
    Args:
        v: 任意值
        
    Returns:
        布尔值
    """
    if isinstance(v, bool):
        return v
    return str(v).lower() in ("1", "true", "yes")
