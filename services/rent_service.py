import logging

from sqlalchemy import select, exists, and_

from core.exceptions import BusinessError, ConflictError, InternalError, NotFoundError
from extensions import db
from models.rent import Rent
from schemas.rent_schema import RentSchema, RentViewSchema

logger = logging.getLogger(__name__)


class RentService:
    ALUGUEL_NAO_LOCALIZADO = "Aluguel não localizado"
    ALUGUEL_ESTA_CANCELADO = "Este aluguel está cancelado"
    MSG_ALUGUEL_CANCELADO = "Aluguel cancelado com sucesso!"

    def add_rent(self, payload: RentSchema) -> tuple[dict, int]:
        try:
            if self._active_rent_on_date(payload.rent_date):
                logger.info(
                    "Aluguel rejeitado: data %s já possui registro",
                    payload.rent_date,
                )
                raise ConflictError(f"Já existe um aluguel agendado para a data {payload.rent_date}")

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
                logger.info("%s id=%s", self.ALUGUEL_NAO_LOCALIZADO, rent_id)
                raise NotFoundError(self.ALUGUEL_NAO_LOCALIZADO)
            if rent.canceled:
                raise BusinessError(self.ALUGUEL_ESTA_CANCELADO)
            
            return self._rent_to_view(rent), 200
        except BusinessError:
            raise
        except Exception:
            db.session.rollback()
            logger.exception("Falha ao consultar aluguel id=%s", rent_id)
            raise InternalError("Não foi possível consultar o aluguel. Tente novamente.")

    def get_all(self) -> tuple[list[dict], int]:
        try:
            stmt = select(Rent).where(Rent.canceled == False)
            rents = db.session.scalars(stmt).all()
            logger.debug("Listando aluguéis ativos: %s registro(s)", len(rents))

            lista_rents = []
            for r in rents:
                lista_rents.append(self._rent_to_view(r))

            return lista_rents, 200

        except Exception:
            db.session.rollback()
            logger.exception("Falha ao listar aluguéis")
            raise InternalError("Não foi possível listar os aluguéis. Tente novamente mais tarde.")

    def delete_by_id(self, rent_id: int):
        rent = db.session.get(Rent, rent_id)
        if not rent:
            raise NotFoundError(self.ALUGUEL_NAO_LOCALIZADO)
        if rent.canceled:
            raise BusinessError(self.ALUGUEL_ESTA_CANCELADO)
        rent.canceled = True
        db.session.commit()

        return {"message": self.MSG_ALUGUEL_CANCELADO}, 200

    def _rent_to_view(self, rent: Rent) -> dict:
        return RentViewSchema.model_validate(rent).model_dump(mode="json")

    def _active_rent_on_date(self, rent_date) -> bool:
        stmt = select(exists().where(and_(Rent.rent_date == rent_date, Rent.canceled == False)))
        return db.session.scalar(stmt)
