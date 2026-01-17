"""Custom source scrapers for specific websites.

This module contains custom implementations for sites that need
specific parsing logic beyond the generic HTML/Facebook scrapers.
"""

__all__ = []

try:
    from .freiheitshalle import FreiheitshalleSource
    __all__.append('FreiheitshalleSource')
except ImportError:
    pass

try:
    from .vhs import VHSSource
    __all__.append('VHSSource')
except ImportError:
    pass

try:
    from .hof_stadt import HofStadtSource
    __all__.append('HofStadtSource')
except ImportError:
    pass
