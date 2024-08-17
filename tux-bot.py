import os
import sqlite3
import asyncio
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes
from dotenv import load_dotenv
from database import init_db, obtener_secciones, obtener_articulos, obtener_contenido_articulo

# Cargar las variables de entorno
load_dotenv()
TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')

# Inicializar la base de datos
init_db()

# Variables globales para manejar la creación de artículos
contexto_actual = ""

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
    global contexto_actual

    if contexto_actual == 'crear_articulo':
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
                # Guardar el artículo
                seccion = context.user_data['seccion_actual']
                titulo = context.user_data['titulo_articulo']
                conn = sqlite3.connect('tuxsentinel.db')
                cursor = conn.cursor()
                cursor.execute("INSERT INTO articulos (seccion_id, titulo, contenido) VALUES ((SELECT id FROM secciones WHERE nombre = ?), ?, ?)", 
                               (seccion, titulo, contenido))
                conn.commit()
                conn.close()

                await update.message.reply_text(f"✅ ¡Artículo '{titulo}' añadido a la sección {seccion}!")
                contexto_actual = ""
                context.user_data.pop('titulo_articulo')

# Función para manejar la selección de botones
async def submenu_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query

    if query.data == 'crear_articulo':
        global contexto_actual
        contexto_actual = 'crear_articulo'
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
    application.add_handler(CallbackQueryHandler(menu, pattern='back_to_menu'))

    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, manejar_mensajes))

    application.run_polling()

if __name__ == '__main__':
    main()
