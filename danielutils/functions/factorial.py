import logging
from .logging_.utils import get_logger

logger = get_logger(__name__)


def factorial(n: int) -> int:
    logger.info(f"Computing factorial of {n}")
    if n < 0:
        logger.error(f"Factorial not defined for negative numbers: {n}")
        raise ValueError("Factorial not defined for negative numbers")
    if n == 0 or n == 1:
        return 1
    
    res = 1
    for i in range(2, n + 1):
        res *= i
    
    logger.info(f"Factorial of {n} computed: {res}")
    return res

__all__ = [
    "factorial"
]