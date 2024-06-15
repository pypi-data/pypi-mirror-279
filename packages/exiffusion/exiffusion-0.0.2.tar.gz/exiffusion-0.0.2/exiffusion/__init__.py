from pathlib import Path
import logging

from rich.logging import RichHandler

logging.basicConfig(
    level="INFO",
    format="%(message)s",
    datefmt="[%X]",
    handlers=[RichHandler(rich_tracebacks=True)],
)

CUR_DIR = Path(__file__).parent

ROOT_DIR = CUR_DIR.parent
