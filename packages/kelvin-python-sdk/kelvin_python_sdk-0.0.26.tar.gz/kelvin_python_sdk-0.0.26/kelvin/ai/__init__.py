try:
    from .rolling_window import RollingWindow
except ImportError as e:
    raise ImportError(
        "Missing requirements to use this feature. Install with `pip install 'kelvin-python-sdk[ai]'`"
    ) from e


__all__ = ["RollingWindow"]
