import os

from config import TMP_FILE_PATH
from chat_bot import ChatBot

bot = ChatBot()
def do_chat(question, files = None):
    print(files)
    if len(files) > 0:
        image = files["upload-file"]
        if image.filename != '':
            path = os.path.join(TMP_FILE_PATH, image.filename)
            image.save(path)
            message = bot.image_chat(question, [path])
            os.remove(path)
            return message
    message = bot.chat(question)
    return message
