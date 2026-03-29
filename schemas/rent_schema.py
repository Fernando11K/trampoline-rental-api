from datetime import datetime, timezone
from decimal import Decimal
from typing import Optional
from zoneinfo import ZoneInfo
from pydantic import BaseModel, Field


class RentSchema(BaseModel):
    """
    Define o formato e os valores padrão para um novo registro de aluguel.
    """
    rent_date: Optional[datetime] = Field(default_factory=lambda: datetime.now(tz=ZoneInfo("America/Sao_Paulo")))
    hours_rented: Optional[int] = 5
    rent_amount: Decimal = Decimal('0')
    renter: str = 'NÃO INFORMADO'
