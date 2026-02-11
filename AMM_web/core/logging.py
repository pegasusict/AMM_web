"""Centralized logging configuration."""

import logging


def setup_logging(level: int = logging.INFO) -> None:
    """Configure app-wide logging."""
    logging.basicConfig(
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        level=level,
    )
    logging.getLogger("reflex").setLevel(logging.WARNING)
