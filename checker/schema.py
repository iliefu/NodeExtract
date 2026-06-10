# ⚠️ 此文件已废弃

## 迁移说明

`checker/schema.py` 中的 `proxy()` 函数已集成到 `checker/dispatcher.py`。

### 函数迁移

| 原函数 | 新函数 | 位置 | 说明 |
|--------|--------|------|------|
| `proxy()` | `filter_proxy()` | `checker.dispatcher` | 过滤空值字段 |

### 使用方式更新

**旧代码（已废弃）:**
```python
from checker.schema import proxy
node = proxy(node_config)
```

**新代码（方式1 - 推荐）:**
```python
from checker.dispatcher import dispatch
result = dispatch(line, filter_empty=True)  # 自动过滤
node = result.node
```

**新代码（方式2 - 单独使用）:**
```python
from checker.dispatcher import filter_proxy
node = filter_proxy(node_config)
```

### 改进说明

- `filter_proxy()` 与原 `proxy()` 功能完全相同
- 在 `dispatch()` 中自动应用，通过 `filter_empty` 参数控制
- 代码结构更加清晰，处理流程统一

## 删除时间表

此文件将在版本升级时删除。建议立即更新所有使用 `schema.proxy()` 的代码。
