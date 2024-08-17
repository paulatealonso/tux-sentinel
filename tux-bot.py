import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes
from dotenv import load_dotenv

# Cargar las variables de entorno
load_dotenv()

# Aquí cargamos el token de nuestro bot desde el archivo .env
TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')

# Comando /menu para mostrar el menú principal
async def menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("🐧 Linux", callback_data='menu_linux')],
        [InlineKeyboardButton("💻 Hacking", callback_data='menu_hacking')],
        [InlineKeyboardButton("🔒 Ciberseguridad", callback_data='menu_ciberseguridad')],
        [InlineKeyboardButton("🦠 Malware", callback_data='menu_malware')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    # Si se activa desde /menu o desde un botón "Volver", respondemos según corresponda
    if update.message:
        await update.message.reply_text(
            "👋 ¡Bienvenido a **TuxSentinel**!\n\n"
            "Selecciona una categoría para explorar contenido detallado:",
            reply_markup=reply_markup
        )
    elif update.callback_query:
        await update.callback_query.message.edit_text(
            "👋 ¡Bienvenido de nuevo a **TuxSentinel**!\n\n"
            "Selecciona una categoría para explorar contenido detallado:",
            reply_markup=reply_markup
        )

# Función para manejar las selecciones del menú principal
async def menu_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == 'menu_linux':
        keyboard = [
            [InlineKeyboardButton("🌍 Distribuciones", callback_data='linux_distribuciones')],
            [InlineKeyboardButton("💻 Comandos Básicos", callback_data='linux_comandos')],
            [InlineKeyboardButton("🛠️ Instalación", callback_data='linux_instalacion')],
            [InlineKeyboardButton("🔙 Volver", callback_data='back_to_menu')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(
            text="🐧 **Linux - Elige una opción para obtener más información:**",
            reply_markup=reply_markup
        )
    elif query.data == 'menu_hacking':
        keyboard = [
            [InlineKeyboardButton("🔓 Ethical Hacking", callback_data='hacking_ethical')],
            [InlineKeyboardButton("🛠️ Herramientas", callback_data='hacking_herramientas')],
            [InlineKeyboardButton("🎯 Técnicas", callback_data='hacking_tecnicas')],
            [InlineKeyboardButton("🔙 Volver", callback_data='back_to_menu')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(
            text="💻 **Hacking - Elige una opción para obtener más información:**",
            reply_markup=reply_markup
        )
    elif query.data == 'menu_ciberseguridad':
        keyboard = [
            [InlineKeyboardButton("📘 Conceptos Básicos", callback_data='ciberseguridad_conceptos')],
            [InlineKeyboardButton("✅ Buenas Prácticas", callback_data='ciberseguridad_practicas')],
            [InlineKeyboardButton("📰 Noticias Recientes", callback_data='ciberseguridad_noticias')],
            [InlineKeyboardButton("🔙 Volver", callback_data='back_to_menu')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(
            text="🔒 **Ciberseguridad - Elige una opción para obtener más información:**",
            reply_markup=reply_markup
        )
    elif query.data == 'menu_malware':
        keyboard = [
            [InlineKeyboardButton("🦠 Tipos de Malware", callback_data='malware_tipos')],
            [InlineKeyboardButton("🛡️ Protección", callback_data='malware_proteccion')],
            [InlineKeyboardButton("📜 Casos Famosos", callback_data='malware_casos')],
            [InlineKeyboardButton("🔙 Volver", callback_data='back_to_menu')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(
            text="🦠 **Malware - Elige una opción para obtener más información:**",
            reply_markup=reply_markup
        )
    elif query.data == 'back_to_menu':
        await menu(update, context)

# Función para manejar las selecciones del submenú
async def submenu_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    # Sección Linux
    if query.data == 'linux_distribuciones':
        await query.edit_message_text(
            text="🌍 **Distribuciones de Linux**:\n\n"
                 "🔸 **Ubuntu**: Ideal para principiantes, con una gran comunidad y soporte extenso.\n"
                 "🔸 **Fedora**: Famosa por estar a la vanguardia en software de código abierto.\n"
                 "🔸 **Debian**: Base de muchas otras distribuciones, conocida por su estabilidad.\n"
                 "🔸 **Arch Linux**: Para usuarios avanzados, te permite construir tu sistema desde cero.\n"
                 "🔸 **Red Hat Enterprise Linux**: Utilizado en entornos empresariales, robusto y con soporte oficial.\n"
                 "🔸 **CentOS**: Versión gratuita de Red Hat, popular en servidores.\n\n"
                 "Cada distribución tiene un enfoque y propósito distinto. ¡Explora y encuentra la tuya!"
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
                 "Con estos comandos, ¡dominarás lo básico de la terminal en poco tiempo!"
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
                 "¡Ya estarás listo para disfrutar de la libertad que ofrece Linux!"
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
                 "El hacking ético es una parte fundamental de la ciberseguridad moderna."
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
                 "Estas herramientas son usadas tanto por profesionales de la seguridad como por hackers éticos."
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
                 "Conocer estas técnicas es clave para defenderse y mitigar posibles ataques."
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
                 "Estos son los pilares fundamentales sobre los que se construye la seguridad en la información."
        )
    elif query.data == 'ciberseguridad_practicas':
        await query.edit_message_text(
            text="✅ **Buenas Prácticas en Ciberseguridad**:\n\n"
                 "🔑 **Usa contraseñas fuertes**: Combina letras, números y símbolos, y cámbialas regularmente.\n"
                 "🔑 **Habilita la autenticación de dos factores (2FA)**: Añade una capa extra de seguridad a tus cuentas.\n"
                 "🔑 **Mantén el software actualizado**: Instala las actualizaciones de seguridad tan pronto estén disponibles.\n"
                 "🔑 **Realiza copias de seguridad regularmente**: Protege tus datos contra pérdida o corrupción.\n"
                 "🔑 **Educa a los usuarios**: La formación es clave para evitar ataques de ingeniería social.\n\n"
                 "Seguir estas prácticas ayudará a protegerte contra las amenazas más comunes."
        )
    elif query.data == 'ciberseguridad_noticias':
        await query.edit_message_text(
            text="📰 **Noticias Recientes en Ciberseguridad**:\n\n"
                 "🔍 Aquí te dejamos algunos titulares recientes en el ámbito de la ciberseguridad:\n"
                 "- **Nuevo ataque de ransomware afecta a miles de empresas en todo el mundo**.\n"
                 "- **Vulnerabilidad crítica descubierta en software ampliamente utilizado**.\n"
                 "- **Aumento de ataques de phishing durante la pandemia**.\n\n"
                 "Mantente al día con las últimas noticias para estar siempre protegido."
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
                 "Conocer estos tipos de malware es crucial para poder detectarlos y eliminarlos a tiempo."
        )
    elif query.data == 'malware_proteccion':
        await query.edit_message_text(
            text="🛡️ **Protección Contra Malware**:\n\n"
                 "🔐 **Usa software antivirus**: Mantén tu antivirus actualizado para detectar y eliminar amenazas.\n"
                 "🔐 **Actualiza tu sistema operativo**: Las actualizaciones suelen incluir parches de seguridad importantes.\n"
                 "🔐 **No abras archivos sospechosos**: Si no conoces el origen de un archivo, es mejor no abrirlo.\n"
                 "🔐 **Evita hacer clic en enlaces desconocidos**: Podrían llevar a sitios maliciosos.\n"
                 "🔐 **Realiza copias de seguridad regularmente**: Así podrás restaurar tu sistema en caso de infección.\n\n"
                 "Estas prácticas son esenciales para protegerte contra la mayoría de los ataques de malware."
        )
    elif query.data == 'malware_casos':
        await query.edit_message_text(
            text="📜 **Casos Famosos de Malware**:\n\n"
                 "🔸 **ILOVEYOU (2000)**: Este gusano de correo electrónico afectó a millones de computadoras en todo el mundo.\n"
                 "🔸 **WannaCry (2017)**: Ransomware que explotó una vulnerabilidad de Windows, causando estragos en miles de sistemas.\n"
                 "🔸 **Stuxnet (2010)**: Malware dirigido a sistemas industriales, utilizado para sabotear el programa nuclear de Irán.\n"
                 "🔸 **Zeus (2007)**: Troyano bancario que robó millones de dólares de cuentas en línea.\n"
                 "🔸 **CryptoLocker (2013)**: Uno de los primeros ransomware modernos que encriptó archivos y exigió un pago en Bitcoin.\n\n"
                 "Estos casos subrayan la importancia de estar siempre vigilante y preparado."
        )

def main():
    # Configuramos el bot con nuestro token
    application = ApplicationBuilder().token(TOKEN).build()

    # Comando /menu para desplegar el menú principal
    application.add_handler(CommandHandler("menu", menu))

    # Manejadores para los menús y submenús
    application.add_handler(CallbackQueryHandler(menu_callback, pattern='menu_'))
    application.add_handler(CallbackQueryHandler(submenu_callback, pattern='linux_'))
    application.add_handler(CallbackQueryHandler(submenu_callback, pattern='hacking_'))
    application.add_handler(CallbackQueryHandler(submenu_callback, pattern='ciberseguridad_'))
    application.add_handler(CallbackQueryHandler(submenu_callback, pattern='malware_'))
    application.add_handler(CallbackQueryHandler(menu_callback, pattern='back_to_menu'))

    # Iniciamos el bot para que comience a escuchar mensajes
    application.run_polling()

if __name__ == '__main__':
    main()
