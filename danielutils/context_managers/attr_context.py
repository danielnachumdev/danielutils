class AttrContext:
    def __init__(self, obj: object, attr: str, new_value: object, *, nonexistent_is_error: bool = True) -> None:
        self.obj = obj
        self.attr = attr
        self.new_value = new_value
        self.old_value = None
        self._has_attr: bool = hasattr(self.obj, self.attr)
        if nonexistent_is_error and not self._has_attr:
            raise RuntimeError(f"Nonexistent attribute '{self.attr}' in '{self.obj}'")

    def __enter__(self) -> 'AttrContext':
        self.old_value = getattr(self.obj, self.attr, None)
        setattr(self.obj, self.attr, self.new_value)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self._has_attr:
            setattr(self.obj, self.attr, self.old_value)
        else:
            delattr(self.obj, self.attr)


__all__ = [
    'AttrContext'
]
