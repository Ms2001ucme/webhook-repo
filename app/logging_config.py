import logging
from logging.handlers import RotatingFileHandler
import os

def configure_logging(app):
    log_dir = "logs"
    os.makedirs(log_dir, exist_ok=True)

    file_handler = RotatingFileHandler(
        f"{log_dir}/app.log", maxBytes=1_000_000, backupCount=5
    )
    file_handler.setLevel(logging.INFO)

    formatter = logging.Formatter(
        '[%(asctime)s] %(levelname)s in %(module)s: %(message)s'
    )
    file_handler.setFormatter(formatter)

    if not app.logger.handlers:
        app.logger.addHandler(file_handler)
    app.logger.setLevel(logging.INFO)
