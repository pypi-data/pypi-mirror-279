import typing
from everai_autoscaler.model import BuiltinAutoScaler

def is_builtin(obj: typing.Any) -> bool:
    if not isinstance(obj, BuiltinAutoScaler):
        return False


    return True


__all__ = [
    'is_builtin',
    Simp
]
