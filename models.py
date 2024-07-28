from app import db

class Marca(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), nullable=False)

    fabricante_id = db.Column(db.Integer, db.ForeignKey('fabricante.id'), nullable=False)
    fabricante = db.relationship('Fabricante', backref=db.backref('modelos', lazy=True))

    def __str__(self) -> str:
        return self.nombre
    

class Categoria(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), nullable=False)

    def __str__(self) -> str:
        return self.nombre
    

class Proveedor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), nullable=False)
    contacto = db.Column(db.String(50), nullable=False)

    def __str__(self) -> str:
        return self.nombre
    

class Inventario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tipo = db.Column(db.String(50))
    producto = db.Column(db.String(100)) 
    cantidadDisponible = db.Column(db.Integer)
    ubicacionAlmacen = db.Column(db.String(100))

    def __str__(self) -> str:
        return self.producto


class Accesorios(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), nullable=False)
    descripcion = db.Column(db.String(1000), nullable=False)
    precio = db.Column(db.Integer, nullable=False)

    def __str__(self) -> str:
        return self.nombre

    
class Caracteristicas(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), nullable=False)
    descripcion = db.Column(db.String(1000), nullable=False)  

    def __str__(self) -> str:
        return self.nombre
  

class Fabricante(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), nullable=False)
    origen = db.Column(db.String(50), nullable=False)

    def __str__(self) -> str:
        return self.nombre    
    

class Modelo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    modelo = db.Column(db.String(50), nullable=False)
    anioLanzamiento = db.Column(db.Integer, nullable=False)
    sistemaOperativo = db.Column(db.String(50), nullable=False)


class Equipo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    precio = db.Column(db.Integer, nullable=False)

    modelo_id = db.Column(db.Integer, db.ForeignKey('modelo.id'), nullable=False)
    marca_id = db.Column(db.Integer, db.ForeignKey('marca.id'), nullable=False)  
    caracteristicas_id = db.Column(db.Integer, db.ForeignKey('caracteristicas.id'), nullable=False)
    proveedor_id = db.Column(db.Integer, db.ForeignKey('proveedor.id'), nullable=False)
    categoria_id = db.Column(db.Integer, db.ForeignKey('categoria.id'), nullable=False)

    modelo = db.relationship('Modelo', backref=db.backref('equipos', lazy=True))
    marca = db.relationship('Marca', backref=db.backref('equipos', lazy=True))
    caracteristicas = db.relationship('Caracteristicas', backref=db.backref('equipos', lazy=True))
    proveedor = db.relationship('Proveedor', backref=db.backref('equipos', lazy=True))
    categoria = db.relationship('Categoria', backref=db.backref('equipos', lazy=True))

    @property
    def nombre(self):
        return f"{self.marca.nombre} {self.modelo.modelo}"
    
class Pedido(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fecha = db.Column(db.Date, nullable=False)
    total = db.Column(db.Integer, nullable=False)

    proveedor_id = db.Column(db.Integer, db.ForeignKey('proveedor.id'), nullable=False)
    proveedor = db.relationship('Proveedor', backref=db.backref('pedidos', lazy=True))

    def __str__(self) -> str:
        return self.fecha    

class Sucursal(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), nullable=False)
    direccion = db.Column(db.String(50), nullable=False)
    telefono = db.Column(db.String(50), nullable=False)

    def __str__(self) -> str:
        return self.nombre    

class Empleado(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), nullable=False)
    puesto = db.Column(db.String(50), nullable=False)

    sucursal_id = db.Column(db.Integer, db.ForeignKey('sucursal.id'), nullable=False)
    sucursal = db.relationship('Sucursal', backref=db.backref('empleados', lazy=True))

    def __str__(self) -> str:
        return self.nombre    

class Cliente(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), nullable=False)
    direccion = db.Column(db.String(50), nullable=False)
    telefono = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    fechaRegistro = db.Column(db.Date, nullable=False)

    def __str__(self) -> str:
        return self.nombre    
    
class Venta(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fecha = db.Column(db.Date, nullable=False)
    cantidad = db.Column(db.Integer, nullable=False)
    total = db.Column(db.Integer, nullable=False)
    tipo = db.Column(db.String(50))
    producto = db.Column(db.String(100)) 

    cliente_id = db.Column(db.Integer, db.ForeignKey('cliente.id'), nullable=False)
    cliente = db.relationship('Cliente', backref=db.backref('ventas', lazy=True))

    def __str__(self) -> str:
        return self.fecha    

