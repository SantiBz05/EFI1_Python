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

    # Crear un nuevo usuario
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

    # Obtener todos los usuarios
    usuarios = Usuario.query.all()
    if administrador:
        return UsuarioSchema(many=True).dump(usuarios)
    else:
        return MinimalUserSchema(many=True).dump(usuarios)


@auth_bp.route("/users/<int:user_id>", methods=["PUT", "DELETE"])
@jwt_required()
def modify_user(user_id):
    additional_data = get_jwt()
    administrador = additional_data.get("administrador")

    # Verificar si el usuario tiene permisos de administrador
    if not administrador:
        return jsonify({"Mensaje": "Ud no está habilitado para modificar o eliminar un usuario."}), 403

    usuario = Usuario.query.get(user_id)

    if not usuario:
        return jsonify({"Mensaje": "Usuario no encontrado"}), 404

    # Actualizar información del usuario (método PUT)
    if request.method == "PUT":
        data = request.get_json()
        username = data.get("usuario")
        password = data.get("contrasenia")
        is_admin = data.get("is_admin", usuario.is_admin)

        # Si se proporciona un nuevo nombre de usuario, actualízalo
        if username:
            usuario.username = username

        # Si se proporciona una nueva contraseña, actualízala
        if password:
            usuario.password_hash = generate_password_hash(password, method="pbkdf2", salt_length=8)

        # Actualizar el estado de administrador si se especifica
        usuario.is_admin = is_admin

        try:
            db.session.commit()
            return jsonify({"Mensaje": "Usuario actualizado exitosamente"}), 200
        except Exception as e:
            return jsonify({"Mensaje": "Error al actualizar el usuario", "Error": str(e)}), 500

    # Eliminar usuario (método DELETE)
    elif request.method == "DELETE":
        try:
            db.session.delete(usuario)
            db.session.commit()
            return jsonify({"Mensaje": "Usuario eliminado exitosamente"}), 200
        except Exception as e:
            return jsonify({"Mensaje": "Error al eliminar el usuario", "Error": str(e)}), 500
