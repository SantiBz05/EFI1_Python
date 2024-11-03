from flask import Blueprint, request, jsonify
from datetime import timedelta

from flask_jwt_extended import (
    JWTManager,
    get_jwt,
    get_jwt_identity,
    create_access_token,
    jwt_required,
)
from werkzeug.security import (
    generate_password_hash,
    check_password_hash
)

from models import Usuario
from app import db
from schemas import UsuarioSchema, MinimalUserSchema

auth_bp = Blueprint('auth', __name__)

@auth_bp.route("/users", methods=['POST', 'GET'])
@jwt_required()
def user():
    print(get_jwt_identity())
    print(get_jwt())
    if request.method == 'POST':
        additional_data = get_jwt()
        administrador = additional_data.get('adminsitrador')
        if administrador is True:       
            data = request.get_json()
            username = data.get('nombre_usuario')
            password = data.get('contraseña')
            
            password_hasheada = generate_password_hash(
                password=password,
                method='pbkdf2',
                salt_length=8,
            )
            print(password_hasheada)

            try:
                nuevo_usuario = Usuario(
                    username=username,
                    password_hash=password_hasheada,
                )
                db.session.add(nuevo_usuario)
                db.session.commit()

                return jsonify({"Usuario Creado" : username}), 201
            except:
                return jsonify({"Error" : "Bien ahi crack, segundo error de tu vida, el primero? Nacer."})
        return jsonify(Mensaje = "Ud no esta habilitado para crear un usario." )
    if administrador is True:
        usuarios = Usuario.query.all()  
        return UsuarioSchema().dump(usuarios, many=True)
    else:
        usuarios = Usuario.query.all()
        return MinimalUserSchema().dump(usuarios, many=True)

@auth_bp.route("/login", methods=['POST'])
def login():
    data = request.authorization 
    username = data.username
    password = data.password

    usuario = Usuario.query.filter_by(username=username).first()

    if usuario and check_password_hash(pwhash=usuario.password_hash, password=password):

        access_token = create_access_token(
            identity = username,
            expires_delta = timedelta(minutes=3),
            additional_claims = dict( 
                administrador = usuario.is_admin
            )
        )

        return jsonify({"Mensaje": f"Token: {access_token}"})
    
    return jsonify({"Mensaje": "NO MATCH"})