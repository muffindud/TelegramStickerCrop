from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext, ApplicationBuilder, MessageHandler, filters
from dotenv import dotenv_values
import cv2
from os import remove


async def start(update: Update, context: CallbackContext):
    await update.message.reply_text("Upload an image and the bot will return a 512x512. Keep the image will be converted to 1:1 aspect ratio with crop and scaled to 512x512.")


async def crop_image(update: Update, context: CallbackContext):
    if update.message.document:
        file = await update.message.document.get_file()
        file_name = update.message.document.file_name
        await file.download_to_drive('./cache/' + file_name)

        image = cv2.imread('./cache/' + file_name)

        height, width = image.shape[:2]

        if height > width:
            start = (height - width) // 2
            image = image[start:start + width, :]
        else:
            start = (width - height) // 2
            image = image[:, start:start + height]

        image = cv2.resize(image, (512, 512))

        if not(file_name.endswith('.gif') or file_name.endswith('.png')):
            file_name = file_name.split('.')[0] + '.png'

        cv2.imwrite('./cache/' + file_name, image)
        await update.message.reply_document('./cache/' + file_name)
        remove('./cache/' + update.message.document.file_name)

    else:
        await update.message.reply_text("Please upload an image file.")


app = ApplicationBuilder().token(dotenv_values('.env')['TELEGRAM_TOKEN']).build()
app.add_handler(CommandHandler(command='start', callback=start))
app.add_handler(MessageHandler(filters=None, callback=crop_image))
app.run_polling()
