from flask import Flask, render_template, request, flash, redirect, make_response, send_file
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
import sqlite3
import pdfkit
from reportlab.pdfgen import canvas
from io import BytesIO
app = Flask(__name__)
app.secret_key = '040518'
bootstrap=Bootstrap(app)  

# Función para obtener todos los clientes desde la base de datos
def obtener_clientes():
    conn = sqlite3.connect('farmacia.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM clientes')
    clientes = cursor.fetchall()
    conn.close()
    return clientes
# ...

def borrar_cliente(cliente_id):
    conn = sqlite3.connect('farmacia.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM clientes WHERE id = ?', (cliente_id,))
    conn.commit()
    conn.close()

def actualizar_cliente(cliente_id, nombre, direccion, telefono, correo):
    conn = sqlite3.connect('farmacia.db')
    cursor = conn.cursor()
    cursor.execute('UPDATE clientes SET nombre = ?, direccion = ?, telefono = ?, correo = ? WHERE id = ?',
                   (nombre, direccion, telefono, correo, cliente_id))
    conn.commit()
    conn.close()

# Función para obtener todos los productos desde la base de datos
def obtener_productos():
    conn = sqlite3.connect('farmacia.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM productos')
    productos = cursor.fetchall()
    conn.close()
    return productos

#Encontrar productos
def encontrar_productos(busqueda):
    conn = sqlite3.connect('farmacia.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM productos WHERE nombre LIKE ?', ('%' + busqueda + '%',))
    productos = cursor.fetchall()
    conn.close()
    return productos

#actualizar producto
def actualizar_producto(producto_id, nombre, precio, stock):
    conn = sqlite3.connect('farmacia.db')
    cursor = conn.cursor()
    cursor.execute('UPDATE productos SET nombre = ?, precio = ?, stock = ? WHERE id = ?', (nombre, precio, stock, producto_id))
    conn.commit()
    conn.close()
#Eliminar Producto

def borrar_producto(producto_id):
    conn = sqlite3.connect('farmacia.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM productos WHERE id = ?', (producto_id,))
    conn.commit()
    conn.close()
# Función para obtener todas las facturas desde la base de datos
def obtener_facturas():
    conn = sqlite3.connect('farmacia.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM facturas')
    facturas = cursor.fetchall()
    conn.close()
    return facturas


#dar facturas
def dar_facturas(factura_id):
    # Lógica para obtener los datos de la factura con el ID proporcionado desde la base de datos
    
    # Ejemplo de conexión a la base de datos
    conn = sqlite3.connect('farmacia.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM facturas WHERE id = ?', (factura_id,))
       # Ejemplo de consulta SQL para obtener los datos de la factura
    facturas = cursor.fetchone()
    
    # Cerrar la conexión a la base de datos
    conn.close()
    
    return facturas

#dar factura pdf
def obtener_factura_pdf(factura_id):
    conn = sqlite3.connect('farmacia.db')  # Conexión a la base de datos
    cursor = conn.cursor()

    # Obtener los datos de la factura según el ID proporcionado
    cursor.execute('SELECT * FROM facturas WHERE id = ?', (factura_id,))
    factura = cursor.fetchone()  # Obtener la primera fila de resultados

    # Cerrar la conexión a la base de datos
    cursor.close()
    conn.close()

    # Comprobar si se encontró la factura
    if factura:
        # Devolver un diccionario con los datos de la factura
        factura_dict = {
            'id': factura[0],
            'cliente_id': factura[1],
            'sucursal': factura[2],
            'fecha': factura[3],
            'total': factura[4]
        }
        return factura_dict
    else:
        return None

#borrar factura
def borrar_factura(factura_id):
    conn = sqlite3.connect('farmacia.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM facturas WHERE id = ?', (factura_id,))
    conn.commit()
    conn.close()

#actualizar factura
def actualizar_factura(factura_id, sucursal, fecha, total):
    conn = sqlite3.connect('farmacia.db')
    cursor = conn.cursor()
    cursor.execute('UPDATE facturas SET sucursal = ?, fecha = ?, total = ? WHERE id = ?', (sucursal, fecha, total, factura_id))
    conn.commit()
    conn.close()


# Función para guardar un cliente en la base de datos
def guardar_cliente(nombre, direccion, telefono, correo):
    conn = sqlite3.connect('farmacia.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM clientes WHERE nombre = ?', (nombre,))
    cliente_existente = cursor.fetchone()
    
    if cliente_existente:
        flash('El cliente ya existe', 'error')
    else:
        cursor.execute('INSERT INTO clientes (nombre, direccion, telefono, correo) VALUES (?, ?, ?, ?)',
                       (nombre, direccion, telefono, correo))
        conn.commit()
        flash('Cliente agregado correctamente', 'success')
    
    conn.close()

# Función para buscar clientes en la base de datos
def encontrar_clientes(busqueda):
    conn = sqlite3.connect('farmacia.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM clientes WHERE nombre LIKE ?', ('%' + busqueda + '%',))
    clientes = cursor.fetchall()
    conn.close()
    return clientes
def obtener_productos():
    conn = sqlite3.connect('farmacia.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM productos')
    productos = cursor.fetchall()
    conn.close()
    return productos

# Función para guardar un producto en la base de datos
def guardar_producto(nombre, precio, stock):
    conn = sqlite3.connect('farmacia.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO productos (nombre, precio, stock) VALUES (?, ?, ?)',
                   (nombre, precio, stock))
    conn.commit()
    conn.close()

# Función para guardar una factura en la base de datos
def guardar_factura(cliente_id, sucursal, fecha, total):
    conn = sqlite3.connect('farmacia.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO facturas (cliente_id, sucursal, fecha, total) VALUES (?, ?, ?, ?)',
                   (cliente_id, sucursal, fecha, total))
    conn.commit()
    conn.close()
# Ruta de la página de inicio
@app.route('/')
def index():
    return render_template('index.html', active='inicio')

# Ruta de la página de clientes
@app.route('/clientes')
def clientes():
    clientes = obtener_clientes()  # Función para obtener los clientes desde la base de datos
    return render_template('clientes.html', active='clientes', clientes=clientes)
# Ruta para agregar un cliente
@app.route('/agregar_cliente', methods=['GET', 'POST'])
def agregar_cliente():
    if request.method == 'POST':
        nombre = request.form['nombre']
        direccion = request.form['direccion']
        telefono = request.form['telefono']
        correo = request.form['correo']
        guardar_cliente(nombre, direccion, telefono, correo)  # Función para guardar el cliente en la base de datos
        return redirect('/clientes')
    return render_template('agregar_cliente.html')

# Ruta para buscar clientes
@app.route('/buscar_cliente', methods=['POST'])
def buscar_cliente():
    busqueda = request.form['busqueda']
    clientes = encontrar_clientes(busqueda)  # Función para buscar clientes en la base de datos
    return render_template('clientes.html', active='clientes', clientes=clientes)

# Ruta para editar un cliente
@app.route('/editar_cliente/<int:cliente_id>', methods=['GET', 'POST'])
def editar_cliente(cliente_id):
    if request.method == 'POST':
        nombre = request.form['nombre']
        direccion = request.form['direccion']
        telefono = request.form['telefono']
        correo = request.form['correo']
        actualizar_cliente(cliente_id, nombre, direccion, telefono, correo)  # Función para actualizar el cliente en la base de datos
        flash('Cliente actualizado correctamente', 'success')
        return redirect('/clientes')
    else:
        conn = sqlite3.connect('farmacia.db')
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM clientes WHERE id = ?', (cliente_id,))
        cliente = cursor.fetchone()
        conn.close()
        if cliente:
            return render_template('editar_cliente.html', cliente=cliente)
        else:
            flash('Cliente no encontrado', 'error')
            return redirect('/clientes')
# Ruta de la página de productos
@app.route('/productos')
def productos():
    productos = obtener_productos()  # Función para obtener los productos desde la base de datos
    return render_template('productos.html', active='productos', productos=productos)
#buscar producto

@app.route('/buscar_producto', methods=['POST'])
def buscar_producto():
    busqueda = request.form['busqueda']
    productos = encontrar_productos(busqueda)  # Función para buscar productos en la base de datos
    return render_template('productos.html', active='productos', productos=productos)



# Ruta para eliminar un cliente
@app.route('/eliminar_cliente/<int:cliente_id>', methods=['POST'])
def eliminar_cliente(cliente_id):
    borrar_cliente(cliente_id)  # Función para eliminar el cliente de la base de datos
    flash('Cliente eliminado correctamente', 'success')
    return redirect('/clientes')
# Ruta para agregar un producto
@app.route('/agregar_producto', methods=['GET', 'POST'])
def agregar_producto():
    if request.method == 'POST':
        nombre = request.form['nombre']
        precio = float(request.form['precio'])
        stock = int(request.form['stock'])
        guardar_producto(nombre, precio, stock)  # Función para guardar el producto en la base de datos
        return redirect('/productos')
    return render_template('agregar_producto.html', productos=productos)

@app.route('/editar_producto/<int:producto_id>', methods=['GET', 'POST'])
def editar_producto(producto_id):
    if request.method == 'POST':
        nombre = request.form['nombre']
        precio = float(request.form['precio'])
        stock = int(request.form['stock'])
        actualizar_producto(producto_id, nombre, precio, stock)  # Función para actualizar el producto en la base de datos
        flash('Producto actualizado correctamente', 'success')
        return redirect('/productos')
    else:
        producto = obtener_producto(producto_id)  # Función para obtener el producto de la base de datos
        if producto:
            return render_template('editar_producto.html', producto=producto)
        else:
            flash('Producto no encontrado', 'error')
            return redirect('/productos')# Ruta para eliminar un producto
@app.route('/eliminar_producto/<int:producto_id>', methods=['POST'])
def eliminar_producto(producto_id):
    borrar_producto(producto_id)  # Función para eliminar el producto de la base de datos
    flash('Producto eliminado correctamente', 'success')
    return redirect('/productos')
# Ruta de la página de facturas
@app.route('/facturas')
def facturas():
    facturas = obtener_facturas()  # Función para obtener las facturas desde la base de datos
    return render_template('facturas.html', active='facturas', facturas=facturas)
# Ruta para agregar una factura

@app.route('/agregar_factura', methods=['GET', 'POST'])
def agregar_factura():
    if request.method == 'POST':
        # Obtener los datos del formulario
        cliente_id = request.form['cliente']
        sucursal = request.form['sucursal']
        fecha = request.form['fecha']
        
        # Obtener los productos seleccionados y calcular el total
        productos = request.form.getlist('productos')
        total = sum(float(request.form['precio_' + producto]) for producto in productos)
        guardar_factura(cliente_id, sucursal, fecha, total)
        # Lógica para guardar la factura en la base de datos
        
        return redirect('/facturas')
    
    clientes = obtener_clientes()  # Función para obtener los clientes desde la base de datos
    productos = obtener_productos()  # Función para obtener los productos desde la base de datos
    
    return render_template('agregar_factura.html', clientes=clientes, productos=productos)

#descargar factura
@app.route('/generar_pdf/<factura_id>')
def generar_pdf(factura_id):
    factura = obtener_factura_pdf(factura_id)  # Obtener los datos de la factura desde la base de datos

    # Crear un objeto de BytesIO para almacenar el PDF
    buffer = BytesIO()

    # Crear un objeto de lienzo (canvas) para el PDF
    p = canvas.Canvas(buffer)

    # Agregar contenido al PDF
    p.setFont("Helvetica", 12)
    p.drawString(50, 750, "Factura")
    p.drawString(50, 700, "ID de Factura: {}".format(factura['id']))
    p.drawString(50, 680, "Fecha: {}".format(factura['fecha']))
    p.drawString(50, 660, "Cliente: {}".format(factura['cliente_id']))
    p.drawString(50, 640, "Total: ${:.2f}".format(float(factura['total'])))

    # Finalizar el lienzo (canvas)
    p.showPage()
    p.save()

    # Reiniciar el buffer y configurar la posición en el inicio
    buffer.seek(0)

    # Enviar el archivo PDF como una respuesta de descarga
    # Crear una respuesta Flask con el PDF adjunto
    response = make_response(send_file(buffer, mimetype='application/pdf'))
    response.headers['Content-Disposition'] = 'attachment; filename=factura.pdf'

    return response
@app.route('/editar_factura/<factura_id>', methods=['GET', 'POST'])
def editar_factura(factura_id):
    if request.method == 'POST':
        sucursal = request.form['sucursal']
        fecha = request.form['fecha']
        total = float(request.form['total'])
        actualizar_factura(factura_id, sucursal, fecha, total)  # Función para actualizar la factura en la base de datos
        return redirect('/facturas')
    factura = dar_facturas(factura_id)  # Función para obtener los datos de la factura desde la base de datos
    return render_template('editar_factura.html', factura=factura)

@app.route('/eliminar_factura/<factura_id>', methods=['POST'])
def eliminar_factura(factura_id):
    borrar_factura(factura_id)  # Función para eliminar la factura de la base de datos
    return redirect('/facturas')
if __name__ == '__main__':
    app.run()
