import sqlite3

# Crear una conexión a la base de datos
conn = sqlite3.connect('farmacia.db')

# Crear una tabla 'clientes' en la base de datos
conn.execute('''
    CREATE TABLE IF NOT EXISTS clientes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT NOT NULL,
        direccion TEXT NOT NULL,
        telefono TEXT NOT NULL,
        correo TEXT NOT NULL
    )
''')

# Crear una tabla 'productos' en la base de datos
conn.execute('''
    CREATE TABLE IF NOT EXISTS productos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT NOT NULL,
        precio REAL NOT NULL,
        stock INTEGER NOT NULL
    )
''')

# Crear una tabla 'facturas' en la base de datos
conn.execute('''
    CREATE TABLE IF NOT EXISTS facturas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        cliente_id INTEGER NOT NULL,
        sucursal TEXT NOT NULL,
        fecha TEXT NOT NULL,
        total REAL NOT NULL,
        FOREIGN KEY (cliente_id) REFERENCES clientes (id)
    )
''')

# Crear una tabla 'detalle_factura' en la base de datos
conn.execute('''
    CREATE TABLE IF NOT EXISTS detalle_factura (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        factura_id INTEGER NOT NULL,
        producto_id INTEGER NOT NULL,
        cantidad INTEGER NOT NULL,
        subtotal REAL NOT NULL,
        FOREIGN KEY (factura_id) REFERENCES facturas (id),
        FOREIGN KEY (producto_id) REFERENCES productos (id)
    )
''')

# Insertar datos de ejemplo en la tabla 'clientes'
clientes = [
    ('Juan Pérez', 'Calle 123', '123456789', 'juanperez@gmail.com'),
    ('María López', 'Avenida 456', '987654321', 'marialopez@gmail.com'),
    ('Pedro Rodríguez', 'Calle 789', '456789123', 'pedrorodriguez@gmail.com'),
    ('Ana Gómez', 'Avenida 789', '321654987', 'anagomez@gmail.com'),
    ('Luisa García', 'Calle 456', '654987321', 'luisagarcia@gmail.com')
]

conn.executemany('INSERT INTO clientes (nombre, direccion, telefono, correo) VALUES (?, ?, ?, ?)', clientes)

# Insertar datos de ejemplo en la tabla 'productos'
productos = [
    ('Paracetamol', 5.99, 100),
    ('Ibuprofeno', 7.5, 50),
    ('Amoxicilina', 12.99, 20),
    ('Vitamina C', 9.75, 80),
    ('Aspirina', 3.99, 60)
]

conn.executemany('INSERT INTO productos (nombre, precio, stock) VALUES (?, ?, ?)', productos)

# Guardar los cambios
conn.commit()

# Cerrar la conexión a la base de datos
conn.close()

