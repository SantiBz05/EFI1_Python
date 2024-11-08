from flask import Blueprint, request, jsonify
from flask_jwt_extended import get_jwt, jwt_required
from app import db
from models import Marca, Categoria, Equipo, Caracteristicas, Proveedor, Modelo
from schemas import (
    ModeloSchema,
    CategoriaSchema,
    MarcaSchema,
    EquipoSchema,
    CaracteristicasSchema,
    ProveedorSchema,
    MinimalEquipoSchema,
)

equipos_bp = Blueprint("equipos", __name__)

# Ruta para obtener todos los modelos
@equipos_bp.route("/modelos", methods=["GET"])
def modelo():
    modelos = Modelo.query.all()
    return ModeloSchema().dump(modelos, many=True)

# Ruta para obtener todas las marcas
@equipos_bp.route("/marcas", methods=["GET"])
def marcas():
    marcas = Marca.query.all()
    return MarcaSchema().dump(marcas, many=True)

# Ruta para obtener todas las características
@equipos_bp.route("/caracteristicas", methods=["GET"])
def caracteristicas():
    caracteristicas = Caracteristicas.query.all()
    return CaracteristicasSchema().dump(caracteristicas, many=True)

# Ruta para obtener todas las categorías
@equipos_bp.route("/categorias", methods=["GET"])
def categorias():
    categorias = Categoria.query.all()
    return CategoriaSchema().dump(categorias, many=True)

# Ruta para obtener todos los proveedores
@equipos_bp.route("/proveedores", methods=["GET"])
def proveedores():
    proveedores = Proveedor.query.all()
    return ProveedorSchema().dump(proveedores, many=True)

# Ruta para manejar equipos (GET, POST, PUT, DELETE)
@equipos_bp.route("/equipos", methods=["GET", "POST"])
@jwt_required()
def equipos():
    additional_data = get_jwt()
    administrador = additional_data.get("administrador")

    # Método POST: Crear nuevo equipo
    if request.method == "POST":
        if administrador:
            data = request.get_json()
            try:
                nuevo_equipo = Equipo(
                    precio=data.get("precio"),
                    modelo_id=data.get("modelo_id"),
                    marca_id=data.get("marca_id"),
                    caracteristicas_id=data.get("caracteristicas_id"),
                    categoria_id=data.get("categoria_id"),
                    proveedor_id=data.get("proveedor_id"),
                    activo=data.get("activo"),
                )
                db.session.add(nuevo_equipo)
                db.session.commit()
                return EquipoSchema().dump(nuevo_equipo), 201
            except Exception as e:
                return jsonify({"Mensaje": "Fallo la creación del nuevo equipo"}), 500
        else:
            return (
                jsonify({"Mensaje": "Ud no está habilitado para crear un equipo."}),
                403,
            )

    # Método GET: Obtener lista de equipos
    equipos = Equipo.query.all()
    if administrador:
        return EquipoSchema().dump(equipos, many=True)
    else:
        return MinimalEquipoSchema().dump(equipos, many=True)


# Ruta para manejar un equipo específico (PUT, DELETE) por id
@equipos_bp.route("/equipos/<int:id>", methods=["PUT", "DELETE"])
@jwt_required()
def equipo(id):
    additional_data = get_jwt()
    administrador = additional_data.get("administrador")

    # Método PUT: Editar equipo existente
    if request.method == "PUT":
        if administrador:
            equipo = Equipo.query.get(id)

            if not equipo:
                return jsonify({"Mensaje": "Equipo no encontrado"}), 404

            data = request.get_json()
            try:
                # Actualizar los campos del equipo
                equipo.precio = data.get("precio", equipo.precio)
                equipo.modelo_id = data.get("modelo_id", equipo.modelo_id)
                equipo.marca_id = data.get("marca_id", equipo.marca_id)
                equipo.caracteristicas_id = data.get("caracteristicas_id", equipo.caracteristicas_id)
                equipo.categoria_id = data.get("categoria_id", equipo.categoria_id)
                equipo.proveedor_id = data.get("proveedor_id", equipo.proveedor_id)
                equipo.activo = data.get("activo", equipo.activo)

                db.session.commit()
                return EquipoSchema().dump(equipo), 200
            except Exception as e:
                return jsonify({"Mensaje": "Fallo la actualización del equipo"}), 500
        else:
            return jsonify({"Mensaje": "Ud no está habilitado para editar un equipo."}), 403

    # Método DELETE: Eliminar equipo existente
    if request.method == "DELETE":
        if administrador:
            equipo = Equipo.query.get(id)

            if not equipo:
                return jsonify({"Mensaje": "Equipo no encontrado"}), 404

            try:
                db.session.delete(equipo)
                db.session.commit()
                return jsonify({"Mensaje": "Equipo eliminado con éxito"}), 200
            except Exception as e:
                return jsonify({"Mensaje": "Fallo al eliminar el equipo"}), 500
        else:
            return jsonify({"Mensaje": "Ud no está habilitado para eliminar un equipo."}), 403
