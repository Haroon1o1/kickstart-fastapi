#error_handler.py
class ErrorHandler:
    """Detects errors such as ball dropping, non-foot kicks, and movement issues."""
    
    def __init__(self):
        self.errors = []

    def detect_errors(self, ball_status, pose_status):
        """Checks for errors and logs them."""
        if ball_status == "No Kick Detected":
            self.errors.append("No ball detected ⚠️")

        if pose_status == "Invalid Kick ❌ (Non-Foot Movement)":
            self.errors.append("Kick used incorrect body part ❌")

    def get_errors(self):
        """Returns list of errors detected."""
        return {"errors": self.errors}

