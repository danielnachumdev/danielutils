"""class for convenience"""


class DisablePytestDiscovery:
    """inheriting from this class will disable pytest discovery
    """
    __test__ = False


__all__ = [
    "DisablePytestDiscovery"
]
