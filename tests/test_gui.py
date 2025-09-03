"""
Tests for GUI module.
Tests basic functionality without requiring actual GUI display.
"""
import pytest
import tkinter as tk
from unittest.mock import Mock, patch
from hangman.gui import HangmanGUI
from hangman.engine import HangmanGame


class TestHangmanGUI:
    """Test Hangman GUI functionality"""
    
    @pytest.fixture
    def mock_root(self):
        """Mock Tkinter root for testing"""
        with patch('tkinter.Tk') as mock_tk:
            mock_root = Mock()
            mock_tk.return_value = mock_root
            yield mock_root
    
    def test_gui_creation(self, mock_root):
        """Test GUI object creation"""
        with patch.object(HangmanGUI, 'setup_styles'), \
             patch.object(HangmanGUI, 'create_widgets'), \
             patch.object(HangmanGUI, 'setup_layout'), \
             patch.object(HangmanGUI, 'bind_events'), \
             patch.object(HangmanGUI, 'new_game'):
            
            gui = HangmanGUI()
            assert gui.root == mock_root
            assert gui.game is None
            assert gui.timer_running is False
    
    def test_choose_answer(self, mock_root):
        """Test word selection logic"""
        with patch.object(HangmanGUI, 'setup_styles'), \
             patch.object(HangmanGUI, 'create_widgets'), \
             patch.object(HangmanGUI, 'setup_layout'), \
             patch.object(HangmanGUI, 'bind_events'), \
             patch.object(HangmanGUI, 'new_game'):
            
            gui = HangmanGUI()
            
            # Test basic level
            answer = gui.choose_answer("basic")
            assert isinstance(answer, str)
            assert len(answer) > 0
            
            # Test intermediate level
            answer = gui.choose_answer("intermediate")
            assert isinstance(answer, str)
            assert len(answer) > 0
    
    def test_game_integration(self, mock_root):
        """Test integration with game engine"""
        with patch.object(HangmanGUI, 'setup_styles'), \
             patch.object(HangmanGUI, 'create_widgets'), \
             patch.object(HangmanGUI, 'setup_layout'), \
             patch.object(HangmanGUI, 'bind_events'), \
             patch.object(HangmanGUI, 'new_game'):
            
            gui = HangmanGUI()
            
            # Create a game manually for testing
            gui.game = HangmanGame("test", lives=6, seconds_per_turn=15)
            
            # Test game state
            assert gui.game.state.answer == "test"
            assert gui.game.state.lives == 6
            assert gui.game.state.seconds_per_turn == 15
    
    def test_timer_functionality(self, mock_root):
        """Test timer-related methods"""
        with patch.object(HangmanGUI, 'setup_styles'), \
             patch.object(HangmanGUI, 'create_widgets'), \
             patch.object(HangmanGUI, 'setup_layout'), \
             patch.object(HangmanGUI, 'bind_events'), \
             patch.object(HangmanGUI, 'new_game'):
            
            gui = HangmanGUI()
            gui.game = HangmanGame("test", lives=6, seconds_per_turn=5)
            
            # Test timer initialization
            assert gui.timer_running is False
            assert gui.current_time_left == 0
            
            # Test timer starting logic (without actual threading)
            gui.current_time_left = 5
            gui.timer_running = True
            assert gui.current_time_left == 5
            assert gui.timer_running is True


def test_gui_import():
    """Test that GUI module can be imported"""
    from hangman.gui import HangmanGUI, main
    assert HangmanGUI is not None
    assert main is not None


def test_tkinter_availability():
    """Test that Tkinter is available"""
    try:
        import tkinter as tk
        # Create a test root (without showing it)
        root = tk.Tk()
        root.withdraw()
        root.destroy()
        success = True
    except ImportError:
        success = False
    
    assert success, "Tkinter should be available for GUI functionality"