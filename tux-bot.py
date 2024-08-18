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

# Función para manejar el comando /menu
async def menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    secciones = obtener_secciones()
    keyboard = [[InlineKeyboardButton(seccion, callback_data=f"menu_{seccion}")] for seccion in secciones]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    if update.message:
        await update.message.reply_text(
            "👋 ¡Bienvenido a **TuxSentinel**!\n\nSelecciona una categoría para explorar contenido detallado:",
            reply_markup=reply_markup
        )
    elif update.callback_query:
        await update.callback_query.message.edit_text(
            "👋 ¡Bienvenido de nuevo a **TuxSentinel**!\n\nSelecciona una categoría para explorar contenido detallado:",
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
        await menu(update, context)
    elif data.startswith('aprobar_'):
        await aprobar_callback(update, context)
    elif data.startswith('rechazar_'):
        await rechazar_callback(update, context)  # Asegúrate de implementar esta función
    else:
        await query.answer("Operación desconocida.")  # Para cualquier otra operación desconocida

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
                    articulo_id = obtener_articulo_id(titulo)  # Función que obtendrá el ID del artículo recién agregado
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
                    # Este mensaje se muestra si, por alguna razón, se intenta insertar un artículo con un título duplicado.
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

# Función principal
def main():
    application = ApplicationBuilder().token(TOKEN).build()

    application.add_handler(CommandHandler("menu", menu))
    application.add_handler(CommandHandler("aprobar", manejar_aprobacion, filters.User(user_id=ADMIN_USER_ID)))
    application.add_handler(CallbackQueryHandler(handle_callback_query))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, manejar_mensajes))

    application.run_polling()

if __name__ == '__main__':
    main()
