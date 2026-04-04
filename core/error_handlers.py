from datetime import datetime

from flask import jsonify
from http import HTTPStatus

from core.exceptions import BusinessError


def register_error_handlers(app):
    @app.errorhandler(BusinessError)
    def handle_business_error(e: BusinessError):
        status = e.status.value
        body = {
            "status": status,
            "error": e.status.name,
            "message": e.message,
            "timestamp": datetime.now().isoformat(),
        }
        return jsonify(body), status

    @app.errorhandler(Exception)
    def handle_exception(e):
        return jsonify({
            "status": HTTPStatus.INTERNAL_SERVER_ERROR.value,
            "error": HTTPStatus.INTERNAL_SERVER_ERROR.name,
            "message": "Ocorreu um erro inesperado. Tente novamente.",
            "timestamp": datetime.now().isoformat(),
        }), HTTPStatus.INTERNAL_SERVER_ERROR.value
