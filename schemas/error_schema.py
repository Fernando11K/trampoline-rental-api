from datetime import datetime

from pydantic import BaseModel


class ErrorSchema(BaseModel):
    """
    Representa a estrutura padrão de erro retornada pela API.
    """
    status: int
    error: str
    message: str
    timestamp: datetime
