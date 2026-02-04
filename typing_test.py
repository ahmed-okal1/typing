"""
Typing Test Module
Core logic for typing tests including WPM, accuracy, and score calculations.
Monkeytype-style implementation with word-by-word validation and accurate error tracking.
"""

import time
from typing import Dict, List


class TypingTest:
    """Manages typing test logic and calculations with Monkeytype-style validation."""
    
    def __init__(self, text: str):
        self.text = text
        self.words = text.split()  # Split into words
        self.start_time = None
        self.end_time = None
        self.user_input = ""
        
        # Track all keystrokes for accurate error counting
        self.total_keystrokes = 0
        self.correct_keystrokes = 0
        self.incorrect_keystrokes = 0
        
        # Track current word progress
        self.current_word_index = 0
        self.current_word_input = ""
        
        # Track completed words
        self.completed_words = []
        
        # Track specific key errors
        self.key_errors = {}
        
    def start(self):
        """Start the typing test timer."""
        self.start_time = time.time()
    
    def finish(self):
        """Finish the typing test timer."""
        self.end_time = time.time()
    
    def get_duration(self) -> float:
        """Get test duration in seconds."""
        if self.start_time and self.end_time:
            return self.end_time - self.start_time
        return 0
    
    def get_current_word(self) -> str:
        """Get the current word that should be typed."""
        if self.current_word_index < len(self.words):
            return self.words[self.current_word_index]
        return ""
    
    def is_current_word_correct(self) -> bool:
        """Check if the current word input matches the expected word."""
        current_word = self.get_current_word()
        return self.current_word_input == current_word
    
    def can_add_space(self) -> bool:
        """Check if user can add a space (only if current word is correct)."""
        return self.is_current_word_correct()
    
    def process_keystroke(self, char: str, is_backspace: bool = False) -> Dict:
        """
        Process a single keystroke and update statistics.
        Returns info about whether the keystroke was accepted.
        """
        if is_backspace:
            # Allow backspace
            if len(self.current_word_input) > 0:
                self.current_word_input = self.current_word_input[:-1]
            return {"accepted": True, "error": False}
        
        # Check if it's a space
        if char == ' ':
            if self.can_add_space():
                # Move to next word
                self.completed_words.append(self.current_word_input)
                self.current_word_index += 1
                self.current_word_input = ""
                self.total_keystrokes += 1
                self.correct_keystrokes += 1
                return {"accepted": True, "error": False}
            else:
                # Reject space if word is not correct
                return {"accepted": False, "error": True}
        
        # Regular character
        current_word = self.get_current_word()
        current_pos = len(self.current_word_input)
        
        # Check if we're still within the word length
        if current_pos < len(current_word):
            is_correct = char == current_word[current_pos]
            self.current_word_input += char
            self.total_keystrokes += 1
            
            if is_correct:
                self.correct_keystrokes += 1
            else:
                self.incorrect_keystrokes += 1
                # Track specific key error (using the expected char)
                expected_char = current_word[current_pos]
                self.key_errors[expected_char] = self.key_errors.get(expected_char, 0) + 1
            
            return {"accepted": True, "error": not is_correct}
        else:
            # Don't allow typing beyond the word length
            return {"accepted": False, "error": True}
    
    def get_full_typed_text(self) -> str:
        """Get the full text typed so far (completed words + current word)."""
        if self.completed_words:
            return ' '.join(self.completed_words) + ' ' + self.current_word_input
        return self.current_word_input
    
    def calculate_wpm(self) -> float:
        """Calculate Words Per Minute (WPM) based on correct characters."""
        duration = self.get_duration()
        if duration == 0:
            return 0
        
        # Use correct keystrokes for WPM calculation
        characters = self.correct_keystrokes
        words = characters / 5
        minutes = duration / 60
        
        return round(words / minutes, 1) if minutes > 0 else 0
    
    def calculate_accuracy(self) -> float:
        """
        Calculate typing accuracy based on ALL keystrokes (including corrected errors).
        This gives the TRUE accuracy, not the final result accuracy.
        """
        if self.total_keystrokes == 0:
            return 100.0
        
        accuracy = (self.correct_keystrokes / self.total_keystrokes * 100)
        return round(accuracy, 1)
    
    def calculate_scores(self) -> Dict[str, float]:
        """Calculate speed and accuracy scores (1-100 scale)."""
        wpm = self.calculate_wpm()
        accuracy = self.calculate_accuracy()
        
        # Speed score: Based on WPM (100 WPM = 100 score)
        speed_score = min(100, round(wpm))
        
        # Accuracy score: Direct percentage
        accuracy_score = round(accuracy)
        
        # Overall score: Average of speed and accuracy
        overall_score = round((speed_score + accuracy_score) / 2)
        
        return {
            "wpm": wpm,
            "accuracy": accuracy,
            "speed_score": speed_score,
            "accuracy_score": accuracy_score,
            "overall_score": overall_score,
            "duration": round(self.get_duration(), 1),
            "total_keystrokes": self.total_keystrokes,
            "correct_keystrokes": self.correct_keystrokes,
            "incorrect_keystrokes": self.incorrect_keystrokes,
            "top_missed_keys": self.get_top_missed_keys()
        }
    
    def get_top_missed_keys(self) -> List[tuple]:
        """Get the top 3 most missed keys."""
        # Sort by count descending
        sorted_errors = sorted(self.key_errors.items(), key=lambda x: x[1], reverse=True)
        return sorted_errors[:3]

    def get_errors_count(self) -> int:
        """Get total number of incorrect keystrokes."""
        return self.incorrect_keystrokes
    
    def get_current_stats(self) -> Dict:
        """Get current statistics during the test."""
        if not self.start_time:
            return {
                "elapsed_time": 0,
                "current_wpm": 0,
                "current_accuracy": 100.0,
                "errors": 0,
                "current_word": self.get_current_word(),
                "current_word_input": self.current_word_input,
                "words_completed": len(self.completed_words),
                "total_words": len(self.words)
            }
        
        elapsed = time.time() - self.start_time
        
        # Calculate current WPM based on correct keystrokes
        if elapsed > 0:
            characters = self.correct_keystrokes
            words = characters / 5
            minutes = elapsed / 60
            current_wpm = round(words / minutes, 1) if minutes > 0 else 0
        else:
            current_wpm = 0
        
        # Calculate current accuracy
        current_accuracy = self.calculate_accuracy()
        
        return {
            "elapsed_time": round(elapsed, 1),
            "current_wpm": current_wpm,
            "current_accuracy": current_accuracy,
            "errors": self.incorrect_keystrokes,
            "current_word": self.get_current_word(),
            "current_word_input": self.current_word_input,
            "words_completed": len(self.completed_words),
            "total_words": len(self.words)
        }
    
    def is_test_complete(self) -> bool:
        """Check if the test is complete (all words typed correctly)."""
        return self.current_word_index >= len(self.words)
