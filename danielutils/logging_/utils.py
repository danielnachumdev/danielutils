import logging
import sys
import io
from typing import Optional, Dict, List


class UTF8StreamHandler(logging.StreamHandler):
    """Custom StreamHandler that ensures UTF-8 encoding."""

    def __init__(self, stream=None) -> None:
        if stream is None:
            stream = sys.stdout
        super().__init__(stream)
        # Ensure the stream uses UTF-8 encoding
        if hasattr(stream, 'reconfigure'):
            try:
                stream.reconfigure(encoding='utf-8', errors='replace')
            except (AttributeError, OSError):
                pass

    def emit(self, record):
        try:
            msg = self.format(record)
            # Ensure the message is properly encoded
            if isinstance(msg, str):
                # Write as UTF-8 bytes to handle Unicode properly
                self.stream.write(msg + self.terminator)
            else:
                self.stream.write(str(msg) + self.terminator)
            self.flush()
        except UnicodeError:
            # Fallback for Unicode issues
            try:
                self.stream.write(f"Unicode error in log: {record.getMessage()}\n")
                self.flush()
            except Exception:
                # Last resort - write to stderr
                sys.stderr.write(f"Critical logging error: {record.getMessage()}\n")


class ExtraDataFormatter(logging.Formatter):
    """Custom formatter that includes extra data from log records."""

    def format(self, record: logging.LogRecord) -> str:
        try:
            # Get the base formatted message
            base_message = super().format(record)

            # Check for data in two ways:
            # 1. Direct 'data' attribute
            # 2. 'data' key inside 'extra' dict
            data = getattr(record, 'data', None)
            if data is None:
                extra = getattr(record, 'extra', None)
                if extra and isinstance(extra, dict):
                    data = extra.get('data')

            if data and isinstance(data, dict):
                # Format data as key=value pairs, sorted alphabetically by key
                # Handle Unicode characters safely
                sorted_items = sorted(data.items())
                data_pairs = []
                for k, v in sorted_items:
                    try:
                        # Ensure both key and value are properly encoded
                        k_str = str(k) if k is not None else 'None'
                        v_str = str(v) if v is not None else 'None'
                        data_pairs.append(f"{k_str}={v_str}")
                    except UnicodeError:
                        # Fallback for problematic Unicode characters
                        data_pairs.append(f"{repr(k)}={repr(v)}")

                data_str = " | " + " | ".join(data_pairs)
                return base_message + data_str

            return base_message
        except UnicodeError as e:
            # Fallback for any Unicode issues
            return f"Unicode error in log formatting: {e} | {record.getMessage()}"


class DanielUtilsLogFilter(logging.Filter):
    """Filter to exclude danielutils logs when requested."""

    def __init__(self, exclude_danielutils_logs: bool = True):
        super().__init__()
        self.exclude_danielutils_logs = exclude_danielutils_logs

    def filter(self, record: logging.LogRecord) -> bool:
        """
        Filter log records based on whether danielutils logs should be excluded.
        
        Args:
            record: The log record to filter
            
        Returns:
            True if the record should be logged, False otherwise
        """
        if not self.exclude_danielutils_logs:
            return True

        # Check if the logger name starts with 'danielutils'
        logger_name = record.name
        return not logger_name.startswith('danielutils')


def get_logger(name: str) -> logging.Logger:
    """
    Get a logger instance using Python's builtin logging.getLogger.
    
    This function simply delegates to the builtin logger and returns the result.

    Args:
        name: The name of the logger

    Returns:
        Logger instance from Python's builtin logging module
    """
    return logging.getLogger(name)


def setup_stdout_logging_handler(
        level: int = logging.INFO,
        format_string: Optional[str] = None,
        exclude_danielutils_logs: bool = True
) -> logging.Logger:
    """
    Set up stdout logging handler for proper log propagation.
    
    This function adds a handler to the root logger so that all child loggers
    will have their messages handled. This is the recommended approach for
    logging configuration as it allows proper log propagation without
    duplicating handlers on every logger.

    Args:
        level: The logging level (default: INFO)
        format_string: Custom format string for log messages
        exclude_danielutils_logs: Whether to exclude logs from danielutils modules (default: True)

    Returns:
        Root logger instance with the new handler added
    """
    if format_string is None:
        format_string = '%(asctime)s - %(name)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s'

    # Get root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(level)

    # Create console handler that outputs to stdout with UTF-8 encoding
    console_handler = UTF8StreamHandler(sys.stdout)
    console_handler.setLevel(level)

    # Add filter to exclude danielutils logs if requested
    if exclude_danielutils_logs:
        danielutils_filter = DanielUtilsLogFilter(exclude_danielutils_logs=True)
        console_handler.addFilter(danielutils_filter)

    # Create formatter
    formatter = ExtraDataFormatter(format_string)
    console_handler.setFormatter(formatter)

    # Add handler to root logger
    root_logger.addHandler(console_handler)

    return root_logger


def get_logger_handlers() -> Dict[str, List[logging.Handler]]:
    """
    Get all registered loggers and their handlers.

    Returns:
        Dictionary mapping logger names to lists of their registered handlers
    """
    logger_dict = {}

    # Get all existing loggers
    for name in logging.Logger.manager.loggerDict:
        logger = logging.getLogger(name)
        if logger.handlers:
            logger_dict[name] = logger.handlers.copy()

    # Also include the root logger if it has handlers
    root_logger = logging.getLogger()
    if root_logger.handlers:
        logger_dict['root'] = root_logger.handlers.copy()

    return logger_dict


__all__ = [
    "UTF8StreamHandler",
    "ExtraDataFormatter",
    "DanielUtilsLogFilter",
    "get_logger",
    "setup_stdout_logging_handler",
    "get_logger_handlers",
]
