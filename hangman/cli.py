from __future__ import annotations
import argparse, random, sys, time
try:
    import select
    HAS_SELECT = True
except ImportError:
    HAS_SELECT = False
from typing import List
from .engine import HangmanGame
from .words import BASIC_WORDS, INTERMEDIATE_PHRASES

def choose_answer(level: str) -> str:
    rng = random.SystemRandom()
    return rng.choice(BASIC_WORDS if level == "basic" else INTERMEDIATE_PHRASES)

def ask_play_again() -> bool:
    """询问用户是否想要再次游玩"""
    while True:
        choice = input("\nDo you want to play again? (y/n): ").strip().lower()
        if choice in ['y', 'yes']:
            return True
        elif choice in ['n', 'no']:
            return False
        else:
            print("Please enter 'y' for yes or 'n' for no.")

def prompt_with_timer(prompt: str, timeout: int) -> str:
    """带实时倒计时显示的输入提示"""
    if not HAS_SELECT:
        # Fallback for systems without select (like Windows)
        print(f"{prompt}(Timeout: {timeout}s) ", end="", flush=True)
        return input().rstrip("\r\n")
    
    import select
    start_time = time.monotonic()
    sys.stdout.write(f"\r{prompt}[{timeout}s] ")
    sys.stdout.flush()
    
    while True:
        elapsed = time.monotonic() - start_time
        remaining = max(0, timeout - int(elapsed))
        
        if remaining == 0:
            sys.stdout.write("\r" + " " * 50 + "\r")  # 清除行
            return ""
        
        # 更新倒计时显示
        sys.stdout.write(f"\r{prompt}[{remaining}s] ")
        sys.stdout.flush()
        
        # 检查是否有输入
        r, _, _ = select.select([sys.stdin], [], [], 0.1)
        if r:
            result = sys.stdin.readline().rstrip("\r\n")
            sys.stdout.write("\r" + " " * 50 + "\r")  # 清除行
            return result

def prompt_with_timeout(prompt: str, timeout: int) -> str:
    sys.stdout.write(prompt); sys.stdout.flush()
    if not HAS_SELECT:
        # Fallback for systems without select (like Windows)
        return input().rstrip("\r\n")
    import select  # Import here to avoid unbound variable warning
    r, _, _ = select.select([sys.stdin], [], [], timeout)
    if r:
        return sys.stdin.readline().rstrip("\r\n")
    return ""

def play_single_game(level: str, lives: int = 6, seconds_per_turn: int = 15) -> int:
    """执行单次游戏"""
    answer = choose_answer(level)
    game = HangmanGame(answer=answer, lives=lives, seconds_per_turn=seconds_per_turn)
    print("Welcome to Hangman! Level:", level)
    print(f"Hint: The word has {game.state.get_word_length()} letters.")
    while game.state.status() == "playing":
        print("Word:", game.state.masked_answer(), "Lives:", game.state.lives)
        game.start_turn(time.monotonic())
        s = prompt_with_timer("Enter a letter: ", seconds_per_turn)
        timed_out = game.tick(time.monotonic())
        if timed_out and not s:
            print("Time's up! Life -1"); continue
        if not s: print("Try again."); continue
        
        # 验证输入：只接受单个字母
        user_input = s.strip().lower()
        if len(user_input) != 1 or not user_input.isalpha():
            print("Please enter a single letter only."); continue
            
        ok, cnt = game.guess(user_input)
        print(("Correct +" if ok else "Wrong -"), cnt)
    
    # 显示游戏结果和答案
    print("\n" + "="*50)
    print("Answer:", answer)
    
    # 显示游戏统计信息
    print("\nGame Statistics:")
    print(f"  • Letters guessed: {game.state.get_guessed_letters()}")
    print(f"  • Correct guesses: {game.state.get_correct_guesses()}")
    print(f"  • Wrong guesses: {game.state.get_wrong_guesses()}")
    print(f"  • Lives remaining: {game.state.lives}")
    
    if game.state.is_won():
        print("\nCongratulations! You successfully guessed the word!")
        print(f"You won with {game.state.lives} {'life' if game.state.lives == 1 else 'lives'} remaining!")
    else:
        print("\nGame Over! You failed to guess the word.")
        print("Better luck next time!")
    
    print("="*50)
    return 0 if game.state.is_won() else 1

def run(level: str, lives: int = 6, seconds_per_turn: int = 15) -> int:
    """主游戏循环，支持重新开始"""
    while True:
        result = play_single_game(level, lives, seconds_per_turn)
        if not ask_play_again():
            print("Thanks for playing!")
            return result

def main(argv: List[str] | None = None) -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--level", choices=["basic","intermediate"], default="basic")
    p.add_argument("--lives", type=int, default=6)
    p.add_argument("--seconds", type=int, default=15)
    a = p.parse_args(argv)
    return run(a.level, a.lives, a.seconds)

if __name__ == "__main__":
    raise SystemExit(main())
