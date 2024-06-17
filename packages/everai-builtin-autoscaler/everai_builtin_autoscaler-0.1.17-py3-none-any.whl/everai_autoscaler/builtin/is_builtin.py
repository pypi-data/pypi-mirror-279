import typing
from everai_autoscaler.model import BuiltinAutoScaler
from .all_builtins import all_builtins


def is_builtin(obj: typing.Any) -> bool:
    if not isinstance(obj, BuiltinAutoScaler):
        return False

    for builtin in all_builtins:
        if isinstance(obj, builtin):
            return True

    return False
