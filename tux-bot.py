import os
import sqlite3
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes
from dotenv import load_dotenv
from database import init_db, obtener_secciones, obtener_articulos, obtener_contenido_articulo, agregar_articulo

# Cargar las variables de entorno
load_dotenv()
TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')

# Inicializar la base de datos
init_db()

# Diccionario para manejar la creación de artículos por usuario
estado_creacion = {}

# Función para manejar el comando /menu
async def menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    secciones = obtener_secciones()
    keyboard = [[InlineKeyboardButton(seccion, callback_data=f"menu_{seccion}")]
                for seccion in secciones]
    
    reply_markup = InlineKeyboardMarkup(keyboard)

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
    seccion = query.data.replace('menu_', '')
    context.user_data['seccion_actual'] = seccion
    articulos = obtener_articulos(seccion)

    keyboard = [[InlineKeyboardButton(titulo, callback_data=f"articulo_{titulo}")]
                for titulo in articulos]
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

# Función para manejar la creación de artículos
async def manejar_mensajes(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id

    if user_id in estado_creacion:
        estado = estado_creacion[user_id]

        if estado['estado'] == 'esperando_titulo':
            titulo = update.message.text.strip()
            if len(titulo) > 50:
                await update.message.reply_text("❌ El título es demasiado largo. Debe tener menos de 50 caracteres.")
            elif obtener_articulos(estado['seccion_actual']).count(titulo) > 0:
                await update.message.reply_text("❌ El título ya existe. Elige otro.")
            elif "http://" in titulo or "https://" in titulo:
                await update.message.reply_text("❌ No se permiten enlaces en el título.")
            else:
                estado_creacion[user_id]['titulo_articulo'] = titulo
                estado_creacion[user_id]['estado'] = 'esperando_contenido'
                await update.message.reply_text("📝 Ahora envía el contenido del artículo.")
        elif estado['estado'] == 'esperando_contenido':
            contenido = update.message.text.strip()
            if "http://" in contenido or "https://" in contenido:
                await update.message.reply_text("❌ No se permiten enlaces en el contenido.")
            else:
                # Guardar el artículo
                seccion = estado_creacion[user_id]['seccion_actual']
                titulo = estado_creacion[user_id]['titulo_articulo']
                agregar_articulo(seccion, titulo, contenido)

                await update.message.reply_text(f"✅ ¡Artículo '{titulo}' añadido a la sección {seccion}!")
                del estado_creacion[user_id]  # Resetear el estado del usuario

# Función para manejar la selección de botones
async def submenu_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    user_id = query.from_user.id

    if query.data == 'crear_articulo':
        estado_creacion[user_id] = {
            'estado': 'esperando_titulo',
            'seccion_actual': context.user_data['seccion_actual']
        }
        await query.edit_message_text(
            text="✏️ Por favor, envía el título del artículo (máximo 50 caracteres):",
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Volver al Menú Principal", callback_data='back_to_menu')]])
        )
    elif query.data.startswith('articulo_'):
        await articulo_callback(update, context)
    else:
        context.user_data['seccion_actual'] = query.data.replace('menu_', '')
        await menu_callback(update, context)

# Función principal
def main():
    application = ApplicationBuilder().token(TOKEN).build()

    application.add_handler(CommandHandler("menu", menu))
    application.add_handler(CallbackQueryHandler(menu_callback, pattern='menu_'))
    application.add_handler(CallbackQueryHandler(submenu_callback, pattern='articulo_'))
    application.add_handler(CallbackQueryHandler(submenu_callback, pattern='crear_articulo'))
    application.add_handler(CallbackQueryHandler(menu, pattern='back_to_menu'))

    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, manejar_mensajes))

    application.run_polling()

if __name__ == '__main__':
    main()
