from http import HTTPStatus


class BusinessError(Exception):
    """Erro de regra de negócio."""

    def __init__(self, message: str, *, code: str | None = None):
        super().__init__(message)
        self.message = message
        self.code = code
        self.status = HTTPStatus.BAD_REQUEST  # padrão; subclasses sobrescrevem


class ConflictError(BusinessError):
    def __init__(self, message: str, *, code: str | None = None):
        super().__init__(message, code=code)
        self.status = HTTPStatus.CONFLICT


class NotFoundError(BusinessError):
    def __init__(self, message: str, *, code: str | None = None):
        super().__init__(message, code=code)
        self.status = HTTPStatus.NOT_FOUND
