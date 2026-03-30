from datetime import datetime
from decimal import Decimal
from typing import Optional
from zoneinfo import ZoneInfo

from pydantic import BaseModel, Field


class RentSchema(BaseModel):
    """
    Define o formato e os valores padrão para um novo registro de aluguel.
    """
    rent_date: Optional[datetime] = Field(default_factory=lambda: datetime.now(tz=ZoneInfo("America/Sao_Paulo")))
    hours_rented: int = Field(default=5, gt=0)
    rent_amount: Decimal = Field(gt=0, max_digits=6, decimal_places=2)
    renter: str = Field(min_length=3, max_length=50)
