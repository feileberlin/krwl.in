"""Custom source scrapers for specific websites.

This module contains custom implementations for sites that need
specific parsing logic beyond the generic HTML/Facebook scrapers.
"""

import logging

logger = logging.getLogger(__name__)

__all__ = []

try:
    from .freiheitshalle import FreiheitshalleSource
    __all__.append('FreiheitshalleSource')
except ImportError as exc:
    logger.debug(
        "Optional custom source 'FreiheitshalleSource' could not be imported: %s",
        exc,
    )

try:
    from .vhs import VHSSource
    __all__.append('VHSSource')
except ImportError as exc:
    logger.debug(
        "Optional custom source 'VHSSource' could not be imported: %s",
        exc,
    )

try:
    from .hof_stadt import HofStadtSource
    __all__.append('HofStadtSource')
except ImportError as exc:
    logger.debug(
        "Optional custom source 'HofStadtSource' could not be imported: %s",
        exc,
    )
