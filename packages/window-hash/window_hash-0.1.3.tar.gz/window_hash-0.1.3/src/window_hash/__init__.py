from typing import Any, Callable, Optional

from .conditions import ConditionType

Buffer = bytes


# Cannot import private class `_Hash` from hashlib
class _Hash:
    def __init__(self, data: Buffer = ...) -> None: ...
    def hexdigest(self) -> str: ...
    def update(self, data: Buffer, /) -> None: ...


class WindowHash:
    def __init__(
        self,
        hash_func: Callable[..., _Hash],
        conditions: tuple[ConditionType],
        data_func: Optional[Callable[[Any], Buffer]] = None,
    ):
        self.__hash_func = hash_func
        self.__conditions = conditions
        self.__data_func = data_func

        self.__reset()

    def __reset(self) -> None:
        self.__hash_cache = list(
            self.__hash_func()
            for _ in self.__conditions
        )
        self.__hash_data = list(
            []
            for _ in self.__conditions
        )

    def __update_single(
        self,
        i: int,
        condition: ConditionType,
        data: Any,
    ) -> Optional[str]:
        hash: _Hash = self.__hash_cache[i]
        hash_data: list[Any] = self.__hash_data[i]

        hashable_data: Buffer = self.__data_func(data) if self.__data_func else data

        hash_data.append(data)
        if condition(hash_data):
            hash.update(hashable_data)
            return None

        old_hash_value: str = hash.hexdigest()

        self.__hash_cache[i] = self.__hash_func(hashable_data)
        self.__hash_data[i] = [data]

        return old_hash_value

    def update(self, data: Any) -> tuple[Optional[str], ...]:
        return tuple(
            self.__update_single(
                i,
                condition,
                data,
            )
            for i, condition in enumerate(
                self.__conditions,
            )
        )

    def close(self) -> tuple[str, ...]:
        result = tuple(
            hash.hexdigest()
            for hash in self.__hash_cache
        )

        self.__reset()

        return result
