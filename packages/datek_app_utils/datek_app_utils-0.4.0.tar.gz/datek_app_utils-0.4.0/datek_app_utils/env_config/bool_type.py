_TRUE_VALUES = ["1", "true", "yes", "y"]
_FALSE_VALUES = ["0", "false", "no", "n"]


class _Bool:
    def __init__(self, value: str):
        self._value = value

    def __bool__(self):
        lower_ = self._value.lower()
        if lower_ in _TRUE_VALUES:
            return True

        if lower_ in _FALSE_VALUES:
            return False

        raise ValueError
