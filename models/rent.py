from decimal import Decimal
from datetime import date

from extensions import db


class Rent(db.Model):
    __tablename__ = 'rent'

    id = db.Column(db.Integer, primary_key=True)
    rent_date = db.Column(db.Date, nullable=False)
    hours_rented = db.Column(db.Integer, nullable=False)
    rent_amount = db.Column(db.Numeric(10, 2), nullable=False)
    renter = db.Column(db.String, nullable=False)
    canceled = db.Column(db.Boolean, nullable=False, default=False)

    def __init__(self, rent_date: date, hours_rented: int, rent_amount: Decimal, renter: str):
        self.rent_date = rent_date
        self.hours_rented = hours_rented
        self.rent_amount = Decimal(rent_amount)
        self.renter = renter

    def __repr__(self):
        return (f"<Rent(id={self.id}, rent_date={self.rent_date}, "
                f"hours_rented={self.hours_rented}, rent_amount={self.rent_amount}, "
                f"renter={self.renter})>")
