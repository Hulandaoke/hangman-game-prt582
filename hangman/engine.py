from __future__ import annotations
from dataclasses import dataclass, field
from typing import Set, Optional, Tuple

REVEAL_CHAR = "_"


@dataclass
class HangmanState:
    answer: str
    letters_guessed: Set[str] = field(default_factory=set)
    lives: int = 6
    last_tick: Optional[float] = None
    seconds_per_turn: int = 15
    score: int = 0  # TDD: Add score field

    def masked_answer(self) -> str:
        out = []
        for ch in self.answer:
            if ch.isalpha():
                out.append(ch if ch.lower() in self.letters_guessed else REVEAL_CHAR)
            else:
                out.append(ch)
        return "".join(out)

    def is_won(self) -> bool:
        return all((not c.isalpha()) or (c.lower() in self.letters_guessed) for c in self.answer)

    def is_lost(self) -> bool:
        return self.lives <= 0

    def status(self) -> str:
        if self.is_won():
            return "won"
        if self.is_lost():
            return "lost"
        return "playing"
    
    def get_word_length(self) -> int:
        """返回单词中字母的总数量（不包括空格等非字母字符）"""
        return sum(1 for c in self.answer if c.isalpha())
    
    def get_guessed_letters(self) -> str:
        """返回已经猜过的字母，按字母顺序排列"""
        return ', '.join(sorted(self.letters_guessed)) if self.letters_guessed else 'None'
    
    def get_correct_guesses(self) -> int:
        """返回正确猜测的次数"""
        return sum(1 for letter in self.letters_guessed if letter in self.answer)
    
    def get_wrong_guesses(self) -> int:
        """返回错误猜测的次数"""
        return sum(1 for letter in self.letters_guessed if letter not in self.answer)


class HangmanGame:
    def __init__(self, answer: str, lives: int = 6, seconds_per_turn: int = 15):
        self.state = HangmanState(answer=answer.lower(), lives=lives, seconds_per_turn=seconds_per_turn)
        self.state.last_tick = None

    def start_turn(self, now: float) -> None:
        self.state.last_tick = now

    def tick(self, now: float) -> bool:
        if self.state.status() != "playing":
            return False
        if self.state.last_tick is None:
            self.state.last_tick = now
            return False
        elapsed = now - self.state.last_tick
        if elapsed >= self.state.seconds_per_turn:
            self.state.lives -= 1
            self.state.last_tick = now
            return True
        return False

    def guess(self, letter: str) -> Tuple[bool, int]:
        if self.state.status() != "playing":
            return False, 0
        if not letter or len(letter) != 1 or not letter.isalpha():
            return False, 0
        letter = letter.lower()
        if letter in self.state.letters_guessed:
            return (letter in self.state.answer), self.state.answer.count(letter) if letter in self.state.answer else 0
        self.state.letters_guessed.add(letter)
        if letter in self.state.answer:
            # TDD: Add score for correct guess
            self.state.score += 10
            return True, self.state.answer.count(letter)
        # TDD: Subtract score for wrong guess
        self.state.score -= 5
        self.state.lives -= 1
        return False, 0
