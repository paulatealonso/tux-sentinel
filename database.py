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
        "🐧 Linux": [
            ("🌍 Distribuciones", "🌍 **Distribuciones de Linux**:\n\n🔸 `Ubuntu`: Ideal para principiantes, con una gran comunidad y soporte extenso.\n🔸 `Fedora`: Famosa por estar a la vanguardia en software de código abierto.\n🔸 `Debian`: Base de muchas otras distribuciones, conocida por su estabilidad.\n🔸 `Arch Linux`: Para usuarios avanzados, te permite construir tu sistema desde cero.\n🔸 `Red Hat Enterprise Linux`: Utilizado en entornos empresariales, robusto y con soporte oficial.\n🔸 `CentOS`: Versión gratuita de Red Hat, popular en servidores.\n\nCada distribución tiene un enfoque y propósito distinto. ¡Explora y encuentra la tuya!"),
            ("💻 Comandos Básicos", "💻 **Comandos Básicos de Linux**:\n\n🔹 `ls`: Listar archivos y directorios en el directorio actual.\n🔹 `cd [directorio]`: Cambiar el directorio de trabajo.\n🔹 `mkdir [nombre]`: Crear un nuevo directorio.\n🔹 `rm [archivo]`: Eliminar un archivo (usa `rm -r` para eliminar directorios).\n🔹 `cp [origen] [destino]`: Copiar archivos o directorios.\n🔹 `mv [origen] [destino]`: Mover o renombrar archivos o directorios.\n🔹 `chmod [permisos] [archivo]`: Cambiar los permisos de un archivo o directorio.\n🔹 `ps`: Listar los procesos en ejecución.\n\nCon estos comandos, ¡dominarás lo básico de la terminal en poco tiempo!"),
            ("🛠️ Instalación", "🛠️ **Instalación de Linux**:\n\n1️⃣ **Descarga la ISO**: Visita la web oficial de la distribución y descarga la imagen ISO.\n2️⃣ **Crea un USB booteable**: Usa herramientas como Rufus o Etcher para crear un USB booteable.\n3️⃣ **Inicia desde el USB**: Configura la BIOS para arrancar desde el USB.\n4️⃣ **Instala Linux**: Sigue las instrucciones del instalador.\n5️⃣ **Configura tu sistema**: Después de la instalación, configura el sistema según tus necesidades.\n\n¡Ya estarás listo para disfrutar de la libertad que ofrece Linux!")
        ],
        "💻 Hacking": [
            ("🔓 Ethical Hacking", "🔓 **Ethical Hacking**:\n\nEl ethical hacking, o hacking ético, se refiere al proceso de penetrar en sistemas informáticos de forma legal y autorizada, con el objetivo de identificar vulnerabilidades antes de que los atacantes malintencionados lo hagan.\n\n🔍 **Objetivos del Ethical Hacking**:\n- Identificar debilidades en la infraestructura.\n- Evaluar la efectividad de las medidas de seguridad actuales.\n- Recomendar soluciones para mejorar la seguridad.\n\n🔧 **Herramientas Comunes**:\n- Metasploit\n- Nmap\n- Wireshark\n- Burp Suite"),
            ("🛠️ Herramientas", "🛠️ **Herramientas de Hacking**:\n\n🔹 **Metasploit**: Un framework para desarrollar y ejecutar exploits contra una máquina remota.\n🔹 **Nmap**: Herramienta para exploración de redes y auditoría de seguridad.\n🔹 **Wireshark**: Analizador de protocolos de red que te permite capturar y explorar datos en tiempo real.\n🔹 **John the Ripper**: Herramienta para crackeo de contraseñas.\n🔹 **Burp Suite**: Plataforma para pruebas de seguridad de aplicaciones web.\n🔹 **Aircrack-ng**: Conjunto de herramientas para evaluar la seguridad de redes WiFi."),
            ("🎯 Técnicas", "🎯 **Técnicas de Hacking**:\n\n🔸 **Phishing**: Engañar a las personas para que revelen información confidencial.\n🔸 **SQL Injection**: Inserción de código malicioso en consultas SQL para manipular bases de datos.\n🔸 **Cross-Site Scripting (XSS)**: Inyección de scripts en páginas web vistas por otros usuarios.\n🔸 **Ataque de Fuerza Bruta**: Probar combinaciones de contraseñas hasta encontrar la correcta.\n🔸 **Man-in-the-Middle (MitM)**: Interceptar y alterar la comunicación entre dos partes.")
        ],
        "🔒 Ciberseguridad": [
            ("📘 Conceptos Básicos", "📘 **Conceptos Básicos de Ciberseguridad**:\n\n🔒 **Confidencialidad**: Asegurar que la información solo sea accesible por personas autorizadas.\n🔒 **Integridad**: Garantizar que la información no sea alterada sin autorización.\n🔒 **Disponibilidad**: Asegurar que los sistemas y datos estén disponibles para su uso cuando se necesiten.\n🔒 **Autenticación**: Verificación de la identidad de usuarios, dispositivos o sistemas.\n🔒 **Autorización**: Control de acceso para asegurar que los usuarios solo tengan acceso a los recursos necesarios."),
            ("🔵 Blue Team", "🔵 **Blue Team**:\n\nEl Blue Team es el equipo responsable de defender y proteger la infraestructura de TI de una organización contra ataques y amenazas cibernéticas. Su objetivo principal es garantizar la seguridad operativa y responder rápidamente a cualquier incidente.\n\n📚 **Certificaciones para Blue Team**:\n- **CompTIA Security+**\n- **Certified Ethical Hacker (CEH)**\n- **Certified Information Systems Security Professional (CISSP)**\n- **GIAC Certified Incident Handler (GCIH)**"),
            ("🔴 Red Team", "🔴 **Red Team**:\n\nEl Red Team se especializa en simular ataques reales para probar las defensas de una organización. Su objetivo es identificar vulnerabilidades que puedan ser explotadas por adversarios y ayudar al Blue Team a fortalecer la seguridad.\n\n📚 **Certificaciones para Red Team**:\n- **CompTIA PenTest+**\n- **eLearnSecurity Junior Penetration Tester (eJPT)**\n- **Offensive Security Certified Professional (OSCP)**\n- **GIAC Penetration Tester (GPEN)**")
        ],
        "🦠 Malware": [
            ("🦠 Tipos de Malware", "🦠 **Tipos de Malware**:\n\n🔹 **Virus**: Se adjunta a archivos legítimos y se propaga al ejecutarlos.\n🔹 **Troyanos**: Se disfrazan de software legítimo pero realizan actividades maliciosas en segundo plano.\n🔹 **Ransomware**: Encripta los archivos del sistema y exige un rescate para liberarlos.\n🔹 **Spyware**: Monitorea las actividades del usuario y roba información sin su conocimiento.\n🔹 **Adware**: Muestra anuncios no deseados y a veces recolecta datos del usuario.\n🔹 **Worms**: Se replica a sí mismo para propagarse a otros sistemas sin intervención del usuario."),
            ("🛡️ Protección", "🛡️ **Protección Contra Malware**:\n\n🔐 **Usa software antivirus**: Mantén tu antivirus actualizado para detectar y eliminar amenazas.\n🔐 **Actualiza tu sistema operativo**: Las actualizaciones suelen incluir parches de seguridad importantes.\n🔐 **No abras archivos sospechosos**: Si no conoces el origen de un archivo, es mejor no abrirlo.\n🔐 **Evita hacer clic en enlaces desconocidos**: Podrían llevar a sitios maliciosos.\n🔐 **Realiza copias de seguridad regularmente**: Así podrás restaurar tu sistema en caso de infección."),
            ("📜 Casos Famosos", "📜 **Casos Famosos de Malware**:\n\n🔸 **ILOVEYOU (2000)**: Este gusano de correo electrónico afectó a millones de computadoras en todo el mundo.\n🔸 **WannaCry (2017)**: Ransomware que explotó una vulnerabilidad de Windows, causando estragos en miles de sistemas.\n🔸 **Stuxnet (2010)**: Malware dirigido a sistemas industriales, utilizado para sabotear el programa nuclear de Irán.\n🔸 **Zeus (2007)**: Troyano bancario que robó millones de dólares de cuentas en línea.\n🔸 **CryptoLocker (2013)**: Uno de los primeros ransomware modernos que encriptó archivos y exigió un pago en Bitcoin.")
        ]
    }

    for seccion, articulos in secciones_articulos.items():
        cursor.execute("INSERT OR IGNORE INTO secciones (nombre) VALUES (?)", (seccion,))
        seccion_id = cursor.lastrowid if cursor.lastrowid != 0 else cursor.execute("SELECT id FROM secciones WHERE nombre = ?", (seccion,)).fetchone()[0]
        for titulo, contenido in articulos:
            cursor.execute("INSERT OR IGNORE INTO articulos (seccion_id, titulo, contenido) VALUES (?, ?, ?)", (seccion_id, titulo, contenido))

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
    contenido = cursor.fetchone()[0]
    conn.close()
    return contenido

def init_db():
    conn = sqlite3.connect('tuxsentinel.db')
    crear_tablas(conn)
    insertar_datos_iniciales(conn)
    conn.close()
