__all__ = ("TelegramError",)


class TelegramError(Exception):
    def __init__(self, error_code: int, description: str) -> None:
        super().__init__(f"{description} - error code {error_code}.")
