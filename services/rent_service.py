from typing import Dict, Any
from extensions import db
from models.rent import Rent
from schemas.rent_schema import RentSchema



class RentService:

    def add_rent(self, form: RentSchema) -> Dict[str, Any]:
        rent = Rent(form.rent_date,
                    form.hours_rented,
                    form.rent_amount,
                    form.renter
                    )
        db.session.add(rent)
        db.session.commit()

        return {
            "id": rent.id,
            "rent_date": rent.rent_date,
            "hours_rented": rent.hours_rented,
            "rent_amount": rent.rent_amount,
            "renter": rent.renter
        }
