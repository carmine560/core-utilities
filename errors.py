"""Shared exception types for core utility modules."""


class CoreUtilitiesError(Exception):
    """Base exception for recoverable core utility errors."""


class BrowserAutomationError(CoreUtilitiesError):
    """Raised when a browser automation action cannot be completed."""


class ConfigBuildError(CoreUtilitiesError):
    """Raised when configuration defaults cannot be built safely."""


class ExternalServiceError(CoreUtilitiesError):
    """Raised when an external service request or API call fails."""


class GuiInteractionError(CoreUtilitiesError):
    """Raised when a GUI helper cannot complete a window interaction."""


class MarketDataError(CoreUtilitiesError):
    """Raised when market data cannot be read, written, or refreshed."""


class ProcessStateError(CoreUtilitiesError):
    """Raised when a required process state prevents an operation."""


class ScraperError(CoreUtilitiesError):
    """Raised when a required page element cannot be scraped safely."""


class TextRecognitionError(CoreUtilitiesError):
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


class UtilityOperationError(CoreUtilitiesError):
    """Raised when a utility helper cannot complete its filesystem task."""


class WidgetPositionError(CoreUtilitiesError):
    """Raised when a widget position string cannot be applied safely."""
