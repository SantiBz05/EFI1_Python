from .auth_views import auth_bp
from .equipos import equipos_bp
from .models_list import models_list_bp

def register_bp(app):
    app.register_blueprint(auth_bp)
    app.register_blueprint(equipos_bp)
    app.register_blueprint(models_list_bp)

