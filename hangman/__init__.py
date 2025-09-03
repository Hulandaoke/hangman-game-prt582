from .engine import HangmanGame, HangmanState

# Optional GUI import (may not be available on all systems)
try:
    from .gui import HangmanGUI
    GUI_AVAILABLE = True
except ImportError:
    GUI_AVAILABLE = False
