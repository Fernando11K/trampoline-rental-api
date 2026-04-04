from pydantic import BaseModel


class RentIdPath(BaseModel):
    rent_id: int