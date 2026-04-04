from pydantic import BaseModel


class ErrorSchema(BaseModel):
    """
    Representa a estrutura padrão de erro retornada pela API.
    """
    message: str
