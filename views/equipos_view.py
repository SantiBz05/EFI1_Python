from flask import Blueprint, request, jsonify, make_response
from models import Marca, Categoria, Equipo, Caracteristicas, Proveedor, Modelo
from schemas import CategoriaSchema, MarcaSchema, EquipoSchema

equipos_bp = Blueprint('equipos', __name__)

@equipos_bp.route('/marcas', methods=['GET'])
def marcas():
    marcas = Marca.query.all()
    return MarcaSchema().dump(marcas, many=True)

@equipos_bp.route('/categoria', methods=['GET'])
def categorias():
    categoria = Categoria.query.all()
    return CategoriaSchema().dump(categoria, many=True)

@equipos_bp.route('/equipos', methods=['GET', 'POST'])
def equipos():
    if request.method == 'POST':
        data = request.get_json()
        errors = EquipoSchema().validate(data)  
        if errors:
            return make_response(jsonify(errors))
        return{}
        
    equipos = Equipo.query.all()
    return EquipoSchema().dump(equipos, many=True)