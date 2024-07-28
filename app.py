from flask import Flask, render_template, redirect, request, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost/tienda_celulares'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)

from models import Marca, Categoria, Proveedor, Inventario, Accesorios, Caracteristicas, Fabricante, Modelo, Equipo, Pedido, Cliente, Empleado, Sucursal, Venta

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/list_marca", methods=['POST', 'GET'])
def marcas():
    marcas = Marca.query.all()
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


@app.route("/list_accesorios", methods=['POST', 'GET'])
def accesorios():
    accesorios = Accesorios.query.all()

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

@app.route("/list_inventario", methods=['POST', 'GET'])
def inventarios():
    inventarios = Inventario.query.all()
    equipos = Equipo.query.all()
    accesorios = Accesorios.query.all()

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
    categorias = Categoria.query.all()
    
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

@app.route("/list_pedidos", methods=['POST', 'GET'])
def pedidos():
    pedidos = Pedido.query.all()
    proveedores = Proveedor.query.all()

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


@app.route("/list_clientes", methods=['POST', 'GET'])
def clientes():
    clientes = Cliente.query.all()

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

@app.route("/clientes/fecha_registro/<string:fecha>")
def clientes_by_fecha(fecha):
    clientes = Cliente.query.filter_by(fechaRegistro=fecha).all()
    
    return render_template(
        "clientes_by_fecha.html",
        clientes=clientes,
        fecha=fecha,
    )

@app.route("/list_empleados", methods=['POST', 'GET'])
def empleados():
    empleados = Empleado.query.all()
    sucursales = Sucursal.query.all()

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


@app.route("/list_sucursales", methods=['POST', 'GET'])
def sucursales():
    sucursales = Sucursal.query.all()

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

@app.route("/list_ventas", methods=['POST', 'GET'])
def ventas():
    ventas = Venta.query.all()
    clientes = Cliente.query.all()
    equipos = Equipo.query.all()
    accesorios = Accesorios.query.all()

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

