import bcrypt
import os
from datetime import timedelta

from flask import Flask, render_template, redirect, request, url_for, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
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

from dotenv import load_dotenv

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get ('SQLALCHEMY_DATABASE_URI')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')

db = SQLAlchemy(app)
migrate = Migrate(app, db)
jwt = JWTManager(app)

from models import Usuario, Marca, Categoria, Proveedor, Inventario, Accesorios, Caracteristicas, Fabricante, Modelo, Equipo, Pedido, Cliente, Empleado, Sucursal, Venta
from services.fabricante_service import FabricanteService
from repositories.fabricante_repository import FabricanteRepository

load_dotenv()

@app.route("/users", methods=['POST', 'GET'])
@jwt_required()
def user():
    if request.method == 'POST':
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
    return jsonify({"Usuario Creado" : "ACA IRIA EL LISTADO"})

@app.route("/login", methods=['POST'])
def login():
    data = request.authorization 
    username = data.username
    password = data.password

    usuario = Usuario.query.filter_by(username=username).first()

    if usuario and check_password_hash(pwhash=usuario.password_hash, password=password):

        access_token = create_access_token(
            identity = username,
            expires_delta = timedelta(minutes=3) 
        )

        return jsonify({"Mensaje": f"Token: {access_token}"})
    
    return jsonify({"Mensaje": "NO MATCH"})
    
@app.route("/")
def index():
    return render_template('index.html')

@app.route("/list_marca", methods=['POST', 'GET'])
def marcas():
    marcas = Marca.query.filter_by(activo=True).all()
    fabricantes = Fabricante.query.all()

    if request.method == 'POST':
        nombre = request.form['nombre']
        fabricante = request.form['fabricante']
        nueva_marca = Marca(
            nombre=nombre,
            fabricante_id=fabricante,
        )
        db.session.add(nueva_marca)
        db.session.commit()
        return redirect(url_for('marcas'))

    return render_template(
        'list_marca.html', 
        marcas=marcas,
        fabricantes=fabricantes,
        )

@app.route("/list_marcas_inactivas", methods=['GET'])
def marcas_inactivas():
    marcas_inactivas = Marca.query.filter_by(activo=False).all()
    return render_template('list_marcas_inactivas.html', marcas=marcas_inactivas)

@app.route("/restaurar_marca/<int:id>", methods=['POST'])
def restaurar_marca(id):
    marca = Marca.query.get_or_404(id)
    marca.activo = True
    db.session.commit()
    return redirect(url_for('marcas'))

@app.route("/marca/<id>/editar", methods=['GET', 'POST'])
def marca_editar(id):
    marca = Marca.query.get_or_404(id)
    fabricantes = Fabricante.query.all() 

    if request.method == 'POST':
        marca.nombre = request.form['nombre']
        marca.fabricante_id = request.form['fabricante']  
        db.session.commit()
        return redirect(url_for('marcas'))

    return render_template(
        "editar_marca.html",
        marca=marca,
        fabricantes=fabricantes
    )

@app.route("/eliminar_marca/<int:id>", methods=['POST'])
def eliminar_marca(id):
    marca = Marca.query.get_or_404(id)
    marca.activo = False
    db.session.commit()
    return redirect(url_for('marcas'))

@app.route("/marcas/fabricante/<int:id>")
def marcas_by_fabricante(id):
    marcas = Marca.query.filter_by(fabricante_id=id).all()
    fabricante = Fabricante.query.get(id)

    return render_template(
        "marcas_by_fabricante.html",
        marcas=marcas,
        fabricante=fabricante.nombre,
    )

@app.route("/list_categorias", methods=['POST', 'GET'])
def categorias():
    categorias = Categoria.query.filter_by(activo=True).all()

    if request.method == 'POST':
        nombre = request.form['nombre']
        nueva_categoria = Categoria(
            nombre=nombre,
        )
        db.session.add(nueva_categoria)
        db.session.commit()
        return redirect(url_for('categorias'))

    return render_template('list_categorias.html', categorias=categorias)

@app.route("/list_categorias_inactivas", methods=['GET'])
def categorias_inactivas():
    categorias_inactivas = Categoria.query.filter_by(activo=False).all()
    return render_template('list_categorias_inactivas.html', categorias=categorias_inactivas)

@app.route("/restaurar_categoria/<int:id>", methods=['POST'])
def restaurar_categoria(id):
    categoria = Categoria.query.get_or_404(id)
    categoria.activo = True
    db.session.commit()
    return redirect(url_for('categorias'))

@app.route("/eliminar_categoria/<int:id>", methods=['POST'])
def eliminar_categoria(id):
    categoria = Categoria.query.get_or_404(id)
    categoria.activo = False
    db.session.commit()
    return redirect(url_for('categorias'))

@app.route("/categoria/<id>/editar", methods=['GET', 'POST'])
def categoria_editar(id):
    categoria = Categoria.query.get_or_404(id)

    if request.method == 'POST':
        categoria.nombre = request.form['nombre']
        db.session.commit()
        return redirect(url_for('categorias'))

    return render_template(
        "editar_categoria.html",
        categoria=categoria
    )

@app.route("/list_fabricantes", methods=['POST', 'GET'])
def fabricantes():
    
    services = FabricanteService(FabricanteRepository)
    fabricantes = services.get_all()

    if request.method == 'POST':
        nombre = request.form['nombre']
        origen = request.form['origen']
        
        services.create(nombre=nombre, origen=origen)
        return redirect(url_for('fabricantes'))

    return render_template('list_fabricantes.html', fabricantes=fabricantes)

@app.route("/list_fabricantes_inactivos", methods=['GET'])
def fabricantes_inactivos():
    fabricantes_inactivos = Fabricante.query.filter_by(activo=False).all()
    return render_template('list_fabricantes_inactivos.html', fabricantes=fabricantes_inactivos)

@app.route("/restaurar_fabricante/<int:id>", methods=['POST'])
def restaurar_fabricante(id):
    fabricante = Fabricante.query.get_or_404(id)
    fabricante.activo = True
    db.session.commit()
    return redirect(url_for('fabricantes'))

@app.route("/eliminar_fabricante/<int:id>", methods=['POST'])
def eliminar_fabricante(id):
    fabricante = Fabricante.query.get_or_404(id)
    fabricante.activo = False
    db.session.commit()
    return redirect(url_for('fabricantes'))

@app.route("/fabricante/<id>/editar", methods=['GET', 'POST'])
def fabricante_editar(id):
    fabricante = Fabricante.query.get_or_404(id)

    if request.method == 'POST':
        fabricante.nombre = request.form['nombre']
        fabricante.origen = request.form['origen']
        db.session.commit()
        return redirect(url_for('fabricantes'))

    return render_template(
        "editar_fabricante.html",
        fabricante=fabricante
    )

@app.route("/list_modelos", methods = ['POST', 'GET'])
def modelos():
    modelos = Modelo.query.filter_by(activo=True).all()
    
    if request.method == 'POST':
        modelo = request.form['modelo']
        anio = request.form['anioLanzamiento']
        sistOp = request.form['sistemaOperativo']
        nuevoModelo = Modelo(
            modelo=modelo,
            anioLanzamiento=anio,
            sistemaOperativo=sistOp,
        )
        db.session.add(nuevoModelo)
        db.session.commit()
        return redirect(url_for('modelos'))

    return render_template(
        'list_modelos.html',
        modelos=modelos,
    )

@app.route("/list_modelos_inactivos", methods=['GET'])
def modelos_inactivos():
    modelos_inactivos = Modelo.query.filter_by(activo=False).all()
    return render_template('list_modelos_inactivos.html', modelos=modelos_inactivos)

@app.route("/restaurar_modelo/<int:id>", methods=['POST'])
def restaurar_modelo(id):
    modelo = Modelo.query.get_or_404(id)
    modelo.activo = True
    db.session.commit()
    return redirect(url_for('modelos'))

@app.route("/eliminar_modelo/<int:id>", methods=['POST'])
def eliminar_modelo(id):
    modelo = Modelo.query.get_or_404(id)
    modelo.activo = False
    db.session.commit()
    return redirect(url_for('modelos'))

@app.route("/modelos/anio/<int:anio>")
def modelos_by_anio(anio):
    modelos = Modelo.query.filter_by(anioLanzamiento=anio).all()
    
    return render_template(
        "modelos_by_anio.html",
        modelos=modelos,
        anio=anio,
    )

@app.route("/modelos/sistema_operativo/<sist_op>")
def modelos_by_sistema_operativo(sist_op):
    modelos = Modelo.query.filter_by(sistemaOperativo=sist_op).all()
       
    return render_template(
        "modelos_by_sistema_operativo.html",
        modelos=modelos,
        sistema_operativo=sist_op,
    )

@app.route("/modelo/<id>/editar", methods=['GET', 'POST'])
def modelo_editar(id):
    modelo = Modelo.query.get_or_404(id)

    if request.method == 'POST':
        modelo.modelo = request.form['modelo']
        modelo.anioLanzamiento = request.form['anioLanzamiento']
        modelo.sistemaOperativo = request.form['sistemaOperativo']
        db.session.commit()
        return redirect(url_for('modelos'))

    return render_template(
        "editar_modelo.html",
        modelo=modelo
    )

@app.route("/list_accesorios", methods=['POST', 'GET'])
def accesorios():
    accesorios = Accesorios.query.filter_by(activo=True).all()

    if request.method == 'POST':
        nombre = request.form['nombre']
        descripcion = request.form['descripcion']
        precio = request.form['precio']
        nuevoAccesorio = Accesorios(
            nombre=nombre,
            descripcion=descripcion,
            precio=precio,
        )
        db.session.add(nuevoAccesorio)
        db.session.commit()
        return redirect(url_for('accesorios'))

    return render_template('list_accesorios.html', accesorios=accesorios)

@app.route("/list_accesorios_inactivos", methods=['GET'])
def accesorios_inactivos():
    accesorios_inactivos = Accesorios.query.filter_by(activo=False).all()
    return render_template('list_accesorios_inactivos.html', accesorios=accesorios_inactivos)

@app.route("/restaurar_accesorio/<int:id>", methods=['POST'])
def restaurar_accesorio(id):
    accesorio = Accesorios.query.get_or_404(id)
    accesorio.activo = True
    db.session.commit()
    return redirect(url_for('accesorios'))

@app.route("/eliminar_accesorio/<int:id>", methods=['POST'])
def eliminar_accesorio(id):
    accesorio = Accesorios.query.get_or_404(id)
    accesorio.activo = False
    db.session.commit()
    return redirect(url_for('accesorios'))

@app.route("/accesorio/<id>/editar", methods=['GET', 'POST'])
def accesorio_editar(id):
    accesorio = Accesorios.query.get_or_404(id)

    if request.method == 'POST':
        accesorio.nombre = request.form['nombre']
        accesorio.descripcion = request.form['descripcion']
        accesorio.precio = request.form['precio']
        db.session.commit()
        return redirect(url_for('accesorios'))

    return render_template(
        "editar_accesorio.html",
        accesorio=accesorio
    )

@app.route("/list_proveedores", methods=['POST', 'GET'])
def proveedores():
    proveedores = Proveedor.query.filter_by(activo=True).all()

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

@app.route("/list_proveedores_inactivos", methods=['GET'])
def proveedores_inactivos():
    proveedores_inactivos = Proveedor.query.filter_by(activo=False).all()
    return render_template('list_proveedores_inactivos.html', proveedores=proveedores_inactivos)

@app.route("/restaurar_proveedor/<int:id>", methods=['POST'])
def restaurar_proveedor(id):
    proveedor = Proveedor.query.get_or_404(id)
    proveedor.activo = True
    db.session.commit()
    return redirect(url_for('proveedores'))

@app.route("/eliminar_proveedor/<int:id>", methods=['POST'])
def eliminar_proveedor(id):
    proveedor = Proveedor.query.get_or_404(id)
    proveedor.activo = False
    db.session.commit()
    return redirect(url_for('proveedores'))

@app.route("/proveedor/<id>/editar", methods=['GET', 'POST'])
def proveedor_editar(id):
    proveedor = Proveedor.query.get_or_404(id)

    if request.method == 'POST':
        proveedor.nombre = request.form['nombre']
        proveedor.contacto = request.form['contacto']
        db.session.commit()
        return redirect(url_for('proveedores'))

    return render_template(
        "editar_proveedor.html",
        proveedor=proveedor
    )

@app.route("/list_inventario", methods=['POST', 'GET'])
def inventarios():
    inventarios = Inventario.query.filter_by(activo=True).all()
    equipos = Equipo.query.filter_by(activo=True).all()
    accesorios = Accesorios.query.filter_by(activo=True).all()

    if request.method == 'POST':
        tipo = request.form['tipo']
        producto = request.form['producto']
        cantidadDisponible = request.form['cantidadDisponible']
        ubicacionAlmacen = request.form['ubicacionAlmacen']

        nuevoInventario = Inventario(
            tipo=tipo,
            producto=producto, 
            cantidadDisponible=cantidadDisponible,
            ubicacionAlmacen=ubicacionAlmacen,
        )
        db.session.add(nuevoInventario)
        db.session.commit()
        return redirect(url_for('inventarios'))

    return render_template(
        'list_inventario.html', 
        inventarios=inventarios,
        equipos=equipos,
        accesorios=accesorios,
    )

@app.route("/list_inventarios_inactivos", methods=['GET'])
def inventarios_inactivos():
    inventarios_inactivos = Inventario.query.filter_by(activo=False).all()
    return render_template('list_inventarios_inactivos.html', inventarios=inventarios_inactivos)

@app.route("/restaurar_inventario/<int:id>", methods=['POST'])
def restaurar_inventario(id):
    inventario = Inventario.query.get_or_404(id)
    inventario.activo = True
    db.session.commit()
    return redirect(url_for('inventarios'))

@app.route("/eliminar_inventario/<int:id>", methods=['POST'])
def eliminar_inventario(id):
    inventario = Inventario.query.get_or_404(id)
    inventario.activo = False
    db.session.commit()
    return redirect(url_for('inventarios'))

@app.route("/inventarios/tipo/<string:tipo>")
def inventarios_by_tipo(tipo):
    inventarios = Inventario.query.filter_by(tipo=tipo).all()
    
    return render_template(
        "inventarios_by_tipo.html",
        inventarios=inventarios,
        tipo=tipo,
    )

@app.route("/inventarios/ubicacion/<string:ubicacion>")
def inventarios_by_ubicacion(ubicacion):
    inventarios = Inventario.query.filter_by(ubicacionAlmacen=ubicacion).all()
    
    return render_template(
        "inventarios_by_ubicacion.html",
        inventarios=inventarios,
        ubicacion=ubicacion,
    )

@app.route("/inventario/<id>/editar", methods=['GET', 'POST'])
def inventario_editar(id):
    inventario = Inventario.query.get_or_404(id)
    equipos = Equipo.query.all()
    accesorios = Accesorios.query.all()

    if request.method == 'POST':
        inventario.tipo = request.form['tipo']
        inventario.producto = request.form['producto']
        inventario.cantidadDisponible = request.form['cantidadDisponible']
        inventario.ubicacionAlmacen = request.form['ubicacionAlmacen']
        db.session.commit()
        return redirect(url_for('inventarios'))

    return render_template(
        "editar_inventario.html",
        inventario=inventario,
        equipos=equipos,
        accesorios=accesorios,
    )

@app.route("/list_caracteristicas", methods=['POST', 'GET'])
def añadirCaracteristica():
    añadirCaracteristica = Caracteristicas.query.filter_by(activo=True).all()

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

@app.route("/list_caracteristicas_inactivas", methods=['GET'])
def caracteristicas_inactivas():
    caracteristicas_inactivas = Caracteristicas.query.filter_by(activo=False).all()
    return render_template('list_caracteristicas_inactivas.html', caracteristicas=caracteristicas_inactivas)

@app.route("/restaurar_caracteristica/<int:id>", methods=['POST'])
def restaurar_caracteristica(id):
    caracteristica = Caracteristicas.query.get_or_404(id)
    caracteristica.activo = True
    db.session.commit()
    return redirect(url_for('añadirCaracteristica'))

@app.route("/eliminar_caracteristica/<int:id>", methods=['POST'])
def eliminar_caracteristica(id):
    caracteristica = Caracteristicas.query.get_or_404(id)
    caracteristica.activo = False
    db.session.commit()
    return redirect(url_for('añadirCaracteristica'))

@app.route("/caracteristica/<id>/editar", methods=['GET', 'POST'])
def editar_caracteristica(id):
    caracteristica = Caracteristicas.query.get_or_404(id)

    if request.method == 'POST':
        caracteristica.nombre = request.form['nombre']
        caracteristica.descripcion = request.form['descripcion']
        db.session.commit()
        return redirect(url_for('añadirCaracteristica'))

    return render_template(
        "editar_caracteristica.html",
        caracteristica=caracteristica
    )

@app.route("/list_equipos", methods = ['POST', 'GET'])
def equipos():
    equipos = Equipo.query.filter_by(activo=True).all()
    modelos = Modelo.query.filter_by(activo=True).all()
    marcas = Marca.query.filter_by(activo=True).all()
    caracteristicas = Caracteristicas.query.filter_by(activo=True).all()
    proveedores = Proveedor.query.filter_by(activo=True).all()
    categorias = Categoria.query.filter_by(activo=True).all()
    
    if request.method == 'POST':
        modelo = request.form['modelo']
        marca = request.form['marca']
        categoria = request.form['categoria']
        precio = request.form['precio']
        caracteristicas = request.form['caracteristicas']
        proveedor = request.form['proveedor']
        nuevoEquipo = Equipo(
            modelo_id=modelo, 
            marca_id=marca,
            categoria_id=categoria,
            precio=precio,
            caracteristicas_id=caracteristicas,
            proveedor_id=proveedor,
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
        categorias=categorias,
        equipos=equipos,
    )

@app.route("/list_equipos_inactivos", methods=['GET'])
def equipos_inactivos():
    equipos_inactivos = Equipo.query.filter_by(activo=False).all()
    return render_template('list_equipos_inactivos.html', equipos=equipos_inactivos)

@app.route("/restaurar_equipo/<int:id>", methods=['POST'])
def restaurar_equipo(id):
    equipo = Equipo.query.get_or_404(id)
    equipo.activo = True
    db.session.commit()
    return redirect(url_for('equipos'))

@app.route("/eliminar_equipo/<int:id>", methods=['POST'])
def eliminar_equipo(id):
    equipo = Equipo.query.get_or_404(id)
    equipo.activo = False
    db.session.commit()
    return redirect(url_for('equipos'))

@app.route("/equipos/marca/<int:id>")
def equipos_by_marca(id):
    equipos = Equipo.query.filter_by(marca_id=id).all()
    marca = Marca.query.get(id).nombre

    return render_template(
        "equipos_by_marca.html",
        equipos=equipos,
        marca=marca,
    )

@app.route("/equipos/categoria/<int:id>")
def equipos_by_categoria(id):
    equipos = Equipo.query.filter_by(categoria_id=id).all()
    categoria = Categoria.query.get(id)

    return render_template(
        "equipos_by_categoria.html",
        equipos=equipos,
        categoria=categoria,
    )

@app.route("/equipos/proveedor/<int:id>")
def equipos_by_proveedor(id):
    equipos = Equipo.query.filter_by(proveedor_id=id).all()
    proveedor = Proveedor.query.get(id)

    return render_template(
        "equipos_by_proveedor.html",
        equipos=equipos,
        proveedor=proveedor,
    )

@app.route("/equipo/<id>/editar", methods=['GET', 'POST'])
def equipo_editar(id):
    equipo = Equipo.query.get_or_404(id)
    modelos = Modelo.query.all()
    marcas = Marca.query.all()
    categorias = Categoria.query.all()
    caracteristicas = Caracteristicas.query.all()
    proveedores = Proveedor.query.all()

    if request.method == 'POST':
        equipo.modelo_id = request.form['modelo']
        equipo.marca_id = request.form['marca']
        equipo.categoria_id = request.form['categoria']
        equipo.precio = request.form['precio']
        equipo.caracteristicas_id = request.form['caracteristicas']
        equipo.proveedor_id = request.form['proveedor']
        db.session.commit()
        return redirect(url_for('equipos'))

    return render_template(
        "editar_equipo.html",
        equipo=equipo,
        modelos=modelos,
        marcas=marcas,
        categorias=categorias,
        caracteristicas=caracteristicas,
        proveedores=proveedores
    )

@app.route("/list_pedidos", methods=['POST', 'GET'])
def pedidos():
    pedidos = Pedido.query.filter_by(activo=True).all()
    proveedores = Proveedor.query.filter_by(activo=True).all()

    if request.method == 'POST':
        proveedor = request.form['proveedor']
        fecha = request.form['fecha']
        total = request.form['total']
        nuevoPedido = Pedido(
            proveedor_id=proveedor,
            fecha=fecha,
            total=total,
        )
        db.session.add(nuevoPedido)
        db.session.commit()
        return redirect(url_for('pedidos'))

    return render_template(
        'list_pedidos.html', 
        pedidos=pedidos,
        proveedores=proveedores,   
    )

@app.route("/list_pedidos_inactivos", methods=['GET'])
def pedidos_inactivos():
    pedidos_inactivos = Pedido.query.filter_by(activo=False).all()
    return render_template('list_pedidos_inactivos.html', pedidos=pedidos_inactivos)

@app.route("/restaurar_pedido/<int:id>", methods=['POST'])
def restaurar_pedido(id):
    pedido = Pedido.query.get_or_404(id)
    pedido.activo = True
    db.session.commit()
    return redirect(url_for('pedidos'))

@app.route("/pedidos/proveedor/<int:proveedor_id>")
def pedidos_by_proveedor(proveedor_id):
    pedidos = Pedido.query.filter_by(proveedor_id=proveedor_id).all()
    proveedor = Proveedor.query.get(proveedor_id)
    
    return render_template(
        "pedidos_by_proveedor.html",
        pedidos=pedidos,
        proveedor=proveedor,
    )

@app.route("/pedidos/fecha/<string:fecha>")
def pedidos_by_fecha(fecha):
    pedidos = Pedido.query.filter_by(fecha=fecha).all()
    
    return render_template(
        "pedidos_by_fecha.html",
        pedidos=pedidos,
        fecha=fecha,
    )

@app.route("/pedido/<id>/editar", methods=['GET', 'POST'])
def pedido_editar(id):
    pedido = Pedido.query.get_or_404(id)
    proveedores = Proveedor.query.all()

    if request.method == 'POST':
        pedido.proveedor_id = request.form['proveedor']
        pedido.fecha = request.form['fecha']
        pedido.total = request.form['total']
        db.session.commit()
        return redirect(url_for('pedidos'))

    return render_template(
        "editar_pedido.html",
        pedido=pedido,
        proveedores=proveedores
    )

@app.route("/eliminar_pedido/<int:id>", methods=['POST'])
def eliminar_pedido(id):
    pedido = Pedido.query.get_or_404(id)
    pedido.activo = False
    db.session.commit()
    return redirect(url_for('pedidos'))

@app.route("/list_clientes", methods=['POST', 'GET'])
def clientes():
    clientes = Cliente.query.filter_by(activo=True).all()

    if request.method == 'POST':
        nombre = request.form['nombre']    
        direccion = request.form['direccion']
        telefono = request.form['telefono']
        email = request.form['email']
        fechaRegistro = request.form['fechaRegistro']        
        nuevoCliente = Cliente(
            nombre=nombre,
            direccion=direccion,
            telefono=telefono,
            email=email,
            fechaRegistro=fechaRegistro,
    )
        db.session.add(nuevoCliente)
        db.session.commit()
        return redirect(url_for('clientes'))

    return render_template(
        'list_clientes.html', 
        clientes=clientes,
    )

@app.route("/list_clientes_inactivos", methods=['GET'])
def clientes_inactivos():
    clientes_inactivos = Cliente.query.filter_by(activo=False).all()
    return render_template('list_clientes_inactivos.html', clientes=clientes_inactivos)

@app.route("/restaurar_cliente/<int:id>", methods=['POST'])
def restaurar_cliente(id):
    cliente = Cliente.query.get_or_404(id)
    cliente.activo = True
    db.session.commit()
    return redirect(url_for('clientes'))

@app.route("/clientes/fecha_registro/<string:fecha>")
def clientes_by_fecha(fecha):
    clientes = Cliente.query.filter_by(fechaRegistro=fecha).all()
    
    return render_template(
        "clientes_by_fecha.html",
        clientes=clientes,
        fecha=fecha,
    )

@app.route("/cliente/<id>/editar", methods=['GET', 'POST'])
def cliente_editar(id):
    cliente = Cliente.query.get_or_404(id)

    if request.method == 'POST':
        cliente.nombre = request.form['nombre']
        cliente.direccion = request.form['direccion']
        cliente.telefono = request.form['telefono']
        cliente.email = request.form['email']
        cliente.fechaRegistro = request.form['fechaRegistro']
        db.session.commit()
        return redirect(url_for('clientes'))

    return render_template(
        "editar_cliente.html",
        cliente=cliente
    )

@app.route("/eliminar_cliente/<int:id>", methods=['POST'])
def eliminar_cliente(id):
    cliente = Cliente.query.get_or_404(id)
    cliente.activo = False
    db.session.commit()
    return redirect(url_for('clientes'))

@app.route("/list_empleados", methods=['POST', 'GET'])
def empleados():
    empleados = Empleado.query.filter_by(activo=True).all()
    sucursales = Sucursal.query.filter_by(activo=True).all()

    if request.method == 'POST':
        nombre = request.form['nombre']    
        puesto = request.form['puesto']
        sucursal = request.form['sucursal']    
        nuevoEmpleado = Empleado(
            nombre=nombre,
            puesto=puesto,
            sucursal_id=sucursal,
    )
        db.session.add(nuevoEmpleado)
        db.session.commit()
        return redirect(url_for('empleados'))

    return render_template(
        'list_empleados.html', 
        empleados=empleados,
        sucursales=sucursales,
    )

@app.route("/list_empleados_inactivos", methods=['GET'])
def empleados_inactivos():
    empleados_inactivos = Empleado.query.filter_by(activo=False).all()
    return render_template('list_empleados_inactivos.html', empleados=empleados_inactivos)

@app.route("/restaurar_empleado/<int:id>", methods=['POST'])
def restaurar_empleado(id):
    empleado = Empleado.query.get_or_404(id)
    empleado.activo = True
    db.session.commit()
    return redirect(url_for('empleados'))

@app.route("/empleados/puesto/<string:puesto>")
def empleados_by_puesto(puesto):
    empleados = Empleado.query.filter_by(puesto=puesto).all()
    
    return render_template(
        "empleados_by_puesto.html",
        empleados=empleados,
        puesto=puesto,
    )

@app.route("/empleados/sucursal/<int:sucursal_id>")
def empleados_by_sucursal(sucursal_id):
    empleados = Empleado.query.filter_by(sucursal_id=sucursal_id).all()
    sucursal = Sucursal.query.get(sucursal_id)
    
    return render_template(
        "empleados_by_sucursal.html",
        empleados=empleados,
        sucursal=sucursal,
    )

@app.route("/empleado/<id>/editar", methods=['GET', 'POST'])
def empleado_editar(id):
    empleado = Empleado.query.get_or_404(id)
    sucursales = Sucursal.query.all()

    if request.method == 'POST':
        empleado.nombre = request.form['nombre']
        empleado.puesto = request.form['puesto']
        empleado.sucursal_id = request.form['sucursal']
        db.session.commit()
        return redirect(url_for('empleados'))

    return render_template(
        "editar_empleado.html",
        empleado=empleado,
        sucursales=sucursales
    )

@app.route("/eliminar_empleado/<int:id>", methods=['POST'])
def eliminar_empleado(id):
    empleado = Empleado.query.get_or_404(id)
    empleado.activo = False
    db.session.commit()
    return redirect(url_for('empleados'))

@app.route("/list_sucursales", methods=['POST', 'GET'])
def sucursales():
    sucursales = Sucursal.query.filter_by(activo=True).all()

    if request.method == 'POST':
        nombre = request.form['nombre']    
        direccion = request.form['direccion']
        telefono = request.form['telefono']    
        nuevaSucursal = Sucursal(
            nombre=nombre,
            direccion=direccion,
            telefono=telefono,
    )
        db.session.add(nuevaSucursal)
        db.session.commit()
        return redirect(url_for('sucursales'))

    return render_template(
        'list_sucursales.html', 
        sucursales=sucursales,
    )

@app.route("/list_sucursales_inactivas", methods=['GET'])
def sucursales_inactivas():
    sucursales_inactivas = Sucursal.query.filter_by(activo=False).all()
    return render_template('list_sucursales_inactivas.html', sucursales=sucursales_inactivas)

@app.route("/restaurar_sucursal/<int:id>", methods=['POST'])
def restaurar_sucursal(id):
    sucursal = Sucursal.query.get_or_404(id)
    sucursal.activo = True
    db.session.commit()
    return redirect(url_for('sucursales'))

@app.route("/sucursal/<id>/editar", methods=['GET', 'POST'])
def sucursal_editar(id):
    sucursal = Sucursal.query.get_or_404(id)

    if request.method == 'POST':
        sucursal.nombre = request.form['nombre']
        sucursal.direccion = request.form['direccion']
        sucursal.telefono = request.form['telefono']
        db.session.commit()
        return redirect(url_for('sucursales'))

    return render_template(
        "editar_sucursal.html",
        sucursal=sucursal
    )

@app.route("/eliminar_sucursal/<int:id>", methods=['POST'])
def eliminar_sucursal(id):
    sucursal = Sucursal.query.get_or_404(id)
    sucursal.activo = False
    db.session.commit()
    return redirect(url_for('sucursales'))

@app.route("/list_ventas", methods=['POST', 'GET'])
def ventas():
    ventas = Venta.query.filter_by(activo=True).all()
    clientes = Cliente.query.filter_by(activo=True).all()
    equipos = Equipo.query.filter_by(activo=True).all()
    accesorios = Accesorios.query.filter_by(activo=True).all()

    if request.method == 'POST':
        cliente = request.form['cliente']
        producto_id = int(request.form['producto'])
        tipo = request.form['tipo']
        fecha = request.form['fecha']
        cantidad = int(request.form['cantidad'])
        
        # Buscar el producto en las listas correspondientes
        producto = None
        if tipo == 'equipo':
            producto = next((p for p in equipos if p.id == producto_id), None)
        elif tipo == 'accesorio':
            producto = next((p for p in accesorios if p.id == producto_id), None)

        if producto:
            total = producto.precio * cantidad  # Calcular el total

            nuevaVenta = Venta(
                cliente_id=cliente,
                fecha=fecha,
                cantidad=cantidad,
                total=total,
                tipo=tipo,
                producto=producto.nombre,
            )
            db.session.add(nuevaVenta)
            db.session.commit()

        return redirect(url_for('ventas'))

    return render_template(
        'list_ventas.html',
        ventas=ventas,
        clientes=clientes,
        equipos=equipos,
        accesorios=accesorios,
    )

@app.route("/ventas/cliente/<int:cliente_id>")
def ventas_by_cliente(cliente_id):
    ventas = Venta.query.filter_by(cliente_id=cliente_id).all()
    cliente = Cliente.query.get(cliente_id)
    
    return render_template(
        "ventas_by_cliente.html",
        ventas=ventas,
        cliente=cliente,
    )

@app.route("/ventas/producto/<string:producto>")
def ventas_by_producto(producto):
    ventas = Venta.query.filter_by(producto=producto).all()
    
    return render_template(
        "ventas_by_producto.html",
        ventas=ventas,
        producto=producto,
    )

@app.route("/ventas/fecha/<string:fecha>")
def ventas_by_fecha(fecha):
    ventas = Venta.query.filter_by(fecha=fecha).all()

    return render_template(
        "ventas_by_fecha.html",
        ventas=ventas,
        fecha=fecha,
    )

@app.route("/ventas/tipo/<string:tipo>")
def ventas_by_tipo(tipo):
    ventas = Venta.query.filter_by(tipo=tipo).all()

    return render_template(
        "ventas_by_tipo.html",
        ventas=ventas,
        tipo=tipo,
    )

@app.route("/venta/<int:id>/editar", methods=['GET', 'POST'])
def venta_editar(id):
    
    venta = Venta.query.get_or_404(id)
    clientes = Cliente.query.all()
    equipos = Equipo.query.all()
    accesorios = Accesorios.query.all()

    if request.method == 'POST':
        venta.cliente_id = request.form['cliente']
        venta.tipo = request.form['tipo']
        venta.producto_id = int(request.form['producto'])
        venta.fecha = request.form['fecha']
        venta.cantidad = int(request.form['cantidad'])

        # Actualizar el total según el producto y cantidad
        producto = None
        if venta.tipo == 'equipo':
            producto = next((p for p in equipos if p.id == venta.producto_id), None)
        elif venta.tipo == 'accesorio':
            producto = next((p for p in accesorios if p.id == venta.producto_id), None)

        if producto:
            venta.total = producto.precio * venta.cantidad
            db.session.commit()
            return redirect(url_for('ventas'))

    return render_template(
        'editar_venta.html',
        venta=venta,
        clientes=clientes,
        equipos=equipos,
        accesorios=accesorios,
    )

@app.route("/eliminar_venta/<int:id>", methods=['POST'])
def eliminar_venta(id):
    venta = Venta.query.get_or_404(id)
    venta.activo = False
    db.session.commit()
    return redirect(url_for('ventas'))

@app.route("/list_ventas_inactivas", methods=['GET'])
def ventas_inactivas():
    ventas_inactivas = Venta.query.filter_by(activo=False).all()
    return render_template('list_ventas_inactivas.html', ventas=ventas_inactivas)

@app.route("/restaurar_venta/<int:id>", methods=['POST'])
def restaurar_venta(id):
    venta = Venta.query.get_or_404(id)
    venta.activo = True
    db.session.commit()
    return redirect(url_for('ventas'))
