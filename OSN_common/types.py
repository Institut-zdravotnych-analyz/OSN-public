"""Custom types"""

from collections.abc import MutableSequence
from typing import Any

import frozendict as fd
import frozenlist as fl
from pandas._libs.missing import NAType

NA = NAType


class FrozenList(fl.FrozenList):
    """Wrapper that makes the inited list immutable"""

    def __init__(self, data: list[Any]) -> None:
        """Init the parrent class and call .freeze()"""
        super().__init__(data)
        self.freeze()

    def tolist(self) -> list:
        """Convert the frozen list back to mutable list"""
        return list(self)


class FrozenDict(fd.frozendict):
    """Wrapper that makes the inited dict immutable. All nested structures will become immutable too."""

    def __new__(cls, data: dict[Any:Any]) -> None:
        """Init the parent class and call deepfreeze()"""
        return super().__new__(cls, cls.deepfreeze(data))

    @staticmethod
    def deepfreeze(data: dict[Any, Any]) -> fd.frozendict:
        """Freezes data"""
        return fd.deepfreeze(data, custom_converters={MutableSequence: FrozenList})

    def todict(self) -> dict:
        """Convert the frozen dict back to mutable dict. Warning: Nested structeres will stay immutable."""
        return dict(self)
