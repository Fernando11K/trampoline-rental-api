from datetime import date
from decimal import Decimal
from pydantic import BaseModel, ConfigDict, Field


class RentSchema(BaseModel):
    rent_date: date
    hours_rented: int = Field(default=5, gt=0)
    rent_amount: Decimal = Field(gt=0, max_digits=10, decimal_places=2)
    renter: str = Field(min_length=3, max_length=50)


class RentViewSchema(BaseModel):
    """
    Retorna todos os aluguéis
    """

    model_config = ConfigDict(from_attributes=True)

    id: int
    rent_date: date
    hours_rented: int
    rent_amount: Decimal
    renter: str
