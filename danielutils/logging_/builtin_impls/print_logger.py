from ..logger_strategy_impl_base import LoggerStrategyImplBase


class PrintLogger(LoggerStrategyImplBase):
    def __init__(self, logger_id: str, channel: str = "all"):
        super().__init__(lambda s: print(s, end=""), logger_id, channel)


__all__ = [
    "PrintLogger"
]
