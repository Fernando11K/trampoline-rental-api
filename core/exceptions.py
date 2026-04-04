from http import HTTPStatus


class BusinessError(Exception):
    """Erro de regra de negócio."""

    def __init__(self, message: str, *, code: str | None = None):
        super().__init__(message)
        self.message = message
        self.code = code
        self.status = HTTPStatus.BAD_REQUEST


class ConflictError(BusinessError):
    def __init__(self, message: str, *, code: str | None = None):
        super().__init__(message, code=code)
        self.status = HTTPStatus.CONFLICT


class NotFoundError(BusinessError):
    def __init__(self, message: str, *, code: str | None = None):
        super().__init__(message, code=code)
        self.status = HTTPStatus.NOT_FOUND


class InternalError(BusinessError):
    """Falha técnica; mensagem pode ser exibida ao cliente (sem detalhes internos)."""

    def __init__(self, message: str, *, code: str | None = None):
        super().__init__(message, code=code)
        self.status = HTTPStatus.INTERNAL_SERVER_ERROR
