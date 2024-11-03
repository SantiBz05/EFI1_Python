from .auth_views import auth_bp
from .equipos import equipos_bp

def register_bp(app):
    app.register_blueprint(auth_bp)
    app.register_blueprint(equipos_bp)