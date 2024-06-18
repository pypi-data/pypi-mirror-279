from pathlib import Path
from datetime import datetime
from rich.console import Console


# Logging setup
LOG_DIRECTORY = Path.cwd() / "logs"
LOG_FILENAME = datetime.now().isoformat().split('.')[0] + "_kdst_error_log.txt"
LOG_FILEPATH = Path(LOG_DIRECTORY / LOG_FILENAME)
Path.mkdir(Path.cwd() / "logs", exist_ok=True)
log_file = open(LOG_FILEPATH, "wt")

# File-logging console
log_console = Console(
    file=log_file,
    log_time_format="[%Y-%m-%d %X]",
)