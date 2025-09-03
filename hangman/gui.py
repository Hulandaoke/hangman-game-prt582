"""
Tkinter GUI interface for Hangman Game.
Provides a graphical interface while maintaining the core game logic.
"""
from __future__ import annotations
import tkinter as tk
from tkinter import ttk, messagebox, font
import threading
import time
from typing import Optional

from .engine import HangmanGame
from .words import BASIC_WORDS, INTERMEDIATE_PHRASES


class HangmanGUI:
    """Tkinter-based GUI for Hangman game"""
    
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Hangman Game")
        self.root.geometry("600x500")
        self.root.resizable(False, False)
        
        # Game state
        self.game: Optional[HangmanGame] = None
        self.timer_running = False
        self.current_time_left = 0
        
        # Setup GUI
        self.setup_styles()
        self.create_widgets()
        self.setup_layout()
        self.bind_events()
        
        # Start new game
        self.new_game()
    
    def setup_styles(self):
        """Configure GUI styles"""
        self.title_font = font.Font(family="Arial", size=16, weight="bold")
        self.word_font = font.Font(family="Courier", size=24, weight="bold")
        self.button_font = font.Font(family="Arial", size=10)
        self.info_font = font.Font(family="Arial", size=10)
    
    def create_widgets(self):
        """Create all GUI widgets"""
        # Main frame
        self.main_frame = ttk.Frame(self.root, padding="10")
        
        # Title
        self.title_label = tk.Label(
            self.main_frame, 
            text="HANGMAN GAME", 
            font=self.title_font,
            fg="darkblue"
        )
        
        # Game info frame
        self.info_frame = ttk.Frame(self.main_frame)
        
        # Level and settings
        self.level_frame = ttk.Frame(self.info_frame)
        tk.Label(self.level_frame, text="Level:", font=self.info_font).grid(row=0, column=0, sticky="w")
        self.level_var = tk.StringVar(value="basic")
        self.level_combo = ttk.Combobox(self.level_frame, textvariable=self.level_var, 
                                       values=["basic", "intermediate"], state="readonly", width=10)
        
        tk.Label(self.level_frame, text="Lives:", font=self.info_font).grid(row=0, column=2, sticky="w", padx=(20,0))
        self.lives_var = tk.StringVar(value="6")
        self.lives_spin = tk.Spinbox(self.level_frame, from_=3, to=10, textvariable=self.lives_var, width=5)
        
        tk.Label(self.level_frame, text="Timeout(s):", font=self.info_font).grid(row=0, column=4, sticky="w", padx=(20,0))
        self.timeout_var = tk.StringVar(value="15")
        self.timeout_spin = tk.Spinbox(self.level_frame, from_=5, to=30, textvariable=self.timeout_var, width=5)
        
        # Word display
        self.word_frame = ttk.Frame(self.main_frame)
        self.word_label = tk.Label(
            self.word_frame, 
            text="_ _ _ _ _", 
            font=self.word_font,
            fg="darkgreen"
        )
        
        # Game status
        self.status_frame = ttk.Frame(self.main_frame)
        self.lives_label = tk.Label(self.status_frame, text="Lives: 6", font=self.info_font)
        self.hint_label = tk.Label(self.status_frame, text="Word has 5 letters", font=self.info_font)
        self.timer_label = tk.Label(self.status_frame, text="Time: 15s", font=self.info_font, fg="red")
        
        # Input frame
        self.input_frame = ttk.Frame(self.main_frame)
        tk.Label(self.input_frame, text="Enter a letter:", font=self.info_font).grid(row=0, column=0, sticky="w")
        self.letter_var = tk.StringVar()
        self.letter_entry = tk.Entry(self.input_frame, textvariable=self.letter_var, width=5, font=self.info_font)
        self.guess_button = tk.Button(self.input_frame, text="Guess", command=self.make_guess, font=self.button_font)
        
        # Guessed letters display
        self.guessed_frame = ttk.Frame(self.main_frame)
        tk.Label(self.guessed_frame, text="Guessed letters:", font=self.info_font).grid(row=0, column=0, sticky="w")
        self.guessed_label = tk.Label(self.guessed_frame, text="None", font=self.info_font, fg="gray")
        
        # Statistics frame
        self.stats_frame = ttk.LabelFrame(self.main_frame, text="Statistics", padding="10")
        self.correct_label = tk.Label(self.stats_frame, text="Correct: 0", font=self.info_font)
        self.wrong_label = tk.Label(self.stats_frame, text="Wrong: 0", font=self.info_font)
        
        # Control buttons
        self.button_frame = ttk.Frame(self.main_frame)
        self.new_game_button = tk.Button(self.button_frame, text="New Game", command=self.new_game, font=self.button_font)
        self.exit_button = tk.Button(self.button_frame, text="Exit", command=self.root.quit, font=self.button_font)
        
        # Result display
        self.result_frame = ttk.Frame(self.main_frame)
        self.result_label = tk.Label(self.result_frame, text="", font=self.title_font)
    
    def setup_layout(self):
        """Arrange widgets in the window"""
        self.main_frame.pack(fill="both", expand=True)
        
        # Title
        self.title_label.pack(pady=(0, 20))
        
        # Game info
        self.info_frame.pack(fill="x", pady=(0, 10))
        self.level_frame.pack()
        self.level_combo.grid(row=0, column=1, padx=(5, 0))
        self.lives_spin.grid(row=0, column=3, padx=(5, 0))
        self.timeout_spin.grid(row=0, column=5, padx=(5, 0))
        
        # Word display
        self.word_frame.pack(pady=20)
        self.word_label.pack()
        
        # Status
        self.status_frame.pack(fill="x", pady=(0, 10))
        self.lives_label.pack(side="left")
        self.hint_label.pack(side="left", padx=(20, 0))
        self.timer_label.pack(side="right")
        
        # Input
        self.input_frame.pack(pady=10)
        tk.Label(self.input_frame, text="Enter a letter:", font=self.info_font).grid(row=0, column=0, sticky="w")
        self.letter_entry.grid(row=0, column=1, padx=(10, 5))
        self.guess_button.grid(row=0, column=2)
        
        # Guessed letters
        self.guessed_frame.pack(fill="x", pady=10)
        self.guessed_label.grid(row=0, column=1, padx=(10, 0), sticky="w")
        
        # Statistics
        self.stats_frame.pack(fill="x", pady=10)
        self.correct_label.pack(side="left")
        self.wrong_label.pack(side="left", padx=(20, 0))
        
        # Result
        self.result_frame.pack(pady=10)
        self.result_label.pack()
        
        # Buttons
        self.button_frame.pack(pady=20)
        self.new_game_button.pack(side="left", padx=(0, 10))
        self.exit_button.pack(side="left")
    
    def bind_events(self):
        """Bind keyboard and other events"""
        self.letter_entry.bind('<Return>', lambda e: self.make_guess())
        self.letter_entry.bind('<KeyRelease>', self.on_letter_change)
        self.root.bind('<F5>', lambda e: self.new_game())
        
        # Focus on entry
        self.letter_entry.focus_set()
    
    def choose_answer(self, level: str) -> str:
        """Choose a random word based on level"""
        import random
        rng = random.SystemRandom()
        return rng.choice(BASIC_WORDS if level == "basic" else INTERMEDIATE_PHRASES)
    
    def new_game(self):
        """Start a new game"""
        # Stop any running timer
        self.timer_running = False
        
        # Get settings
        level = self.level_var.get()
        lives = int(self.lives_var.get())
        timeout = int(self.timeout_var.get())
        
        # Create new game
        answer = self.choose_answer(level)
        self.game = HangmanGame(answer=answer, lives=lives, seconds_per_turn=timeout)
        
        # Reset UI
        self.update_display()
        self.result_label.config(text="", fg="black")
        self.letter_var.set("")
        self.letter_entry.config(state="normal")
        self.guess_button.config(state="normal")
        
        # Start timer
        self.start_timer()
        
        # Focus on entry
        self.letter_entry.focus_set()
    
    def make_guess(self):
        """Process a letter guess"""
        if not self.game or self.game.state.status() != "playing":
            return
        
        letter = self.letter_var.get().strip().lower()
        
        # Validate input
        if not letter or len(letter) != 1 or not letter.isalpha():
            messagebox.showwarning("Invalid Input", "Please enter a single letter only.")
            self.letter_var.set("")
            return
        
        # Make guess
        self.game.start_turn(time.monotonic())
        ok, count = self.game.guess(letter)
        
        # Update display
        self.update_display()
        
        # Clear input
        self.letter_var.set("")
        
        # Check game status
        if self.game.state.status() != "playing":
            self.end_game()
        else:
            # Restart timer for next turn
            self.start_timer()
    
    def start_timer(self):
        """Start the countdown timer"""
        if not self.game:
            return
            
        self.timer_running = True
        self.current_time_left = self.game.state.seconds_per_turn
        self.game.start_turn(time.monotonic())
        
        # Start timer thread
        threading.Thread(target=self.timer_thread, daemon=True).start()
    
    def timer_thread(self):
        """Timer thread for countdown"""
        while self.timer_running and self.current_time_left > 0:
            # Update timer display
            self.root.after(0, self.update_timer_display)
            
            time.sleep(0.1)
            self.current_time_left -= 0.1
            
            # Check if game timed out
            if self.game and self.timer_running:
                timed_out = self.game.tick(time.monotonic())
                if timed_out:
                    self.root.after(0, self.handle_timeout)
                    break
    
    def update_timer_display(self):
        """Update timer display on main thread"""
        if self.timer_running and self.current_time_left > 0:
            self.timer_label.config(text=f"Time: {int(self.current_time_left)}s")
        else:
            self.timer_label.config(text="Time: 0s")
    
    def handle_timeout(self):
        """Handle timer timeout"""
        self.timer_running = False
        messagebox.showinfo("Time's Up!", "Time's up! Life -1")
        self.update_display()
        
        if self.game and self.game.state.status() == "playing":
            self.start_timer()
        elif self.game:
            self.end_game()
    
    def update_display(self):
        """Update all game displays"""
        if not self.game:
            return
        
        # Update word display
        word_display = " ".join(self.game.state.masked_answer())
        self.word_label.config(text=word_display)
        
        # Update game info
        self.lives_label.config(text=f"Lives: {self.game.state.lives}")
        self.hint_label.config(text=f"Word has {self.game.state.get_word_length()} letters")
        
        # Update guessed letters
        guessed = self.game.state.get_guessed_letters()
        self.guessed_label.config(text=guessed)
        
        # Update statistics
        self.correct_label.config(text=f"Correct: {self.game.state.get_correct_guesses()}")
        self.wrong_label.config(text=f"Wrong: {self.game.state.get_wrong_guesses()}")
    
    def end_game(self):
        """Handle game end"""
        self.timer_running = False
        
        if not self.game:
            return
        
        # Disable input
        self.letter_entry.config(state="disabled")
        self.guess_button.config(state="disabled")
        
        # Show result
        answer = self.game.state.answer
        if self.game.state.is_won():
            result_text = "Congratulations! You successfully guessed the word!"
            result_color = "green"
            detail = f"You won with {self.game.state.lives} lives remaining!"
        else:
            result_text = "Game Over! You failed to guess the word."
            result_color = "red"
            detail = "Better luck next time!"
        
        self.result_label.config(text=result_text, fg=result_color)
        
        # Show detailed result
        stats = (
            f"Answer: {answer}\n\n"
            f"Statistics:\n"
            f"• Letters guessed: {self.game.state.get_guessed_letters()}\n"
            f"• Correct guesses: {self.game.state.get_correct_guesses()}\n"
            f"• Wrong guesses: {self.game.state.get_wrong_guesses()}\n"
            f"• Lives remaining: {self.game.state.lives}\n\n"
            f"{detail}"
        )
        
        # Ask for new game
        response = messagebox.askyesno(
            "Game Over", 
            f"{stats}\n\nDo you want to play again?"
        )
        
        if response:
            self.new_game()
        # If no, just leave the game ended state
    
    def on_letter_change(self, event):
        """Handle letter entry changes"""
        # Limit to single character
        text = self.letter_var.get()
        if len(text) > 1:
            self.letter_var.set(text[-1])
    
    def run(self):
        """Start the GUI application"""
        self.root.mainloop()


def main():
    """Main entry point for GUI version"""
    app = HangmanGUI()
    app.run()


if __name__ == "__main__":
    main()