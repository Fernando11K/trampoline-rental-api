from flask import Flask, redirect, Response
from flask_cors import CORS
from flask_openapi3 import OpenAPI, Info, Tag

from core.error_handlers import register_error_handlers
from extensions import db, migrate
from schemas.error_schema import ErrorSchema
from schemas.rent_path import RentIdPath
from schemas.rent_schema import RentViewSchema


def create_app():
    info = Info(title="Trampoline Rental API", version="0.0.1")
    app = OpenAPI(__name__, info=info)
    CORS(app)

    home_tag = Tag(name="Documentação", description="Seleção de documentação: Swagger, Redoc ou RapiDoc")
    rent_tag = Tag(name="Rent", description="Registro, consulta, alteração e cancelamento de aluguéis de trampolins")

    app.config.from_pyfile('config.py')

    db.init_app(app)
    migrate.init_app(app, db)

    # para migration
    from models.rent import Rent

    from schemas.rent_schema import RentSchema
    from services.rent_service import RentService

    service = RentService()

    @app.get('/', tags=[home_tag])
    def home():
        """
        Redireciona a raiz para a documentação interativa da API (OpenAPI).
        """
        return redirect('/openapi')

    @app.post("/rent", tags=[rent_tag], responses={"201": RentViewSchema, "409": ErrorSchema})
    def add_rent(form: RentSchema):
        """
        Resgistra um aluguel
        """
        return service.add_rent(form)

    @app.get("/rent", tags=[rent_tag])
    def get_all():
        """
        Retona todos os aluguéis
        """
        return service.get_all()

    @app.get("/rent/<int:rent_id>", tags=[rent_tag])
    def get_by_id(path: RentIdPath):
        """
          Consulta o aluguel pelo id
          """
        return service.get_by_id(path.rent_id)

    register_error_handlers(app)

    return app


if __name__ == '__main__':
    create_app().run(debug=True)
