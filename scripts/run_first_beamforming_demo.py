#!/usr/bin/env python3
"""Run first offline beamforming demonstration script."""

from __future__ import annotations

import logging

from jamguard.utils.logging_utils import configure_logging


def main() -> None:
    configure_logging()
    logging.getLogger(__name__).info("TODO: implement beamforming demo pipeline")


if __name__ == "__main__":
    main()
