from app import db

class Marca(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), nullable=False)

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
    
class Stock(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cantidadDisponible = db.Column(db.Integer, nullable=False)
    ubicacionAlmacen = db.Column(db.String(10), nullable=False)

    def __str__(self) -> str:
        return str(self.cantidadDisponible)

class Accesorios(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), nullable=False)
    descripcion = db.Column(db.String(1000), nullable=False)
    stock_id = db.Column(db.Integer, db.ForeignKey('stock.id'), nullable=False)
    stock = db.relationship('Stock', backref=db.backref('accesorios', lazy=True))

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
    anioLanzamiento = db.Column(db.Integer)
    sistemaOperativo = db.Column(db.String(50), nullable=False)
    categoria = db.Column(db.String(50), nullable=False)

    fabricante_id = db.Column(db.Integer, db.ForeignKey('fabricante.id'), nullable=False)
    fabricante = db.relationship('Fabricante', backref=db.backref('modelos', lazy=True))

    categoria_id = db.Column(db.Integer, db.ForeignKey('categoria.id'), nullable=False)
    categoria = db.relationship('Categoria', backref=db.backref('modelos', lazy=True))


class Equipo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    categoria = db.Column(db.String(50), nullable=False)
    precio = db.Column(db.Integer)

    modelo_id = db.Column(db.Integer, db.ForeignKey('modelo.id'), nullable=False)
    marca_id = db.Column(db.Integer, db.ForeignKey('marca.id'), nullable=False)  
    caracteristicas_id = db.Column(db.Integer, db.ForeignKey('caracteristicas.id'), nullable=False)
    proveedor_id = db.Column(db.Integer, db.ForeignKey('proveedor.id'), nullable=False)
    stock_id = db.Column(db.Integer, db.ForeignKey('stock.id'), nullable=False)
    categoria_id = db.Column(db.Integer, db.ForeignKey('categoria.id'), nullable=False)

    modelo = db.relationship('Modelo', backref=db.backref('equipos', lazy=True))
    marca = db.relationship('Marca', backref=db.backref('equipos', lazy=True))
    caracteristicas = db.relationship('Caracteristicas', backref=db.backref('equipos', lazy=True))
    proveedor = db.relationship('Proveedor', backref=db.backref('equipos', lazy=True))
    stock = db.relationship('Stock', backref=db.backref('equipos', lazy=True))
    categoria = db.relationship('Categoria', backref=db.backref('equipos', lazy=True))

