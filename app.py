from flask import Flask
from extensions import db, migrate

def create_app():
    app = Flask(__name__)
    app.config.from_pyfile('config.py')

    db.init_app(app)
    migrate.init_app(app, db)

    # para migration
    from models.rent import Rent

    from schemas.rent_schema import RentSchema
    from services.rent_service import RentService

    service = RentService()

    @app.route("/rent", methods=["POST",])
    def add_rent(form: RentSchema):
        return service.add_rent(form)

    return app


if __name__ == '__main__':
    create_app().run(debug=True)
