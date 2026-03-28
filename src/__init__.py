"""
BGMI Emulator Bypass Tool Package

Educational tool for understanding emulator detection bypass mechanisms.
"""

__version__ = "1.0.0"
__author__ = "Educational Research"
__license__ = "Educational Use Only"

from .lib_bypass import LibraryBypass
from .gameloop_handler import GameLoopHandler
from .utils import setup_logging

__all__ = [
    'LibraryBypass',
    'GameLoopHandler',
    'setup_logging'
]
