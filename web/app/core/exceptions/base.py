class NovaHubException(Exception):
    """
    NovaHub asosiy exception klassi.

    Barcha loyiha exceptionlari ushbu klassdan
    meros olishi kerak.
    """

    def __init__(
        self,
        message: str,
        *,
        error_code: str = "NOVAHUB_ERROR",
        status_code: int = 400,
    ):
        self.message = message
        self.error_code = error_code
        self.status_code = status_code

        super().__init__(message)
