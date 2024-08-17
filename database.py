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
            FOREIGN KEY (seccion_id) REFERENCES secciones (id)
        )
    ''')

    conn.commit()

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
    cursor.execute("SELECT titulo FROM articulos WHERE seccion_id = (SELECT id FROM secciones WHERE nombre = ?)", (seccion,))
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
        "INSERT INTO articulos (seccion_id, titulo, contenido) VALUES ((SELECT id FROM secciones WHERE nombre = ?), ?, ?)",
        (seccion, titulo, contenido)
    )
    conn.commit()
    conn.close()

def init_db():
    conn = sqlite3.connect('tuxsentinel.db')
    crear_tablas(conn)
    insertar_datos_iniciales(conn)
    conn.close()
