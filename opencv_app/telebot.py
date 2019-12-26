import telegram
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import os
import logging
import cv2

#auth Token
TOKEN = 'Your Telegram Token'

def start(update, context):
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Send me some image",
    )

def findingCountour(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray = cv2.blur(gray, (3, 3))
    edges = cv2.Canny(gray, 30, 160)
    ret, th2 = cv2.threshold(edges, 100, 255, cv2.THRESH_BINARY_INV)
    return th2

def callback_func(update, context):
    def send_cv_frame(frame):
        if frame is not None:
            try:
                cv2.imwrite("temp.jpg", frame)
            except:
                logging.info('Failed to dump temp frame to disk as file!')
            context.bot.send_photo(
                chat_id=update.effective_chat.id, photo=open("temp.jpg", "rb")
            )
            os.remove('temp.png')
        else:
            logging.info('Cannot send empty frame!')

    cmd = ""
    img_file = None
    img = None

    cmd = update.effective_message.caption
    img_file = context.bot.get_file(update.message.photo[-1].file_id)

    if img_file is not None:
        img_file.download("img.jpg")
        img = cv2.imread("img.jpg")

    updated_image = findingCountour(img)
    send_cv_frame(updated_image)

def main():
    updater = Updater(TOKEN, use_context=True)
    dispatcher = updater.dispatcher

    start_handler = CommandHandler("start", start)
    cv_handler = MessageHandler(Filters.photo, callback_func)

    dispatcher.add_handler(start_handler)
    dispatcher.add_handler(cv_handler)

    updater.start_polling()
    updater.idle()


if __name__ == "__main__":
    main()
