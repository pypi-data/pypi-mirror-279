from typing import Any, TypeVar

from cattrs import Converter
from cattrs.gen import make_dict_structure_fn, override

from botops import telegram

__all__ = ["Loader"]

T = TypeVar("T")


class Loader:
    def __init__(self) -> None:
        self._converter = Converter()
        self._converter.register_structure_hook(
            telegram.Message,
            make_dict_structure_fn(
                telegram.Message, self._converter, from_user=override(rename="from")
            ),
        )

    def __call__(self, _type: type[T], data: Any) -> T:
        return self._converter.structure(data, _type)
