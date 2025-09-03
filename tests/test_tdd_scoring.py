"""
TDD Example: Adding a new feature using Test-Driven Development
This module demonstrates how to add a scoring system using TDD approach.
"""

import pytest
from hangman.engine import HangmanGame


class TestScoringSystem:
    """
    TDD Example: Adding a scoring system to the game
    
    RED -> GREEN -> REFACTOR cycle demonstration
    """
    
    def test_initial_score_is_zero(self):
        """RED: Test that fails - scoring system doesn't exist yet"""
        game = HangmanGame("test")
        # This will fail initially - no scoring system implemented
        assert hasattr(game.state, 'score')
        assert game.state.score == 0
    
    def test_correct_guess_increases_score(self):
        """RED: Test that correct guesses increase score"""
        game = HangmanGame("test")
        initial_score = game.state.score
        game.guess("t")  # correct guess
        assert game.state.score > initial_score
    
    def test_wrong_guess_decreases_score(self):
        """RED: Test that wrong guesses decrease score"""
        game = HangmanGame("test")
        initial_score = game.state.score
        game.guess("z")  # wrong guess
        assert game.state.score < initial_score
    
    def test_final_score_calculation(self):
        """RED: Test final score includes time bonus"""
        game = HangmanGame("hi", lives=6, seconds_per_turn=10)
        # Fast completion should give bonus
        game.guess("h")
        game.guess("i")
        assert game.state.is_won()
        # Should have base score + time bonus
        assert game.state.score >= 20  # base points for winning


# TDD Implementation Notes:
# 1. RED: Write failing tests first (above tests will fail)
# 2. GREEN: Implement minimal code to pass tests
# 3. REFACTOR: Improve code while keeping tests green

"""
To implement TDD properly:

1. Run tests first (they should FAIL):
   python -m pytest tests/test_tdd_scoring.py -v

2. Implement minimal scoring in engine.py:
   - Add score field to HangmanState
   - Add scoring logic to guess() method
   - Add time bonus calculation

3. Run tests again (they should PASS)
4. Refactor code while keeping tests green
"""