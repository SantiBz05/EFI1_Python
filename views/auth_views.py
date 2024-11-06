from datetime import timedelta
from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, get_jwt, jwt_required
from werkzeug.security import check_password_hash, generate_password_hash
from models import Usuario
from app import db
from schemas import UsuarioSchema, MinimalUserSchema

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.authorization
    if not data or not data.username or not data.password:
        return jsonify({"Mensaje": "Falta el nombre de usuario o la contraseña"}), 401

    username = data.username
    password = data.password

    usuario = Usuario.query.filter_by(username=username).first()

    if usuario and check_password_hash(usuario.password_hash, password):
        access_token = create_access_token(
            identity=username,
            expires_delta=timedelta(minutes=30),
            additional_claims={"administrador": usuario.is_admin},
        )
        return jsonify({"Token": f"Bearer {access_token}"})

    return (
        jsonify({"Mensaje": "El usuario y la contraseña al parecer no coinciden"}),
        401,
    )


@auth_bp.route("/users", methods=["GET", "POST"])
@jwt_required()
def users():
    additional_data = get_jwt()
    administrador = additional_data.get("administrador")

    if request.method == "POST":
        if administrador:
            data = request.get_json()
            username = data.get("usuario")
            password = data.get("contrasenia")

            if Usuario.query.filter_by(username=username).first() is not None:
                return jsonify({"Mensaje": "El usuario ya existe"}), 400

            password_hash = generate_password_hash(
                password=password, method="pbkdf2", salt_length=8
            )

            try:
                nuevo_usuario = Usuario(
                    username=username,
                    password_hash=password_hash,
                    is_admin=False,
                )
                db.session.add(nuevo_usuario)
                db.session.commit()
                return jsonify({"Usuario Creado": username}), 201
            except Exception as e:
                return (
                    jsonify(
                        {
                            "Mensaje": "Fallo la creación del nuevo usuario",
                            "Error": str(e),
                        }
                    ),
                    500,
                )
        else:
            return (
                jsonify({"Mensaje": "Ud no está habilitado para crear un usuario."}),
                403,
            )

    usuarios = Usuario.query.all()
    if administrador:
        return UsuarioSchema(many=True).dump(usuarios)
    else:
        return MinimalUserSchema(many=True).dump(usuarios)
