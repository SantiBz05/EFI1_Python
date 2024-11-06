from flask import Blueprint, request, jsonify
from flask_jwt_extended import get_jwt, jwt_required
from flask import Blueprint, request, jsonify
from models import Accesorios, Inventario, Fabricante, Pedido, Sucursal, Empleado, Cliente, Venta
from schemas import (
    AccesorioSchema,
    InventarioSchema,
    FabricanteSchema,
    PedidoSchema,
    SucursalSchema,
    EmpleadoSchema,
    ClienteSchema,
    VentaSchema,
)

models_list_bp = Blueprint("models_list", __name__)

@models_list_bp.route("/accesorios", methods=["GET"])
def accesorios():
    accesorios = Accesorios.query.all()
    return AccesorioSchema().dump(accesorios, many=True)

@models_list_bp.route("/inventario", methods=["GET"])
def inventario():
    inventario = Inventario.query.all()
    return InventarioSchema().dump(inventario, many=True)

@models_list_bp.route("/fabricantes", methods=["GET"])
def fabricantes():
    fabricantes = Fabricante.query.all()
    return FabricanteSchema().dump(fabricantes, many=True)

@models_list_bp.route("/pedidos", methods=["GET"])
def mopedidosdelo():
    pedidos = Pedido.query.all()
    return PedidoSchema().dump(pedidos, many=True)

@models_list_bp.route("/sucursales", methods=["GET"])
def sucursales():
    sucursales = Sucursal.query.all()
    return SucursalSchema().dump(sucursales, many=True)

@models_list_bp.route("/empleados", methods=["GET"])
def empleados():
    empleados = Empleado.query.all()
    return EmpleadoSchema().dump(empleados, many=True)

@models_list_bp.route("/clientes", methods=["GET"])
def clientes():
    clientes = Cliente.query.all()
    return ClienteSchema().dump(clientes, many=True)

@models_list_bp.route("/venta", methods=["GET"])
def venta():
    venta = Venta.query.all()
    return VentaSchema().dump(venta, many=True)
