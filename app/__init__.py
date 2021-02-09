from . import cardf
from . import auth

from app.server import app

# registering user and card blueprints
app.register_blueprint(cardf.card_bp)
app.register_blueprint(auth.user_bp)

if __name__ == "__main__":
    app.run(debug=True)
