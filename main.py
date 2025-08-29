import os
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, InputMediaPhoto, Update
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

TOKEN = os.getenv("BOT_TOKEN")

if not TOKEN:
    raise ValueError("BOT_TOKEN environment variable is not set!")

# Menu structure
main_menu = [
    [InlineKeyboardButton("Lithuania 🇱🇹", callback_data='lithuania')]
]

lithuania_stats = [
    [InlineKeyboardButton("last 3 hours", callback_data='3h'),
     InlineKeyboardButton("last 24 hours", callback_data='24h')],
     
    [InlineKeyboardButton("last 7 days", callback_data='7d'),
     InlineKeyboardButton("last 30 days", callback_data='30d')],
     
    [InlineKeyboardButton("Back 🔙", callback_data='main')],
]


# Start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    reply_markup = InlineKeyboardMarkup(main_menu)
    await update.message.reply_text("Welcome! Choose a country:", reply_markup=reply_markup)

# Button handler
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    data = query.data
    
    if data == 'main':
        await query.message.delete()   # delete the photo message
        reply_markup = InlineKeyboardMarkup(main_menu)
        await query.message.chat.send_message("Choose a country:", reply_markup=reply_markup)
    elif data == 'lithuania':
        reply_markup = InlineKeyboardMarkup(lithuania_stats)
        await query.edit_message_text("Choose time range:", reply_markup=reply_markup)

    elif data == '3h':
        image_url = "http://ec2-13-60-196-116.eu-north-1.compute.amazonaws.com/queue_length_visual_3_hours.png"
        await query.edit_message_media(
            media=InputMediaPhoto(media=image_url, caption="Queue length in the last 3 hours"),
            reply_markup=InlineKeyboardMarkup(lithuania_stats)
        )
    elif data == '24h':
        image_url = "http://ec2-13-60-196-116.eu-north-1.compute.amazonaws.com/queue_length_visual_24_hours.png"
        await query.edit_message_media(
            media=InputMediaPhoto(media=image_url, caption="Queue length in the last 24 hours"),
            reply_markup=InlineKeyboardMarkup(lithuania_stats)
        )
    elif data == '7d':
        image_url = "http://ec2-13-60-196-116.eu-north-1.compute.amazonaws.com/queue_length_visual_1_week.png"
        await query.edit_message_media(
            media=InputMediaPhoto(media=image_url, caption="Queue length in the last 7 days"),
            reply_markup=InlineKeyboardMarkup(lithuania_stats)
        )
    elif data == '30d':
        image_url = "http://ec2-13-60-196-116.eu-north-1.compute.amazonaws.com/queue_length_visual_1_month.png"
        await query.edit_message_media(
            media=InputMediaPhoto(media=image_url, caption="Queue length in the last 30 days"),
            reply_markup=InlineKeyboardMarkup(lithuania_stats)
        )

    elif data == 'exit':
        await query.edit_message_text("Goodbye! 👋")
    else:
        # Handle item selection
        await query.edit_message_text(f"You selected: {data.capitalize()}")

# Main function
def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler('start', start))
    app.add_handler(CallbackQueryHandler(button_handler))

    app.run_polling()

if __name__ == '__main__':
    main()
