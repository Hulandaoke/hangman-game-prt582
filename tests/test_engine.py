import time
from hangman.engine import HangmanGame

def test_masked_and_spaces():
    g = HangmanGame(answer="unit testing")
    assert g.state.masked_answer() == "____ _______"
    g.state.letters_guessed.update({"t","n"})
    assert g.state.masked_answer() == "_n_t t__t_n_"

def test_correct_reveals_all():
    g = HangmanGame(answer="banana")
    ok, count = g.guess("a")
    assert ok and count == 3

def test_wrong_reduces_life():
    g = HangmanGame(answer="python", lives=2)
    ok, _ = g.guess("z")
    assert not ok and g.state.lives == 1

def test_duplicate_no_penalty():
    g = HangmanGame(answer="data", lives=2)
    g.guess("a")
    lives = g.state.lives
    g.guess("a")
    assert g.state.lives == lives

def test_win_and_loss():
    g = HangmanGame(answer="go")
    g.guess("g"); g.guess("o")
    assert g.state.is_won()
    h = HangmanGame(answer="hi", lives=1)
    h.guess("z")
    assert h.state.is_lost()

def test_timer_timeout():
    g = HangmanGame(answer="test", lives=3, seconds_per_turn=1)
    t0 = time.monotonic()
    g.start_turn(t0)
    assert g.tick(t0 + 1.1) is True
    assert g.state.lives == 2

def test_get_word_length():
    g = HangmanGame(answer="unit testing")
    assert g.state.get_word_length() == 11  # "unittesting"去掉空格后有11个字母
    h = HangmanGame(answer="python")
    assert h.state.get_word_length() == 6

def test_statistics_methods():
    g = HangmanGame(answer="test")
    # 初始状态
    assert g.state.get_guessed_letters() == "None"
    assert g.state.get_correct_guesses() == 0
    assert g.state.get_wrong_guesses() == 0
    
    # 猜一个正确的字母
    g.guess("t")
    assert "t" in g.state.get_guessed_letters()
    assert g.state.get_correct_guesses() == 1
    assert g.state.get_wrong_guesses() == 0
    
    # 猜一个错误的字母
    g.guess("z")
    assert "z" in g.state.get_guessed_letters()
    assert g.state.get_correct_guesses() == 1
    assert g.state.get_wrong_guesses() == 1

def test_timer_functionality():
    """测试计时器相关功能的基本逻辑"""
    from hangman.cli import HAS_SELECT
    # 基本检查：确保计时器模块可以正常导入和配置
    assert isinstance(HAS_SELECT, bool)
    
    # 测试时间相关的游戏逻辑
    g = HangmanGame(answer="test", lives=3, seconds_per_turn=2)
    start_time = time.monotonic()
    g.start_turn(start_time)
    
    # 测试计时器超时逻辑
    timeout_occurred = g.tick(start_time + 2.1)
    assert timeout_occurred is True
    assert g.state.lives == 2
