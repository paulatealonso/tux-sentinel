import os
import asyncio
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes
from dotenv import load_dotenv
from database import init_db, obtener_secciones, obtener_articulos, obtener_contenido_articulo, agregar_articulo, obtener_articulos_pendientes, aprobar_articulo, eliminar_articulo, obtener_articulo_id

# Cargar las variables de entorno
load_dotenv()
TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
ADMIN_USER_ID = int(os.getenv('ADMIN_USER_ID'))

# Inicializar la base de datos
init_db()

# Función para manejar mensajes de usuarios no autorizados
async def manejar_no_autorizado(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🚫 Este bot solo está disponible en el grupo de Telegram. Únete aquí: [Enlace al grupo]",
        disable_web_page_preview=True
    )

# Función para manejar mensajes privados
async def manejar_mensajes_privados(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_chat.id != ADMIN_USER_ID:
        await manejar_no_autorizado(update, context)
    else:
        await mostrar_menu_admin(update, context)

# Función para manejar el comando /start para el administrador
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_chat.id != ADMIN_USER_ID:
        await manejar_no_autorizado(update, context)
    else:
        await mostrar_menu_admin(update, context)

# Función para mostrar el menú de administración
async def mostrar_menu_admin(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("📝 Revisar artículos pendientes", callback_data='revisar_pendientes')],
        [InlineKeyboardButton("✏️ Gestionar artículos", callback_data='gestionar_articulos')],
        [InlineKeyboardButton("📂 Gestionar secciones", callback_data='gestionar_secciones')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.effective_message.reply_text(  # Cambiado de update.message a update.effective_message
        "🔧 **Panel de administración**\nSelecciona una opción:",
        reply_markup=reply_markup
    )

# Función para manejar todas las selecciones de administración
async def manejar_seleccion_admin(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    data = query.data

    if data == 'revisar_pendientes':
        await manejar_aprobacion(update, context)
    elif data == 'gestionar_articulos':
        await mostrar_menu_gestion_articulos(update, context)
    elif data == 'gestionar_secciones':
        await mostrar_menu_gestion_secciones(update, context)
    elif data == 'volver_menu_admin':
        await mostrar_menu_admin(update, context)
    else:
        await query.answer("Operación desconocida.")

# Función para mostrar el menú de gestión de artículos
async def mostrar_menu_gestion_articulos(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("➕ Crear nuevo artículo", callback_data='crear_nuevo_articulo')],
        [InlineKeyboardButton("🗑️ Eliminar artículo", callback_data='eliminar_articulo')],
        [InlineKeyboardButton("🔙 Volver", callback_data='volver_menu_admin')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.callback_query.message.edit_text(
        "📝 **Gestión de artículos**\nSelecciona una opción:",
        reply_markup=reply_markup
    )

# Función para mostrar el menú de gestión de secciones
async def mostrar_menu_gestion_secciones(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("➕ Crear nueva sección", callback_data='crear_nueva_seccion')],
        [InlineKeyboardButton("🗑️ Eliminar sección", callback_data='eliminar_seccion')],
        [InlineKeyboardButton("🔙 Volver", callback_data='volver_menu_admin')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.callback_query.message.edit_text(
        "📂 **Gestión de secciones**\nSelecciona una opción:",
        reply_markup=reply_markup
    )

# Función para manejar todas las selecciones de callback
async def handle_callback_query(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    data = query.data

    if data.startswith('menu_'):
        await menu_callback(update, context)
    elif data.startswith('articulo_'):
        await articulo_callback(update, context)
    elif data == 'crear_articulo':
        await iniciar_creacion_articulo(update, context)
    elif data == 'back_to_menu':
        await mostrar_menu_principal(update, context)  # Usar una función específica para manejar el back
    elif data.startswith('aprobar_'):
        await aprobar_callback(update, context)
    elif data.startswith('rechazar_'):
        await rechazar_callback(update, context)
    elif data == 'eliminar_articulo':
        await seleccionar_seccion_eliminar(update, context)
    elif data.startswith('eliminar_seccion_'):
        await seleccionar_articulo_eliminar(update, context)
    elif data.startswith('confirmar_eliminar_'):
        await confirmar_eliminar_articulo(update, context)
    elif data in ['revisar_pendientes', 'gestionar_articulos', 'gestionar_secciones', 'volver_menu_admin']:
        await manejar_seleccion_admin(update, context)
    else:
        await query.answer("Operación desconocida.")

# Función para manejar el comando /menu en el grupo
async def mostrar_menu_principal(update: Update, context: ContextTypes.DEFAULT_TYPE):
    secciones = obtener_secciones()
    keyboard = [[InlineKeyboardButton(seccion, callback_data=f"menu_{seccion}")] for seccion in secciones]
    reply_markup = InlineKeyboardMarkup(keyboard)

    if update.message:
        await update.message.reply_text(
            "👋 ¡Bienvenido a **TuxSentinel**!\n\nSelecciona una categoría para explorar contenido detallado:",
            reply_markup=reply_markup
        )
    else:
        await update.callback_query.message.edit_text(
            "👋 ¡Bienvenido a **TuxSentinel**!\n\nSelecciona una categoría para explorar contenido detallado:",
            reply_markup=reply_markup
        )

# Función para manejar las selecciones del menú principal
async def menu_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    seccion = query.data.replace('menu_', '')
    context.user_data['seccion_actual'] = seccion
    articulos = obtener_articulos(seccion)

    keyboard = [[InlineKeyboardButton(titulo, callback_data=f"articulo_{titulo}")] for titulo in articulos]
    keyboard.append([InlineKeyboardButton("✏️ Crear Artículo", callback_data='crear_articulo')])
    keyboard.append([InlineKeyboardButton("🔙 Volver al Menú Principal", callback_data='back_to_menu')])

    reply_markup = InlineKeyboardMarkup(keyboard)

    await query.edit_message_text(
        text=f"📂 **{seccion} - Artículos disponibles:**",
        reply_markup=reply_markup
    )

# Función para manejar la visualización del contenido de los artículos
async def articulo_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    articulo = query.data.replace('articulo_', '')
    seccion = context.user_data.get('seccion_actual', '')

    contenido = obtener_contenido_articulo(seccion, articulo)
    if contenido:
        await query.edit_message_text(
            text=contenido,
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Volver al Menú Principal", callback_data='back_to_menu')]])
        )
    else:
        await query.edit_message_text(
            text="❌ El contenido de este artículo no está disponible.",
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Volver al Menú Principal", callback_data='back_to_menu')]])
        )

# Función para iniciar el proceso de creación de artículos
async def iniciar_creacion_articulo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['contexto_actual'] = 'crear_articulo'
    await update.callback_query.edit_message_text(
        text="✏️ Por favor, envía el título del artículo (máximo 50 caracteres):",
        reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Volver al Menú Principal", callback_data='back_to_menu')]])
    )

# Función para manejar la creación de artículos y notificar al administrador
async def manejar_mensajes(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if 'contexto_actual' in context.user_data and context.user_data['contexto_actual'] == 'crear_articulo':
        if 'titulo_articulo' not in context.user_data:
            titulo = update.message.text.strip()
            if len(titulo) > 50:
                await update.message.reply_text("❌ El título es demasiado largo. Debe tener menos de 50 caracteres.")
            elif obtener_articulos(context.user_data['seccion_actual']).count(titulo) > 0:
                await update.message.reply_text("❌ El título ya existe. Elige otro.")
            elif "http://" in titulo or "https://" in titulo:
                await update.message.reply_text("❌ No se permiten enlaces en el título.")
            else:
                context.user_data['titulo_articulo'] = titulo
                await update.message.reply_text("📝 Ahora envía el contenido del artículo.")
        else:
            contenido = update.message.text.strip()
            if "http://" in contenido or "https://" in contenido:
                await update.message.reply_text("❌ No se permiten enlaces en el contenido.")
            else:
                seccion = context.user_data['seccion_actual']
                titulo = context.user_data['titulo_articulo']
                try:
                    agregar_articulo(seccion, titulo, contenido)

                    await update.message.reply_text(f"✅ ¡Artículo '{titulo}' enviado para su aprobación!")
                    
                    # Notificar al administrador con contenido completo y botones
                    articulo_id = obtener_articulo_id(titulo)
                    texto_notificacion = (
                        f"📝 **Nuevo artículo pendiente de aprobación**\n\n"
                        f"**Sección:** {seccion}\n"
                        f"**Título:** {titulo}\n\n"
                        f"**Contenido:**\n{contenido}"
                    )
                    botones = InlineKeyboardMarkup([
                        [InlineKeyboardButton("✅ Aprobar", callback_data=f"aprobar_{articulo_id}")],
                        [InlineKeyboardButton("❌ Rechazar", callback_data=f"rechazar_{articulo_id}")]
                    ])
                    await context.bot.send_message(chat_id=ADMIN_USER_ID, text=texto_notificacion, reply_markup=botones)

                    # Resetear contexto
                    context.user_data.pop('titulo_articulo', None)
                    context.user_data.pop('contexto_actual', None)

                except sqlite3.IntegrityError:
                    await update.message.reply_text("❌ Error: El título del artículo ya existe. Por favor, elige otro título.")
                    context.user_data.pop('titulo_articulo', None)

# Función para manejar la aprobación de un artículo
async def aprobar_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    articulo_id = int(query.data.replace('aprobar_', ''))
    aprobar_articulo(articulo_id)
    await query.answer("Artículo aprobado con éxito.")
    await query.edit_message_reply_markup(reply_markup=None)

# Función para manejar el rechazo de un artículo
async def rechazar_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    articulo_id = int(query.data.replace('rechazar_', ''))
    eliminar_articulo(articulo_id)
    await query.answer("Artículo rechazado y eliminado.")
    await query.edit_message_reply_markup(reply_markup=None)

# Función para manejar la lista de artículos pendientes a través del comando /aprobar
async def manejar_aprobacion(update: Update, context: ContextTypes.DEFAULT_TYPE):
    articulos_pendientes = obtener_articulos_pendientes()
    
    if not articulos_pendientes:
        await update.message.reply_text("No hay artículos pendientes de aprobación.")
        return

    for articulo in articulos_pendientes:
        articulo_id, seccion_id, titulo, contenido = articulo
        texto_notificacion = (
            f"📝 **Artículo pendiente de aprobación**\n\n"
            f"**Título:** {titulo}\n\n"
            f"**Contenido:**\n{contenido}"
        )
        botones = InlineKeyboardMarkup([
            [InlineKeyboardButton("✅ Aprobar", callback_data=f"aprobar_{articulo_id}")],
            [InlineKeyboardButton("❌ Rechazar", callback_data=f"rechazar_{articulo_id}")]
        ])
        await update.message.reply_text(texto_notificacion, reply_markup=botones)

# Función para seleccionar una sección al eliminar un artículo
async def seleccionar_seccion_eliminar(update: Update, context: ContextTypes.DEFAULT_TYPE):
    secciones = obtener_secciones()
    keyboard = [[InlineKeyboardButton(seccion, callback_data=f"eliminar_seccion_{seccion}")] for seccion in secciones]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.callback_query.message.edit_text(
        "📂 **Selecciona una sección para eliminar un artículo:**",
        reply_markup=reply_markup
    )

# Función para seleccionar un artículo de una sección para eliminar
async def seleccionar_articulo_eliminar(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    seccion = query.data.replace('eliminar_seccion_', '')
    context.user_data['seccion_actual'] = seccion
    articulos = obtener_articulos(seccion)

    keyboard = [[InlineKeyboardButton(titulo, callback_data=f"confirmar_eliminar_{titulo}")] for titulo in articulos]
    keyboard.append([InlineKeyboardButton("🔙 Volver", callback_data='gestionar_articulos')])
    reply_markup = InlineKeyboardMarkup(keyboard)

    await query.edit_message_text(
        text=f"📑 **Selecciona un artículo para eliminar de la sección {seccion}:**",
        reply_markup=reply_markup
    )

# Función para confirmar la eliminación de un artículo
async def confirmar_eliminar_articulo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    articulo = query.data.replace('confirmar_eliminar_', '')
    seccion = context.user_data.get('seccion_actual', '')

    articulo_id = obtener_articulo_id(articulo)
    eliminar_articulo(articulo_id)

    await query.edit_message_text(
        text=f"✅ El artículo '{articulo}' ha sido eliminado de la sección {seccion}."
    )

# Función principal
def main():
    application = ApplicationBuilder().token(TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("menu", mostrar_menu_principal))
    application.add_handler(CommandHandler("aprobar", manejar_aprobacion, filters.User(user_id=ADMIN_USER_ID)))

    application.add_handler(MessageHandler(filters.ChatType.PRIVATE & filters.TEXT & ~filters.COMMAND, manejar_mensajes_privados))

    application.add_handler(CallbackQueryHandler(handle_callback_query))

    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, manejar_mensajes))

    application.run_polling()

if __name__ == '__main__':
    main()
