
class UsagePlanLimitException(Exception):
    """Raised when monthly metric or notification usage limits have reached for your organization."""
    def __init__(self, message):
        super().__init__(message)