"""Shared exception types for trading assistant modules."""


class TradingAssistantError(Exception):
    """Base exception for recoverable application errors."""


class ConfigBuildError(TradingAssistantError):
    """Raised when configuration defaults cannot be built safely."""


class ExternalServiceError(TradingAssistantError):
    """Raised when an external service request or API call fails."""


class MarketDataError(TradingAssistantError):
    """Raised when market data cannot be read, written, or refreshed."""


class ProcessStateError(TradingAssistantError):
    """Raised when a required process state prevents an operation."""


class ScraperError(TradingAssistantError):
    """Raised when a required page element cannot be scraped safely."""


class GuiInteractionError(TradingAssistantError):
    """Raised when a GUI helper cannot complete a window interaction."""


class WidgetPositionError(TradingAssistantError):
    """Raised when a widget position string cannot be applied safely."""


class BrowserAutomationError(TradingAssistantError):
    """Raised when a browser automation action cannot be completed."""


class TextRecognitionError(TradingAssistantError):
    """Raised when OCR cannot produce parseable text within set limits."""

    def __init__(
        self,
        message,
        *,
        attempts,
        last_output,
        region,
        text_type,
    ):
        """Store OCR failure details for callers and diagnostics."""
        super().__init__(message)
        self.attempts = attempts
        self.last_output = last_output
        self.region = region
        self.text_type = text_type


class UtilityOperationError(TradingAssistantError):
    """Raised when a utility helper cannot complete its filesystem task."""


class ActionLookupError(TradingAssistantError):
    """Raised when a requested action is not defined."""

    def __init__(self, message, *, action_name):
        """Store missing action context for callers and diagnostics."""
        super().__init__(message)
        self.action_name = action_name


class ActionExecutionError(TradingAssistantError):
    """Raised when an action definition is invalid at execution time."""

    def __init__(
        self,
        message,
        *,
        action_path,
        instruction_index,
        command,
    ):
        """Store action context for callers and diagnostics."""
        super().__init__(message)
        self.action_path = tuple(action_path)
        self.instruction_index = instruction_index
        self.command = command
