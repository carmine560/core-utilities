"""Shared exception types for trading assistant modules."""


class TradingAssistantError(Exception):
    """Base exception for recoverable application errors."""


class ConfigBuildError(TradingAssistantError):
    """Raised when configuration defaults cannot be built safely."""


class ExternalServiceError(TradingAssistantError):
    """Raised when an external service request or API call fails."""


class MarketDataError(TradingAssistantError):
    """Raised when market data cannot be read, written, or refreshed."""
