import logging
from pathlib import Path

_logger = logging.getLogger("task_manager")
_logger.setLevel(logging.INFO) 

if not _logger.handlers:
    logs_dir = Path(__file__).resolve().parents[2] / "logs"
    logs_dir.mkdir(parents=True, exist_ok=True)

    file_handler = logging.FileHandler(logs_dir / "app.log")
    file_handler.setLevel(logging.DEBUG)

    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)

    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)-8s | %(name)s | %(module)s:%(lineno)d – %(message)s"
    )
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)

    _logger.addHandler(file_handler)
    _logger.addHandler(console_handler)


def get_logger(name: str = "task_manager") -> logging.Logger:
    """
    Return the configured logger instance.
    The global configuration above runs only once, so repeated calls are cheap.
    """
    return logging.getLogger(name)

logger = _logger