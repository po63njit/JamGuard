#!/usr/bin/env python3
"""Run channel calibration summary from one capture."""

from __future__ import annotations

import logging

from jamguard.utils.logging_utils import configure_logging


def main() -> None:
    configure_logging()
    logging.getLogger(__name__).info("TODO: implement calibration summary pipeline")


if __name__ == "__main__":
    main()
