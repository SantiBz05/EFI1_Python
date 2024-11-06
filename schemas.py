from app import ma
from models import Usuario, Marca, Categoria, Equipo, Caracteristicas, Proveedor, Modelo
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


class ProveedorSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Proveedor

    nombre = ma.auto_field()


class CaracteristicasSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Caracteristicas

    nombre = ma.auto_field()


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
