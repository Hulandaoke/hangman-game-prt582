#!/usr/bin/env python3
"""
Launcher script for Hangman Game.
Provides options to run either CLI or GUI version.
"""

import sys
import argparse


def main():
    parser = argparse.ArgumentParser(description="Hangman Game Launcher")
    parser.add_argument(
        "--gui", "-g", 
        action="store_true", 
        help="Launch GUI version (default: CLI version)"
    )
    parser.add_argument(
        "--level", 
        choices=["basic", "intermediate"], 
        default="basic",
        help="Game difficulty level (CLI only)"
    )
    parser.add_argument(
        "--lives", 
        type=int, 
        default=6,
        help="Number of lives (CLI only)"
    )
    parser.add_argument(
        "--seconds", 
        type=int, 
        default=15,
        help="Seconds per turn (CLI only)"
    )
    
    args = parser.parse_args()
    
    if args.gui:
        # Launch GUI version
        try:
            from hangman.gui import main as gui_main
            print("Starting Hangman GUI...")
            gui_main()
        except ImportError as e:
            print(f"Error: Could not import GUI module: {e}")
            print("Make sure Tkinter is installed.")
            sys.exit(1)
        except Exception as e:
            print(f"Error starting GUI: {e}")
            sys.exit(1)
    else:
        # Launch CLI version
        try:
            from hangman.cli import main as cli_main
            sys.exit(cli_main([
                "--level", args.level,
                "--lives", str(args.lives),
                "--seconds", str(args.seconds)
            ]))
        except Exception as e:
            print(f"Error starting CLI: {e}")
            sys.exit(1)


if __name__ == "__main__":
    main()