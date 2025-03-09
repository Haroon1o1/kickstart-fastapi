#streak_tracker.py

class StreakTracker:
    """Tracks correct and incorrect kicks, longest streak, and error handling."""
    def __init__(self):
        self.current_streak = 0
        self.longest_streak = 0
        self.correct_kicks = 0
        self.incorrect_kicks = 0

    def update_streak(self, kick_status):
        """Updates the streak based on kick validation."""
        if kick_status == "Valid Kick ✅":
            self.correct_kicks += 1
            self.current_streak += 1
            self.longest_streak = max(self.longest_streak, self.current_streak)
        else:
            self.incorrect_kicks += 1
            self.current_streak = 0  # Reset streak on error

    def get_stats(self):
        """Returns session statistics."""
        return {
            "correct_kicks": self.correct_kicks,
            "incorrect_kicks": self.incorrect_kicks,
            "longest_streak": self.longest_streak
        }

