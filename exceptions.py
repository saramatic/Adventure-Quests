# Custom exceptions
class InvalidCommandError(Exception):
    """Raised when an invalid command is entered."""
    pass


class InvalidActionError(Exception):
    """Raised during combat or item usage for invalid actions."""
    pass


class QuestNotAvailableError(Exception):
    """Raised when a player attempts to start a quest that is unavailable."""
    pass
