import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes
from dotenv import load_dotenv

# Cargar las variables de entorno
load_dotenv()

TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')

# Función para manejar el comando /menu
async def menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("🐧 Linux", callback_data='menu_linux')],
        [InlineKeyboardButton("💻 Hacking", callback_data='menu_hacking')],
        [InlineKeyboardButton("🔒 Ciberseguridad", callback_data='menu_ciberseguridad')],
        [InlineKeyboardButton("🦠 Malware", callback_data='menu_malware')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    # Si es un comando /menu, se usa update.message
    if update.message:
        await update.message.reply_text(
            "👋 ¡Bienvenido a **TuxSentinel**!\n\n"
            "Seleccione una categoría para explorar contenido detallado:",
            reply_markup=reply_markup
        )
    # Si es un callback del botón "Volver", se usa update.callback_query.message
    elif update.callback_query:
        await update.callback_query.message.edit_text(
            "👋 ¡Bienvenido a **TuxSentinel**!\n\n"
            "Seleccione una categoría para explorar contenido detallado:",
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

    if query.data == 'linux_distribuciones':
        await query.edit_message_text(
            text="🌍 **Distribuciones de Linux**:\n\n"
                 "- Ubuntu\n- Fedora\n- Debian\n- Arch Linux\n- Red Hat\n- CentOS\n\n"
                 "Cada distribución de Linux tiene sus propias características y usos específicos.\n\n"
                 "🔙 /menu para volver al menú principal."
        )
    elif query.data == 'linux_comandos':
        await query.edit_message_text(
            text="💻 **Comandos Básicos de Linux**:\n\n"
                 "`ls`: Listar archivos y directorios\n"
                 "`cd`: Cambiar directorio\n"
                 "`mkdir`: Crear un nuevo directorio\n"
                 "`rm`: Eliminar archivos o directorios\n"
                 "`cp`: Copiar archivos o directorios\n"
                 "`mv`: Mover o renombrar archivos o directorios\n\n"
                 "Estos son solo algunos de los comandos esenciales de Linux.\n\n"
                 "🔙 /menu para volver al menú principal."
        )
    elif query.data == 'linux_instalacion':
        await query.edit_message_text(
            text="🛠️ **Instalación de Linux**:\n\n"
                 "Para instalar Linux, sigue estos pasos generales:\n"
                 "1. Descarga la imagen ISO de la distribución que prefieras.\n"
                 "2. Crea un medio de instalación (USB o DVD).\n"
                 "3. Arranca desde el medio de instalación y sigue las instrucciones.\n"
                 "4. Configura las particiones del disco si es necesario.\n"
                 "5. Completa la instalación y reinicia el sistema.\n\n"
                 "🔙 /menu para volver al menú principal."
        )
    # Aquí puedes agregar más casos para otras opciones de submenús y categorías

def main():
    application = ApplicationBuilder().token(TOKEN).build()

    application.add_handler(CommandHandler("menu", menu))
    application.add_handler(CallbackQueryHandler(menu_callback, pattern='menu_'))
    application.add_handler(CallbackQueryHandler(submenu_callback, pattern='linux_'))
    application.add_handler(CallbackQueryHandler(submenu_callback, pattern='hacking_'))
    application.add_handler(CallbackQueryHandler(submenu_callback, pattern='ciberseguridad_'))
    application.add_handler(CallbackQueryHandler(submenu_callback, pattern='malware_'))
    application.add_handler(CallbackQueryHandler(menu_callback, pattern='back_to_menu'))

    application.run_polling()

if __name__ == '__main__':
    main()
