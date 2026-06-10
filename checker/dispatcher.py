from checker.parser import (
    parse_node
)

from checker.validator import (
    validate
)

from checker.normalizer import (
    normalize
)


class DispatchResult:

    def __init__(
        self,
        ok,
        node=None,
        error=None
    ):

        self.ok = ok
        self.node = node
        self.error = error


def filter_proxy(node: dict) -> dict:
    """
    过滤代理节点，移除空值字段
    
    Args:
        node: 节点配置字典
        
    Returns:
        过滤后的节点配置，移除了None、空字符串、空列表
    """
    return {
        k: v
        for k, v in node.items()
        if v not in (None, "", [])
    }


def dispatch(
    line: str,
    filter_empty: bool = True
):
    """
    分派单条节点行记录
    
    Args:
        line: 节点配置行
        filter_empty: 是否过滤空值字段，默认True
        
    Returns:
        DispatchResult 对象，包含解析结果或错误信息
    """
    try:

        node = parse_node(
            line
        )

        node = normalize(
            node
        )

        if not validate(
            node
        ):

            return DispatchResult(

                ok=False,

                error="validation failed"
            )

        if filter_empty:
            node = filter_proxy(node)

        return DispatchResult(

            ok=True,

            node=node
        )

    except Exception as e:

        return DispatchResult(

            ok=False,

            error=str(e)
        )
