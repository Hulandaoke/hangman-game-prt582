# Hangman Game PRT582

A Hangman word-guessing game implemented in Python for PRT582 Software Engineering course. Features both CLI and GUI interfaces with real-time timer and comprehensive unit testing.

## Features

- 🖥️ **Dual Interface**: Command Line (CLI) and Graphical (GUI) versions
- ⏰ **Real-time Timer**: Live countdown for each turn
- 📊 **Game Statistics**: Detailed statistics and English prompts
- 🧪 **Unit Testing**: 17 comprehensive tests with pytest
- 🌍 **Cross-platform**: Windows, macOS, and Linux support

## Quick Start

```bash
# Clone and setup
git clone https://github.com/Hulandaoke/hangman-game-prt582.git
cd hangman-game-prt582
pip install pytest

# Run CLI version
python run_hangman.py

# Run GUI version
python run_hangman.py --gui

# Run tests
python -m pytest
```

## Project Structure

```
hangman_project/
├── hangman/          # Main game package
│   ├── cli.py       # Command line interface  
│   ├── engine.py    # Core game logic
│   ├── gui.py       # Graphical interface
│   └── words.py     # Word lists
├── tests/           # Unit tests (17 tests)
├── run_hangman.py   # Main launcher
└── README.md        # Documentation
```

## Course Information

- **Course**: PRT582 Software Engineering
- **Focus**: Unit Testing & Code Architecture  
- **Features**: Modular design, comprehensive testing, dual interfaces
- **Testing Approach**: Unit testing with TDD examples (see `tests/test_tdd_scoring.py`)

## Testing & TDD

The project includes:
- **17 comprehensive unit tests** covering all functionality
- **TDD example module** demonstrating test-driven development
- **Cross-platform compatibility tests**

```bash
# Run all tests
python -m pytest

# Run TDD example (will fail initially)
python -m pytest tests/test_tdd_scoring.py -v
```