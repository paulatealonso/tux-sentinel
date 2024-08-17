import os
import re
import asyncio
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes
from dotenv import load_dotenv
from telegram.error import RetryAfter

# Cargar las variables de entorno
load_dotenv()

TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')

# Almacenamiento en memoria (puedes cambiarlo por una base de datos si es necesario)
secciones = {
    "Linux": [],
    "Hacking": [],
    "Ciberseguridad": [],
    "Malware": []
}

nueva_seccion = ""
contexto_actual = ""

# Función para manejar el comando /menu
async def menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("🐧 Linux", callback_data='menu_linux')],
        [InlineKeyboardButton("💻 Hacking", callback_data='menu_hacking')],
        [InlineKeyboardButton("🔒 Ciberseguridad", callback_data='menu_ciberseguridad')],
        [InlineKeyboardButton("🦠 Malware", callback_data='menu_malware')],
        [InlineKeyboardButton("➕ Crear Sección", callback_data='crear_seccion')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    if update.message:
        await update.message.reply_text(
            "👋 ¡Bienvenido a **TuxSentinel**!\n\n"
            "Selecciona una categoría para explorar contenido detallado o crear una nueva sección:",
            reply_markup=reply_markup
        )
    elif update.callback_query:
        await update.callback_query.message.edit_text(
            "👋 ¡Bienvenido de nuevo a **TuxSentinel**!\n\n"
            "Selecciona una categoría para explorar contenido detallado o crear una nueva sección:",
            reply_markup=reply_markup
        )

# Función para manejar las selecciones del menú principal
async def menu_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    global contexto_actual
    contexto_actual = query.data

    if query.data == 'menu_linux':
        keyboard = [
            [InlineKeyboardButton("🌍 Distribuciones", callback_data='linux_distribuciones')],
            [InlineKeyboardButton("💻 Comandos Básicos", callback_data='linux_comandos')],
            [InlineKeyboardButton("🛠️ Instalación", callback_data='linux_instalacion')],
            [InlineKeyboardButton("✏️ Crear Artículo", callback_data='crear_articulo')],
            [InlineKeyboardButton("🔙 Volver", callback_data='back_to_menu')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(
            text="🐧 **Linux - Elige una opción para obtener más información o crear un artículo:**",
            reply_markup=reply_markup
        )
    elif query.data == 'menu_hacking':
        keyboard = [
            [InlineKeyboardButton("🔓 Ethical Hacking", callback_data='hacking_ethical')],
            [InlineKeyboardButton("🛠️ Herramientas", callback_data='hacking_herramientas')],
            [InlineKeyboardButton("🎯 Técnicas", callback_data='hacking_tecnicas')],
            [InlineKeyboardButton("✏️ Crear Artículo", callback_data='crear_articulo')],
            [InlineKeyboardButton("🔙 Volver", callback_data='back_to_menu')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(
            text="💻 **Hacking - Elige una opción para obtener más información o crear un artículo:**",
            reply_markup=reply_markup
        )
    elif query.data == 'menu_ciberseguridad':
        keyboard = [
            [InlineKeyboardButton("📘 Conceptos Básicos", callback_data='ciberseguridad_conceptos')],
            [InlineKeyboardButton("🔵 Blue Team", callback_data='ciberseguridad_blue_team')],
            [InlineKeyboardButton("🔴 Red Team", callback_data='ciberseguridad_red_team')],
            [InlineKeyboardButton("✏️ Crear Artículo", callback_data='crear_articulo')],
            [InlineKeyboardButton("🔙 Volver", callback_data='back_to_menu')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(
            text="🔒 **Ciberseguridad - Elige una opción para obtener más información o crear un artículo:**",
            reply_markup=reply_markup
        )
    elif query.data == 'menu_malware':
        keyboard = [
            [InlineKeyboardButton("🦠 Tipos de Malware", callback_data='malware_tipos')],
            [InlineKeyboardButton("🛡️ Protección", callback_data='malware_proteccion')],
            [InlineKeyboardButton("📜 Casos Famosos", callback_data='malware_casos')],
            [InlineKeyboardButton("✏️ Crear Artículo", callback_data='crear_articulo')],
            [InlineKeyboardButton("🔙 Volver", callback_data='back_to_menu')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(
            text="🦠 **Malware - Elige una opción para obtener más información o crear un artículo:**",
            reply_markup=reply_markup
        )
    elif query.data == 'crear_seccion':
        await query.edit_message_text(
            text="➕ **Crear Nueva Sección**:\n\n"
                 "Por favor, envía el título de la nueva sección (máximo 100 caracteres)."
        )
    elif query.data == 'back_to_menu':
        await menu(update, context)

# Función para manejar la creación de artículos y secciones
async def manejar_mensajes(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global contexto_actual, nueva_seccion

    if contexto_actual == 'crear_articulo':
        # Verificar que no contiene enlaces para evitar spam
        if re.search(r'http[s]?://', update.message.text):
            await update.message.reply_text(
                "❌ El artículo no puede contener enlaces. Por favor, envía un artículo válido."
            )
        else:
            secciones[nueva_seccion].append(update.message.text)
            await update.message.reply_text(
                "✅ ¡Artículo subido con éxito a la sección **{}**!".format(nueva_seccion)
            )
            contexto_actual = ""

    elif contexto_actual == 'crear_seccion':
        nueva_seccion = update.message.text.strip()
        if len(nueva_seccion) > 100:
            await update.message.reply_text(
                "❌ El título de la sección no puede exceder los 100 caracteres. Por favor, intenta de nuevo."
            )
        else:
            secciones[nueva_seccion] = []
            await update.message.reply_text(
                "✅ ¡Sección **{}** creada con éxito! Ahora puedes crear artículos.".format(nueva_seccion),
                reply_markup=InlineKeyboardMarkup([
                    [InlineKeyboardButton("✏️ Crear Artículo", callback_data='crear_articulo')],
                    [InlineKeyboardButton("🔙 Volver", callback_data='back_to_menu')]
                ])
            )
            contexto_actual = ""

# Función para manejar las selecciones del submenú
async def submenu_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    try:
        if query.data == 'linux_distribuciones':
            await query.edit_message_text(
                text="🌍 **Distribuciones de Linux**:\n\n"
                     "🔸 `Ubuntu`: Ideal para principiantes, con una gran comunidad y soporte extenso.\n"
                     "🔸 `Fedora`: Famosa por estar a la vanguardia en software de código abierto.\n"
                     "🔸 `Debian`: Base de muchas otras distribuciones, conocida por su estabilidad.\n"
                     "🔸 `Arch Linux`: Para usuarios avanzados, te permite construir tu sistema desde cero.\n"
                     "🔸 `Red Hat Enterprise Linux`: Utilizado en entornos empresariales, robusto y con soporte oficial.\n"
                     "🔸 `CentOS`: Versión gratuita de Red Hat, popular en servidores.\n\n"
                     "Cada distribución tiene un enfoque y propósito distinto. ¡Explora y encuentra la tuya!",
                reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Volver", callback_data='menu_linux')]])
            )
        elif query.data == 'linux_comandos':
            await query.edit_message_text(
                text="💻 **Comandos Básicos de Linux**:\n\n"
                     "Aquí tienes algunos comandos esenciales para empezar:\n"
                     "🔹 `ls`: Listar archivos y directorios en el directorio actual.\n"
                     "🔹 `cd [directorio]`: Cambiar el directorio de trabajo.\n"
                     "🔹 `mkdir [nombre]`: Crear un nuevo directorio.\n"
                     "🔹 `rm [archivo]`: Eliminar un archivo (usa `rm -r` para eliminar directorios).\n"
                     "🔹 `cp [origen] [destino]`: Copiar archivos o directorios.\n"
                     "🔹 `mv [origen] [destino]`: Mover o renombrar archivos o directorios.\n"
                     "🔹 `chmod [permisos] [archivo]`: Cambiar los permisos de un archivo o directorio.\n"
                     "🔹 `ps`: Listar los procesos en ejecución.\n\n"
                     "Con estos comandos, ¡dominarás lo básico de la terminal en poco tiempo!",
                reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Volver", callback_data='menu_linux')]])
            )
        elif query.data == 'linux_instalacion':
            await query.edit_message_text(
                text="🛠️ **Instalación de Linux**:\n\n"
                     "Pasos básicos para instalar una distribución de Linux:\n"
                     "1️⃣ **Descarga la ISO**: Visita la web oficial de la distribución y descarga la imagen ISO.\n"
                     "2️⃣ **Crea un USB booteable**: Usa herramientas como Rufus o Etcher para crear un USB booteable.\n"
                     "3️⃣ **Inicia desde el USB**: Configura la BIOS para arrancar desde el USB.\n"
                     "4️⃣ **Instala Linux**: Sigue las instrucciones del instalador. Puedes elegir entre instalar junto a otro sistema operativo o utilizar todo el disco.\n"
                     "5️⃣ **Configura tu sistema**: Después de la instalación, configura el sistema según tus necesidades.\n\n"
                     "¡Ya estarás listo para disfrutar de la libertad que ofrece Linux!",
                reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Volver", callback_data='menu_linux')]])
            )
        elif query.data == 'crear_articulo':
            await query.edit_message_text(
                text="✏️ **Crear Artículo**:\n\n"
                     "Por favor, envía el contenido del artículo que deseas agregar a la sección **{}**.".format(contexto_actual)
            )

        # Sección Hacking
        elif query.data == 'hacking_ethical':
            await query.edit_message_text(
                text="🔓 **Ethical Hacking**:\n\n"
                     "El ethical hacking, o hacking ético, se refiere al proceso de penetrar en sistemas informáticos "
                     "de forma legal y autorizada, con el objetivo de identificar vulnerabilidades antes de que los "
                     "atacantes malintencionados lo hagan.\n\n"
                     "🔍 **Objetivos del Ethical Hacking**:\n"
                     "- Identificar debilidades en la infraestructura.\n"
                     "- Evaluar la efectividad de las medidas de seguridad actuales.\n"
                     "- Recomendar soluciones para mejorar la seguridad.\n\n"
                     "🔧 **Herramientas Comunes**:\n"
                     "- Metasploit\n"
                     "- Nmap\n"
                     "- Wireshark\n"
                     "- Burp Suite\n\n"
                     "El hacking ético es una parte fundamental de la ciberseguridad moderna.",
                reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Volver", callback_data='menu_hacking')]])
            )
        elif query.data == 'hacking_herramientas':
            await query.edit_message_text(
                text="🛠️ **Herramientas de Hacking**:\n\n"
                     "Aquí tienes algunas de las herramientas más populares en el ámbito del hacking y la seguridad informática:\n"
                     "🔹 **Metasploit**: Un framework para desarrollar y ejecutar exploits contra una máquina remota.\n"
                     "🔹 **Nmap**: Herramienta para exploración de redes y auditoría de seguridad.\n"
                     "🔹 **Wireshark**: Analizador de protocolos de red que te permite capturar y explorar datos en tiempo real.\n"
                     "🔹 **John the Ripper**: Herramienta para crackeo de contraseñas.\n"
                     "🔹 **Burp Suite**: Plataforma para pruebas de seguridad de aplicaciones web.\n"
                     "🔹 **Aircrack-ng**: Conjunto de herramientas para evaluar la seguridad de redes WiFi.\n\n"
                     "Estas herramientas son usadas tanto por profesionales de la seguridad como por hackers éticos.",
                reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Volver", callback_data='menu_hacking')]])
            )
        elif query.data == 'hacking_tecnicas':
            await query.edit_message_text(
                text="🎯 **Técnicas de Hacking**:\n\n"
                     "Aquí tienes un vistazo a algunas técnicas comunes de hacking:\n"
                     "🔸 **Phishing**: Engañar a las personas para que revelen información confidencial.\n"
                     "🔸 **SQL Injection**: Inserción de código malicioso en consultas SQL para manipular bases de datos.\n"
                     "🔸 **Cross-Site Scripting (XSS)**: Inyección de scripts en páginas web vistas por otros usuarios.\n"
                     "🔸 **Ataque de Fuerza Bruta**: Probar combinaciones de contraseñas hasta encontrar la correcta.\n"
                     "🔸 **Man-in-the-Middle (MitM)**: Interceptar y alterar la comunicación entre dos partes.\n\n"
                     "Conocer estas técnicas es clave para defenderse y mitigar posibles ataques.",
                reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Volver", callback_data='menu_hacking')]])
            )

        elif query.data == 'crear_articulo':
            await query.edit_message_text(
                text="✏️ **Crear Artículo**:\n\n"
                     "Por favor, envía el contenido del artículo que deseas agregar a la sección **{}**.".format(contexto_actual)
            )

        # Sección Ciberseguridad
        elif query.data == 'ciberseguridad_conceptos':
            await query.edit_message_text(
                text="📘 **Conceptos Básicos de Ciberseguridad**:\n\n"
                     "🔒 **Confidencialidad**: Asegurar que la información solo sea accesible por personas autorizadas.\n"
                     "🔒 **Integridad**: Garantizar que la información no sea alterada sin autorización.\n"
                     "🔒 **Disponibilidad**: Asegurar que los sistemas y datos estén disponibles para su uso cuando se necesiten.\n"
                     "🔒 **Autenticación**: Verificación de la identidad de usuarios, dispositivos o sistemas.\n"
                     "🔒 **Autorización**: Control de acceso para asegurar que los usuarios solo tengan acceso a los recursos necesarios.\n\n"
                     "Estos son los pilares fundamentales sobre los que se construye la seguridad en la información.",
                reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Volver", callback_data='menu_ciberseguridad')]])
            )
        elif query.data == 'ciberseguridad_blue_team':
            await query.edit_message_text(
                text="🔵 **Blue Team**:\n\n"
                     "El Blue Team es el equipo responsable de defender y proteger la infraestructura de TI "
                     "de una organización contra ataques y amenazas cibernéticas. Su objetivo principal es "
                     "garantizar la seguridad operativa y responder rápidamente a cualquier incidente.\n\n"
                     "📚 **Certificaciones para Blue Team**:\n"
                     "- *Para Principiantes*:\n"
                     "  - **CompTIA Security+**: Introducción a los conceptos de seguridad.\n"
                     "  - **Certified Ethical Hacker (CEH)**: Funda tu conocimiento en técnicas de defensa.\n"
                     "- *Para Profesionales*:\n"
                     "  - **Certified Information Systems Security Professional (CISSP)**: Certificación avanzada para gestores de seguridad.\n"
                     "  - **GIAC Certified Incident Handler (GCIH)**: Especialización en respuesta a incidentes y manejo de amenazas.\n\n"
                     "Los miembros del Blue Team trabajan incansablemente para mantener la seguridad y estabilidad de la organización.",
                reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Volver", callback_data='menu_ciberseguridad')]])
            )
        elif query.data == 'ciberseguridad_red_team':
            await query.edit_message_text(
                text="🔴 **Red Team**:\n\n"
                     "El Red Team se especializa en simular ataques reales para probar las defensas de una organización. "
                     "Su objetivo es identificar vulnerabilidades que puedan ser explotadas por adversarios y ayudar al "
                     "Blue Team a fortalecer la seguridad.\n\n"
                     "📚 **Certificaciones para Red Team**:\n"
                     "- *Para Principiantes*:\n"
                     "  - **CompTIA PenTest+**: Introducción al testing de penetración.\n"
                     "  - **eLearnSecurity Junior Penetration Tester (eJPT)**: Certificación inicial en pruebas de penetración.\n"
                     "- *Para Profesionales*:\n"
                     "  - **Offensive Security Certified Professional (OSCP)**: Certificación rigurosa en pruebas de penetración.\n"
                     "  - **GIAC Penetration Tester (GPEN)**: Enfoque avanzado en técnicas de penetración y explotación.\n\n"
                     "El Red Team juega un papel crucial al exponer puntos débiles y mejorar las defensas de la organización.",
                reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Volver", callback_data='menu_ciberseguridad')]])
            )

        elif query.data == 'crear_articulo':
            await query.edit_message_text(
                text="✏️ **Crear Artículo**:\n\n"
                     "Por favor, envía el contenido del artículo que deseas agregar a la sección **{}**.".format(contexto_actual)
            )

        # Sección Malware
        elif query.data == 'malware_tipos':
            await query.edit_message_text(
                text="🦠 **Tipos de Malware**:\n\n"
                     "🔹 **Virus**: Se adjunta a archivos legítimos y se propaga al ejecutarlos.\n"
                     "🔹 **Troyanos**: Se disfrazan de software legítimo pero realizan actividades maliciosas en segundo plano.\n"
                     "🔹 **Ransomware**: Encripta los archivos del sistema y exige un rescate para liberarlos.\n"
                     "🔹 **Spyware**: Monitorea las actividades del usuario y roba información sin su conocimiento.\n"
                     "🔹 **Adware**: Muestra anuncios no deseados y a veces recolecta datos del usuario.\n"
                     "🔹 **Worms**: Se replica a sí mismo para propagarse a otros sistemas sin intervención del usuario.\n\n"
                     "Conocer estos tipos de malware es crucial para poder detectarlos y eliminarlos a tiempo.",
                reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Volver", callback_data='menu_malware')]])
            )
        elif query.data == 'malware_proteccion':
            await query.edit_message_text(
                text="🛡️ **Protección Contra Malware**:\n\n"
                     "🔐 **Usa software antivirus**: Mantén tu antivirus actualizado para detectar y eliminar amenazas.\n"
                     "🔐 **Actualiza tu sistema operativo**: Las actualizaciones suelen incluir parches de seguridad importantes.\n"
                     "🔐 **No abras archivos sospechosos**: Si no conoces el origen de un archivo, es mejor no abrirlo.\n"
                     "🔐 **Evita hacer clic en enlaces desconocidos**: Podrían llevar a sitios maliciosos.\n"
                     "🔐 **Realiza copias de seguridad regularmente**: Así podrás restaurar tu sistema en caso de infección.\n\n"
                     "Estas prácticas son esenciales para protegerte contra la mayoría de los ataques de malware.",
                reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Volver", callback_data='menu_malware')]])
            )
        elif query.data == 'malware_casos':
            await query.edit_message_text(
                text="📜 **Casos Famosos de Malware**:\n\n"
                     "🔸 **ILOVEYOU (2000)**: Este gusano de correo electrónico afectó a millones de computadoras en todo el mundo.\n"
                     "🔸 **WannaCry (2017)**: Ransomware que explotó una vulnerabilidad de Windows, causando estragos en miles de sistemas.\n"
                     "🔸 **Stuxnet (2010)**: Malware dirigido a sistemas industriales, utilizado para sabotear el programa nuclear de Irán.\n"
                     "🔸 **Zeus (2007)**: Troyano bancario que robó millones de dólares de cuentas en línea.\n"
                     "🔸 **CryptoLocker (2013)**: Uno de los primeros ransomware modernos que encriptó archivos y exigió un pago en Bitcoin.\n\n"
                     "Estos casos subrayan la importancia de estar siempre vigilante y preparado.",
                reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Volver", callback_data='menu_malware')]])
            )

        elif query.data == 'crear_articulo':
            await query.edit_message_text(
                text="✏️ **Crear Artículo**:\n\n"
                     "Por favor, envía el contenido del artículo que deseas agregar a la sección **{}**.".format(contexto_actual)
            )

    except RetryAfter as e:
        await asyncio.sleep(e.retry_after)
        await submenu_callback(update, context)

def main():
    application = ApplicationBuilder().token(TOKEN).build()

    application.add_handler(CommandHandler("menu", menu))
    application.add_handler(CallbackQueryHandler(menu_callback, pattern='menu_'))
    application.add_handler(CallbackQueryHandler(submenu_callback, pattern='linux_'))
    application.add_handler(CallbackQueryHandler(submenu_callback, pattern='hacking_'))
    application.add_handler(CallbackQueryHandler(submenu_callback, pattern='ciberseguridad_'))
    application.add_handler(CallbackQueryHandler(submenu_callback, pattern='malware_'))
    application.add_handler(CallbackQueryHandler(menu_callback, pattern='back_to_menu'))

    # Manejador para mensajes de texto (creación de artículos y secciones)
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, manejar_mensajes))

    application.run_polling()

if __name__ == '__main__':
    main()
