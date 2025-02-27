from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext, ApplicationBuilder, MessageHandler
from dotenv import dotenv_values


async def start(update: Update, context: CallbackContext):
    await update.message.reply_text("Upload an image and the bot will return a 512x512. Keep the image will be converted to 1:1 aspect ratio with crop and scaled to 512x512.")


async def crop_image(update: Update, context: CallbackContext):
    if update.message.document:
        file = await update.message.document.get_file()
        # save the file locally
        await file.download_to_drive('image.jpg')
    else:
        await update.message.reply_text("Please upload an image file.")


app = ApplicationBuilder().token(dotenv_values('.env')['TELEGRAM_TOKEN']).build()
app.add_handler(CommandHandler(command='start', callback=start))
app.add_handler(MessageHandler(filters=None, callback=crop_image))
app.run_polling()
