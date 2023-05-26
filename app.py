from flask import Flask, render_template, request, redirect, make_response
from flask_bootstrap import Bootstrap
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import sqlite3
app = Flask(__name__)
bootstrap=Bootstrap(app)
#####################USUARIOS###############################
def registrar_usuario(nombre, apellido, dni, password):
    conn = sqlite3.connect('farmacia.db')
    cursor = conn.cursor()

    # Insertar los datos del nuevo usuario en la tabla usuarios
    cursor.execute('INSERT INTO usuarios (nombre, apellido, dni, contraseña) VALUES (?, ?, ?, ?)',
                   (nombre, apellido, dni, password))

    # Guardar los cambios y cerrar la conexión
    conn.commit()
    conn.close()

def verificar_usuario_existente(dni):
    conn = sqlite3.connect('farmacia.db')
    cursor = conn.cursor()

    # Buscar si existe un usuario con el DNI proporcionado
    cursor.execute('SELECT * FROM usuarios WHERE dni = ?', (dni,))
    usuario = cursor.fetchone()

    # Cerrar la conexión
    conn.close()

    # Si se encontró un usuario con el DNI proporcionado, devuelve True; de lo contrario, devuelve False
    return usuario is not None
import sqlite3

def verificar_credenciales(dni, password):
    conn = sqlite3.connect('farmacia.db')
    cursor = conn.cursor()

    # Buscar al usuario por su DNI y contraseña
    cursor.execute('SELECT * FROM usuarios WHERE dni = ? AND contraseña = ?', (dni, password))
    usuario = cursor.fetchone()

    # Cerrar la conexión
    conn.close()

    # Si se encontró un usuario con las credenciales proporcionadas, devuelve True; de lo contrario, devuelve False
    return usuario is not None


############################################################
##############################CLIENTES################################

def obtener_clientes_por_nombre(nombre):
    conn = sqlite3.connect('farmacia.db')
    cursor = conn.cursor()

    # Realizar la consulta para obtener los clientes por nombre
    cursor.execute("SELECT * FROM clientes WHERE nombre LIKE ?", ('%' + nombre + '%',))
    clientes = cursor.fetchall()

    # Cerrar la conexión
    conn.close()

    return clientes

######################################################################
def obtener_productos_por_nombre(nombre):
    conn = sqlite3.connect('farmacia.db')
    cursor = conn.cursor()

    # Realizar la consulta para obtener los clientes por nombre
    cursor.execute("SELECT * FROM productos WHERE nombre LIKE ?", ('%' + nombre + '%',))
    productos = cursor.fetchall()

    # Cerrar la conexión
    conn.close()

    return productos



##############################################
# Función para calcular el total de la factura
def calcular_total(cantidad, precio):
    return cantidad * precio

# Función para obtener la lista de productos
def obtener_productos():
    conn = sqlite3.connect('farmacia.db')
    cursor = conn.cursor()
    cursor.execute('SELECT codigo, nombre FROM productos')
    productos = cursor.fetchall()
    conn.close()
    return productos

# Función para obtener la lista de clientes
def obtener_clientes():
    conn = sqlite3.connect('farmacia.db')
    cursor = conn.cursor()
    cursor.execute('SELECT id, nombre FROM clientes')
    clientes = cursor.fetchall()
    conn.close()
    return clientes

# Función para obtener la lista de usuarios
def obtener_usuarios():
    conn = sqlite3.connect('farmacia.db')
    cursor = conn.cursor()
    cursor.execute('SELECT id, nombre FROM usuarios')
    usuarios = cursor.fetchall()
    conn.close()
    return usuarios
# Ruta para el inicio de sesión (login)
@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Obtener los datos del formulario de inicio de sesión
        dni = request.form.get('dni')
        password = request.form.get('password')
        
        # Verificar las credenciales del usuario en la base de datos
        if verificar_credenciales(dni, password):
            # Si las credenciales son válidas, realizar alguna acción (por ejemplo, redirigir a la página principal)
            return redirect('/inicio')
        else: 
            # Si las credenciales son inválidas, mostrar un mensaje de error
            error = 'DNI o contraseña incorrectos'
            return render_template('login.html', error=error)
    else:
        # Renderizar la plantilla del formulario de inicio de sesión
        return render_template('login.html')

# Ruta para el registro de usuario
@app.route('/registro', methods=['GET', 'POST'])
def registro():
    if request.method == 'POST':
        # Obtener los datos del formulario de registro de usuario
        nombre = request.form.get('nombre')
        apellido = request.form.get('apellido')
        dni = request.form.get('dni')
        password = request.form.get('password')
        
        # Verificar si el usuario ya está registrado en la base de datos
        if verificar_usuario_existente(dni):
            error = 'El usuario ya está registrado'
            return render_template('registro.html', error=error)
        else:
            # Registrar al nuevo usuario en la base de datos
            registrar_usuario(nombre, apellido, dni, password)
            # Realizar alguna acción adicional, como redirigir a la página de inicio de sesión
            return redirect('/')
    else:
        # Renderizar la plantilla del formulario de registro de usuario
        return render_template('registro.html')

@app.route('/inicio')
def pagina1():
    return render_template('home.html')

# Ruta para mostrar todos los clientes
@app.route('/clientes')
def mostrar_clientes():
    conn = sqlite3.connect('farmacia.db')
    cursor = conn.cursor()

    # Obtener todos los clientes de la base de datos
    cursor.execute('SELECT * FROM clientes')
    clientes = cursor.fetchall()

    # Cerrar la conexión 
    conn.close()

    return render_template('clientes.html', clientes=clientes)

# Ruta para ingresar un nuevo cliente
@app.route('/clientes/ingresar', methods=['GET', 'POST'])
def ingresar_cliente():
    if request.method == 'POST':
        # Obtener los datos del formulario de ingreso de cliente
        nombre = request.form.get('nombre')
        apellido = request.form.get('apellido')
        dni = request.form.get('dni')
        direccion = request.form.get('direccion')

        conn = sqlite3.connect('farmacia.db')
        cursor = conn.cursor()

        # Insertar el nuevo cliente en la base de datos
        cursor.execute('INSERT INTO clientes (nombre, apellido, dni, dirección) VALUES (?, ?, ?, ?)',
                       (nombre, apellido, dni, direccion))
        conn.commit()

        # Cerrar la conexión
        conn.close()

        # Redirigir a la página de mostrar clientes
        return redirect('/clientes')
    else:
        return render_template('ingresar_cliente.html')

# Ruta para editar un cliente existente
@app.route('/clientes/editar/<int:cliente_id>', methods=['GET', 'POST'])
def editar_cliente(cliente_id):
    if request.method == 'POST':
        # Obtener los datos del formulario de edición de cliente
        nombre = request.form.get('nombre')
        apellido = request.form.get('apellido')
        dni = request.form.get('dni')
        direccion = request.form.get('direccion')

        conn = sqlite3.connect('farmacia.db')
        cursor = conn.cursor()

        # Actualizar los datos del cliente en la base de datos
        cursor.execute('UPDATE clientes SET nombre=?, apellido=?, dni=?, dirección=? WHERE id=?',
                       (nombre, apellido, dni, direccion, cliente_id))
        conn.commit()

        # Cerrar la conexión
        conn.close()

        # Redirigir a la página de mostrar clientes
        return redirect('/clientes')
    else:
        conn = sqlite3.connect('farmacia.db')
        cursor = conn.cursor()

        # Obtener los datos del cliente a editar de la base de datos
        cursor.execute('SELECT * FROM clientes WHERE id=?', (cliente_id,))
        cliente = cursor.fetchone()

        # Cerrar la conexión
        conn.close()

        return render_template('editar_cliente.html', cliente=cliente)

# Ruta para eliminar un cliente existente
@app.route('/clientes/eliminar/<int:cliente_id>', methods=['POST'])
def eliminar_cliente(cliente_id):
    conn = sqlite3.connect('farmacia.db')
    cursor = conn.cursor()

    # Eliminar el cliente de la base de datos
    cursor.execute('DELETE FROM clientes WHERE id=?', (cliente_id,))
    conn.commit()

    # Cerrar la conexión
    conn.close()

    # Redirigir a la página de mostrar clientes
    return redirect('/clientes')

@app.route('/buscar_cliente', methods=['GET'])
def buscar_cliente():
    nombre = request.args.get('nombre')
    clientes = obtener_clientes_por_nombre(nombre)  # Implementa la lógica para obtener los clientes por nombre

    return render_template('clientes.html', clientes=clientes)

####################################################################################

# Ruta para mostrar todos los productos
@app.route('/productos')
def mostrar_productos():
    conn = sqlite3.connect('farmacia.db')
    cursor = conn.cursor()

    # Obtener todos los productos de la base de datos
    cursor.execute('SELECT * FROM productos')
    productos = cursor.fetchall()

    # Cerrar la conexión 
    conn.close()

    return render_template('productos.html', productos=productos)

# Ruta para ingresar un nuevo producto
@app.route('/productos/ingresar', methods=['GET', 'POST'])
def ingresar_producto():
    if request.method == 'POST':
        # Obtener los datos del formulario de ingreso de producto
        nombre = request.form.get('nombre')
        detalle = request.form.get('detalle')
        stock = request.form.get('stock')
        cantidad_vendida = request.form.get('cantidad_vendida')
        precio = request.form.get('precio')

        conn = sqlite3.connect('farmacia.db')
        cursor = conn.cursor()

        # Insertar el nuevo producto en la base de datos
        cursor.execute('INSERT INTO productos (nombre, detalle, stock, cantidad_vendida, precio) VALUES (?, ?, ?, ?, ?)',
                       (nombre, detalle, stock, cantidad_vendida, precio))
        conn.commit()

        # Cerrar la conexión
        conn.close()

        # Redirigir a la página de mostrar productos
        return redirect('/productos')
    else:
        return render_template('ingresar_productos.html')

# Ruta para editar un producto existente
@app.route('/productos/editar/<int:producto_id>', methods=['GET', 'POST'])
def editar_producto(producto_id):
    if request.method == 'POST':
        # Obtener los datos del formulario de edición de producto
        nombre = request.form.get('nombre')
        detalle = request.form.get('detalle')
        stock = request.form.get('stock')
        cantidad_vendida = request.form.get('cantidad_vendida')
        precio = request.form.get('precio')

        conn = sqlite3.connect('farmacia.db')
        cursor = conn.cursor()

        # Actualizar los datos del producto en la base de datos
        cursor.execute('UPDATE productos SET nombre=?, detalle=?, stock=?, cantidad_vendida=?, precio=? WHERE codigo=?',
                       (nombre, detalle, stock, cantidad_vendida, precio, producto_id))
        conn.commit()

        # Cerrar la conexión
        conn.close()

        # Redirigir a la página de mostrar productos
        return redirect('/productos')
    else:
        conn = sqlite3.connect('farmacia.db')
        cursor = conn.cursor()

        # Obtener los datos del producto a editar de la base de datos
        cursor.execute('SELECT * FROM productos WHERE codigo=?', (producto_id,))
        producto = cursor.fetchone()

        # Cerrar la conexión
        conn.close() 

        return render_template('editar_producto.html', producto=producto)

# Ruta para eliminar un producto existente
@app.route('/productos/eliminar/<int:producto_id>', methods=['POST'])
def eliminar_producto(producto_id):
    conn = sqlite3.connect('farmacia.db')
    cursor = conn.cursor()

    # Eliminar el producto de la base de datos
    cursor.execute('DELETE FROM productos WHERE codigo=?', (producto_id,))
    conn.commit()

    # Cerrar la conexión
    conn.close()

    # Redirigir a la página de mostrar productos
    return redirect('/productos')

@app.route('/buscar_producto', methods=['GET'])
def buscar_producto():
    nombre = request.args.get('nombre')
    productos = obtener_productos_por_nombre(nombre)  

    return render_template('productos.html', productos=productos)

###################################################################################
# Ruta para mostrar todas las facturas
@app.route('/facturas')
def mostrar_facturas():
    conn = sqlite3.connect('farmacia.db')
    cursor = conn.cursor()

    # Obtener todas las facturas de la base de datos
    cursor.execute('SELECT * FROM facturas')
    facturas = cursor.fetchall()

    # Cerrar la conexión
    conn.close()

    return render_template('facturas.html', facturas=facturas)

# Ruta para ingresar una nueva factura
@app.route('/facturas/ingresar', methods=['GET', 'POST'])
def ingresar_factura():
    if request.method == 'POST':
        # Obtener los datos del formulario de ingreso de factura
        cliente_id = request.form.get('cliente_id')
        usuario_id = request.form.get('usuario_id')
        fecha_factura = request.form.get('fecha_factura')
        impuestos = float(request.form.get('impuestos'))
        total = float(request.form.get('total'))
        producto_id = request.form.get('producto')
        cantidad_comprada = int(request.form.get('cantidad'))
        precio_unitario = float(request.form.get('precio'))
        
        # Calcular el total de la factura
        subtotal = cantidad_comprada * precio_unitario
        total = subtotal + impuestos

        conn = sqlite3.connect('farmacia.db')
        cursor = conn.cursor()
                # Insertar la nueva factura en la base de datos
        cursor.execute('INSERT INTO facturas (cliente_id, usuario_id, fecha_factura, producto_id, cantidad_comprada, precio_unitario, impuestos, total) VALUES (?, ?, ?, ?, ?, ?, ?, ?)',
                       (cliente_id, usuario_id, fecha_factura, producto_id, cantidad_comprada, precio_unitario, impuestos, total))

        conn.commit()

        # Cerrar la conexión
        conn.close()

        # Redirigir a la página de mostrar facturas
        return redirect('/facturas')

    productos = obtener_productos()
    clientes = obtener_clientes()
    usuarios = obtener_usuarios()
    total = 0.0
    return render_template('ingresar_facturas.html', productos=productos, clientes=clientes, usuarios=usuarios)

# Ruta para eliminar una factura existente.
@app.route('/facturas/eliminar/<int:factura_id>', methods=['POST'])
def eliminar_factura(factura_id):
    conn = sqlite3.connect('farmacia.db')
    cursor = conn.cursor()

    # Eliminar la factura de la base de datos
    cursor.execute('DELETE FROM facturas WHERE numero_factura=?', (factura_id,))
    conn.commit()

    # Cerrar la conexión
    conn.close()

    # Redirigir a la página de mostrar facturas
    return redirect('/facturas')




###################################################################################







if __name__ == '__main__': 
    app.run(debug=True)
