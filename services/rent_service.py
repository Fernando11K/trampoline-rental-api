import logging

from sqlalchemy import select, exists

from extensions import db
from models.rent import Rent
from schemas.rent_schema import RentSchema, RentViewSchema  # FIXME verificar

logger = logging.getLogger(__name__)


class RentService:

    def add_rent(self, payload: RentSchema) -> tuple[dict, int]:
        if self._exist_by_rent_date(payload.rent_date):
            logger.info(
                "Aluguel rejeitado: data %s já possui registro",
                payload.rent_date,
            )
            return {"message": "Já existe um aluguel para a data informada"}, 409

        rent = Rent(
            payload.rent_date,
            payload.hours_rented,
            payload.rent_amount,
            payload.renter
        )
        try:
            db.session.add(rent)
            db.session.commit()
        except Exception:
            logger.exception("Falha ao persistir aluguel")
            return {"message": "Ops! Tivemos um problema ao registrar o aluguel. Tente novamente."}, 500

        logger.info("Aluguel criado id=%s rent_date=%s", rent.id, rent.rent_date)

        return {
            "id": rent.id,
            "rent_date": rent.rent_date.isoformat() if rent.rent_date else None,
            "hours_rented": rent.hours_rented,
            "rent_amount": float(rent.rent_amount),
            "renter": rent.renter
        }, 201

    def get_by_id(self, rent_id: int) -> tuple[dict, int]:
        stmt = select(Rent).where(Rent.id == rent_id)
        rent = db.session.scalars(stmt).first()
        if not rent:
            error_message: str = "Aluguel não encontrato"
            logger.info(error_message, rent_id)
            return {"message": error_message}, 404

        return self.convert_to_json(rent), 200

    def get_all(self) -> dict:
        stmt = select(Rent)
        rents = db.session.scalars(stmt).all()
        logger.debug("Listando aluguéis: %s registro(s)", len(rents))

        result = []
        for rent in rents:
            item = RentViewSchema.model_validate(rent).model_dump(mode="json")
            result.append(item)
        return self.convert_to_json(result)

    def convert_to_json(self, rent: Rent | list[Rent]) -> dict:
        return RentViewSchema.model_validate(rent).model_dump(mode="json")

    def _exist_by_rent_date(self, rent_date) -> bool:
        stmt = select(exists().where(Rent.rent_date == rent_date))
        return db.session.scalar(stmt)
