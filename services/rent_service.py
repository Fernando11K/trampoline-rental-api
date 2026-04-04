import logging

from sqlalchemy import select, exists

from core.exceptions import BusinessError, ConflictError, InternalError, NotFoundError
from extensions import db
from models.rent import Rent
from schemas.rent_schema import RentSchema, RentViewSchema  # FIXME verificar

logger = logging.getLogger(__name__)


class RentService:
    ALUGUEL_NAO_LOCALIZADO = "Aluguel não localizado"

    def add_rent(self, payload: RentSchema) -> tuple[dict, int]:
        try:
            if self._exists_by_rent_date(payload.rent_date):
                logger.info(
                    "Aluguel rejeitado: data %s já possui registro",
                    payload.rent_date,
                )
                raise ConflictError("Já existe um aluguel para a data informada")

            rent = Rent(payload.rent_date, payload.hours_rented, payload.rent_amount, payload.renter)
            db.session.add(rent)
            db.session.commit()

            logger.info("Aluguel criado id=%s rent_date=%s", rent.id, rent.rent_date)
            return self._rent_to_view(rent), 201
        except BusinessError:
            raise
        except Exception:
            db.session.rollback()
            logger.exception("Falha ao registrar aluguel")
            raise InternalError(
                "Não foi possível registrar o aluguel. Tente novamente.",
            )

    def get_by_id(self, rent_id: int) -> tuple[dict, int]:
        try:
            stmt = select(Rent).where(Rent.id == rent_id)
            rent = db.session.scalars(stmt).first()
            if not rent:
                error_message = self.ALUGUEL_NAO_LOCALIZADO
                logger.info("%s id=%s", error_message, rent_id)
                raise NotFoundError(error_message)

            return self._rent_to_view(rent), 200
        except BusinessError:
            raise
        except Exception:
            db.session.rollback()
            logger.exception("Falha ao consultar aluguel id=%s", rent_id)
            raise InternalError("Não foi possível consultar o aluguel. Tente novamente.")

    def get_all(self) -> tuple[list[dict], int]:
        try:
            stmt = select(Rent)
            rents = db.session.scalars(stmt).all()
            logger.debug("Listando aluguéis: %s registro(s)", len(rents))

            lista_rents = []
            for r in rents:
                lista_rents.append(self._rent_to_view(r))

            return lista_rents, 200

        except Exception:
            db.session.rollback()
            logger.exception("Falha ao listar aluguéis")
            raise InternalError(
                "Não foi possível listar os aluguéis. Tente novamente.",
            )


    def cancel(self, rent_id: int):
        rent = db.session.get(Rent, rent_id)
        if not rent:
            raise NotFoundError(self.ALUGUEL_NAO_LOCALIZADO)
        db.session.delete(rent)
        db.session.commit()
        return {"message": 'Aluguel cancelado com sucesso!' }, 200

    def delete_by_id(self, rent_id: int):
        rent = db.session.get(Rent, rent_id)
        if not rent:
            raise NotFoundError(self.ALUGUEL_NAO_LOCALIZADO)
        db.session.delete(rent)
        db.session.commit()
        return {"message": 'Aluguel cancelado com sucesso!' }, 200

    def _rent_to_view(self, rent: Rent) -> dict:
        return RentViewSchema.model_validate(rent).model_dump(mode="json")

    def _exists_by_rent_date(self, rent_date) -> bool:
        stmt = select(exists().where(Rent.rent_date == rent_date))
        return db.session.scalar(stmt)


