"""Fancy logging"""
import logging
from rich.logging import RichHandler


def configure_logger():
    """Default log format"""
    log_format = "%(asctime)s [bold cyan]%(levelname)s[/] [yellow]-[/] [royal_blue1]%(name)s[/] [yellow]-[/] %(message)s [yellow]([/][chartreuse4]%(filename)s[/]:%(lineno)d[yellow])[/]"
    logging.basicConfig(
        level=logging.INFO, format=log_format, datefmt="[%X]", handlers=[RichHandler(show_time=False, show_level=False, markup=True, tracebacks_show_locals=True, rich_tracebacks=True)]
    )
    return logging.getLogger("kernel")
