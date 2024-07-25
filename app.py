from flask import Flask, render_template, redirect, request, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost/tienda_celulares_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)

from models import Marca, Categoria, Proveedor, Stock, Accesorios, Caracteristicas, Fabricante, Modelo, Equipo 

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/list_marca", methods=['POST', 'GET'])
def marcas():
    marcas = Marca.query.all()

    if request.method == 'POST':
        nombre = request.form['nombre']
        nueva_marca = Marca(
            nombre=nombre,
        )
        db.session.add(nueva_marca)
        db.session.commit()
        return redirect(url_for('marcas'))

    return render_template('list_marca.html', marcas=marcas)

@app.route("/list_categorias", methods=['POST', 'GET'])
def categorias():
    categorias = Categoria.query.all()

    if request.method == 'POST':
        nombre = request.form['nombre']
        nueva_categoria = Categoria(
            nombre=nombre,
        )
        db.session.add(nueva_categoria)
        db.session.commit()
        return redirect(url_for('categorias'))

    return render_template('list_categorias.html', categorias=categorias)

@app.route("/list_fabricantes", methods=['POST', 'GET'])
def fabricantes():
    fabricantes = Fabricante.query.all()

    if request.method == 'POST':
        nombre = request.form['nombre']
        origen = request.form['origen']
        
        nuevoFabricante = Fabricante(
            nombre=nombre,
            origen=origen
        )
        db.session.add(nuevoFabricante)
        db.session.commit()
        return redirect(url_for('fabricantes'))

    return render_template('list_fabricantes.html', fabricantes=fabricantes)

@app.route("/list_modelos", methods = ['POST', 'GET'])
def modelos():
    modelos = Modelo.query.all()
    fabricantes = Fabricante.query.all()
    categorias = Categoria.query.all()
    
    if request.method == 'POST':
        modelo = request.form['modelo']
        anio = request.form['anioLanzamiento']
        sistOp = request.form['sistemaOperativo']
        fabricante = request.form['fabricante']
        categoria = request.form['categoria']
        nuevoModelo = Modelo(
            modelo=modelo,
            anioLanzamiento=anio,
            sistemaOperativo=sistOp,
            fabricante_id=fabricante,
            categoria_id=categoria
        )
        db.session.add(nuevoModelo)
        db.session.commit()
        return redirect(url_for('modelos'))

    return render_template(
        'list_modelos.html',
        modelos=modelos,
        fabricantes=fabricantes,
        categorias=categorias,
    )

@app.route("/list_accesorios", methods=['POST', 'GET'])
def accesorios():
    accesorios = Accesorios.query.all()
    stocks = Stock.query.all()

    if request.method == 'POST':
        nombre = request.form['nombre']
        descripcion = request.form['descripcion']
        stock = request.form['stock']
        
        nuevoAccesorio = Accesorios(
            nombre=nombre,
            descripcion=descripcion,
            stock_id=stock
        )
        db.session.add(nuevoAccesorio)
        db.session.commit()
        return redirect(url_for('accesorios'))

    return render_template('list_accesorios.html', accesorios=accesorios, stocks=stocks)

@app.route("/list_proveedores", methods=['POST', 'GET'])
def proveedores():
    proveedores = Proveedor.query.all()

    if request.method == 'POST':
        nombre = request.form['nombre']
        contacto = request.form['contacto']
        nuevoProveedor = Proveedor(
            nombre=nombre,
            contacto=contacto
        )
        db.session.add(nuevoProveedor)
        db.session.commit()
        return redirect(url_for('proveedores'))

    return render_template('list_proveedores.html', proveedores=proveedores)

@app.route("/list_Stock", methods=['POST', 'GET'])
def añadirStock():
    añadirStock = Stock.query.all()

    if request.method == 'POST':
        cantDisp = request.form['cantDisp']
        uniAlm = request.form['ubiAlm']
        nuevoStock = Stock(
            cantidadDisponible=cantDisp,
            ubicacionAlmacen=uniAlm
        )
        db.session.add(nuevoStock)
        db.session.commit()
        return redirect(url_for('añadirStock'))

    return render_template('list_Stock.html', añadirStock=añadirStock)

@app.route("/list_caracteristicas", methods=['POST', 'GET'])
def añadirCaracteristica():
    añadirCaracteristica = Caracteristicas.query.all()

    if request.method == 'POST':
        nombre = request.form['nombre']
        descripcion = request.form['descripcion']  

        nuevaCaracteristica = Caracteristicas(
            nombre=nombre,
            descripcion=descripcion,
        )
        db.session.add(nuevaCaracteristica)
        db.session.commit()
        return redirect(url_for('añadirCaracteristica'))  

    return render_template('list_caracteristicas.html', añadirCaracteristica=añadirCaracteristica)

@app.route("/list_equipos", methods = ['POST', 'GET'])
def equipos():
    equipos = Equipo.query.all()
    modelos = Modelo.query.all()
    marcas = Marca.query.all()
    caracteristicas = Caracteristicas.query.all()
    proveedores = Proveedor.query.all()
    stocks = Stock.query.all()
    categorias = Categoria.query.all()
    
    if request.method == 'POST':
        modelo = request.form['modelo']
        marca = request.form['marca']
        categoria = request.form['categoria']
        precio = request.form['precio']
        caracteristicas = request.form['caracteristicas']
        proveedor = request.form['proveedor']
        stock = request.form['stock']
        nuevoEquipo = Equipo(
            modelo_id=modelo, 
            marca_id=marca,
            categoria_id=categoria,
            precio=precio,
            caracteristicas_id=caracteristicas,
            proveedor_id=proveedor,
            stock_id=stock,
        )
        db.session.add(nuevoEquipo)
        db.session.commit()
        return redirect(url_for('equipos'))

    return render_template(
        'list_equipos.html',
        modelos=modelos,
        marcas=marcas,
        caracteristicas=caracteristicas,
        proveedores=proveedores,
        stocks=stocks,
        categorias=categorias,
        equipos=equipos,
    )