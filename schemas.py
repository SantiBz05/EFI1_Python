from app import ma
from models import Usuario, Marca, Categoria, Equipo, Caracteristicas, Proveedor, Modelo, Accesorios, Inventario, Fabricante, Pedido, Sucursal, Empleado, Cliente, Venta
from marshmallow import validates, ValidationError


class UsuarioSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Usuario

    id = ma.auto_field()
    username = ma.auto_field()
    password_hash = ma.auto_field()
    is_admin = ma.auto_field()


class MinimalUserSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Usuario

    username = ma.auto_field()


class MarcaSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Marca

    nombre = ma.auto_field()


class CategoriaSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Categoria

    nombre = ma.auto_field()


class ModeloSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Modelo

    modelo = ma.auto_field()
    anioLanzamiento = ma.auto_field()
    sistemaOperativo = ma.auto_field()


class ProveedorSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Proveedor

    nombre = ma.auto_field
    contacto = ma.auto_field()


class CaracteristicasSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Caracteristicas

    nombre = ma.auto_field()
    descripcion = ma.auto_field()


class EquipoSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Equipo

    id = ma.auto_field()
    precio = ma.auto_field()
    activo = ma.auto_field()

    modelo_id = ma.auto_field()
    marca_id = ma.auto_field()
    categoria_id = ma.auto_field()
    caracteristicas_id = ma.auto_field()
    proveedor_id = ma.auto_field()

    @validates("precio")
    def validate_precio(self, value):
        if value <= 0:
            raise ValidationError("El precio no puede ser menor o igual a cero.")


class MinimalEquipoSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Equipo

    id = ma.auto_field()
    modelo_id = ma.auto_field()
    marca_id = ma.auto_field()
    precio = ma.auto_field()
    activo = ma.auto_field()

class AccesorioSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Accesorios

    nombre = ma.auto_field()
    precio = ma.auto_field()
    
class InventarioSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Inventario

    tipo = ma.auto_field()
    producto = ma.auto_field()
    tipo = ma.auto_field()
    cantidadDisponible = ma.auto_field()


class FabricanteSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Fabricante

    nombre = ma.auto_field()
    origen = ma.auto_field()

class PedidoSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Pedido

    fecha = ma.auto_field()
    total = ma.auto_field()

class SucursalSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Sucursal

    nombre = ma.auto_field()
    direccion = ma.auto_field()
    telefono = ma.auto_field()

class EmpleadoSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Empleado

    nombre = ma.auto_field()
    puesto = ma.auto_field()

class ClienteSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Cliente

    nombre = ma.auto_field()
    telefono = ma.auto_field()
    email = ma.auto_field()

class VentaSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Venta

    fecha = ma.auto_field()
    producto = ma.auto_field()
    cantidad = ma.auto_field()
    total = ma.auto_field()

