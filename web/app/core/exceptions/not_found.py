from app.core.exceptions.base import NovaHubException


class NotFoundException(NovaHubException):
    """
    Resurs topilmagan holatlar uchun exception.
    """

    def __init__(
        self,
        message: str = "Resource not found.",
        *,
        error_code: str = "NOT_FOUND",
    ):
        super().__init__(
            message=message,
            error_code=error_code,
            status_code=404,
        )
