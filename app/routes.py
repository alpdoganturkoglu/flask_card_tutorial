from app import cardf
from app import auth


def init_routes(app):
    # registering user and card blueprints
    app.register_blueprint(cardf.card_bp)
    app.register_blueprint(auth.user_bp)
