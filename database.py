import sqlite3

def crear_tablas(conn):
    cursor = conn.cursor()
    
    # Crear tabla secciones
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS secciones (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT UNIQUE NOT NULL
        )
    ''')
    
    # Crear tabla articulos
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS articulos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            seccion_id INTEGER NOT NULL,
            titulo TEXT UNIQUE NOT NULL,
            contenido TEXT NOT NULL,
            aprobado INTEGER DEFAULT 0,
            FOREIGN KEY (seccion_id) REFERENCES secciones (id)
        )
    ''')

    conn.commit()

def agregar_columna_aprobado():
    conn = sqlite3.connect('tuxsentinel.db')
    cursor = conn.cursor()

    # Comprobar si la columna 'aprobado' ya existe
    cursor.execute("PRAGMA table_info(articulos)")
    columnas = [info[1] for info in cursor.fetchall()]
    if 'aprobado' not in columnas:
        cursor.execute("ALTER TABLE articulos ADD COLUMN aprobado INTEGER DEFAULT 0")
        conn.commit()
        print("Columna 'aprobado' agregada correctamente.")

    conn.close()

def insertar_datos_iniciales(conn):
    cursor = conn.cursor()

    secciones_articulos = {
        "🐧 Linux": [],
        "💻 Hacking": [],
        "🔒 Ciberseguridad": [],
        "🦠 Malware": []
    }

    for seccion in secciones_articulos.keys():
        cursor.execute("INSERT OR IGNORE INTO secciones (nombre) VALUES (?)", (seccion,))

    conn.commit()

def obtener_secciones():
    conn = sqlite3.connect('tuxsentinel.db')
    cursor = conn.cursor()
    cursor.execute("SELECT nombre FROM secciones")
    secciones = [row[0] for row in cursor.fetchall()]
    conn.close()
    return secciones

def obtener_articulos(seccion):
    conn = sqlite3.connect('tuxsentinel.db')
    cursor = conn.cursor()
    cursor.execute("SELECT titulo FROM articulos WHERE seccion_id = (SELECT id FROM secciones WHERE nombre = ?) AND aprobado = 1", (seccion,))
    articulos = [row[0] for row in cursor.fetchall()]
    conn.close()
    return articulos

def obtener_contenido_articulo(seccion, titulo):
    conn = sqlite3.connect('tuxsentinel.db')
    cursor = conn.cursor()
    cursor.execute("SELECT contenido FROM articulos WHERE seccion_id = (SELECT id FROM secciones WHERE nombre = ?) AND titulo = ?", (seccion, titulo))
    contenido = cursor.fetchone()
    conn.close()
    return contenido[0] if contenido else None

def agregar_articulo(seccion, titulo, contenido):
    conn = sqlite3.connect('tuxsentinel.db')
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO articulos (seccion_id, titulo, contenido, aprobado) VALUES ((SELECT id FROM secciones WHERE nombre = ?), ?, ?, 0)",
        (seccion, titulo, contenido)
    )
    conn.commit()
    conn.close()

def obtener_articulos_pendientes():
    conn = sqlite3.connect('tuxsentinel.db')
    cursor = conn.cursor()
    cursor.execute("SELECT id, seccion_id, titulo, contenido FROM articulos WHERE aprobado = 0")
    articulos = cursor.fetchall()
    conn.close()
    return articulos

def aprobar_articulo(articulo_id):
    conn = sqlite3.connect('tuxsentinel.db')
    cursor = conn.cursor()
    cursor.execute("UPDATE articulos SET aprobado = 1 WHERE id = ?", (articulo_id,))
    conn.commit()
    conn.close()

def eliminar_articulo(articulo_id):
    conn = sqlite3.connect('tuxsentinel.db')
    cursor = conn.cursor()
    cursor.execute("DELETE FROM articulos WHERE id = ?", (articulo_id,))
    conn.commit()
    conn.close()

def init_db():
    conn = sqlite3.connect('tuxsentinel.db')
    crear_tablas(conn)
    agregar_columna_aprobado()  # Esta llamada sólo agrega la columna si es necesario
    insertar_datos_iniciales(conn)
    conn.close()
