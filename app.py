from flask import Flask, redirect, Response
from flask_cors import CORS
from flask_openapi3 import OpenAPI, Info, Tag

from extensions import db, migrate


def create_app():
    info = Info(title="Trampoline Rental API", version="0.0.1")
    app = OpenAPI(__name__, info=info)
    CORS(app)

    home_tag = Tag(name="Documentação", description="Seleção de documentação: Swagger, Redoc ou RapiDoc")
    rent_tag = Tag(name="Rent", description="Registro e gestão de aluguéis de trampolins.")

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

    @app.post("/rent", tags=[rent_tag])
    def add_rent(payload: RentSchema):
        return service.add_rent(payload)

    return app


if __name__ == '__main__':
    create_app().run(debug=True)
