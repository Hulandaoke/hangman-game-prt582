from hangman.words import BASIC_WORDS, INTERMEDIATE_PHRASES

def test_basic_words_are_single_words():
    assert all(" " not in w for w in BASIC_WORDS)

def test_intermediate_has_space():
    assert any(" " in p for p in INTERMEDIATE_PHRASES)
