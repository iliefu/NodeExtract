# ⚠️ 此文件已废弃

## 迁移说明

`checker/base.py` 中的所有函数已迁移到 `checker/parsers/base.py`。

### 函数迁移清单

| 函数名 | 新位置 | 说明 |
|--------|--------|------|
| `b64decode_auto()` | `checker.parsers.base` | Base64自动填充解码 |
| `b64decode_safe()` | `checker.parsers.base` | Base64安全解码（失败返回原文） |
| `parse_query()` | `checker.parsers.base` | URL查询参数解析 |
| `parse_name()` | `checker.parsers.base` | URL片段提取 |
| `require()` | `checker.parsers.base` | 字段必需性检查 |
| `boolify()` | `checker.parsers.base` | 值转布尔 |

### 导入更新

**旧代码（已废弃）:**
```python
from checker.base import b64decode_auto
```

**新代码（使用此方式）:**
```python
from checker.parsers.base import b64decode_auto
```

### 其他改动

- Base64解码逻辑已统一到 `checker/parsers/base.py`
- `checker/subscription.py` 内联使用相同的Base64处理算法
- `checker/dispatcher.py` 已集成代理过滤功能（原 `checker/schema.py`）

## 删除时间表

此文件将在版本升级时删除。建议立即更新所有导入语句。
