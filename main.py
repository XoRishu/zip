import os
import zipfile
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from telegram import InputMediaPhoto, InputMediaVideo

TOKEN = '5752952621:AAGO61IiffzN23YuXyv71fbDztA_ubGM6qo'

def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Send a zip file with the /unzip command to extract its contents.")

def unzip(update, context):
    # Check if the message has a document
    if not update.message.document:
        context.bot.send_message(chat_id=update.effective_chat.id, text="Please send a document.")
        return

    # Check if the document is a zip file
    if update.message.document.mime_type != 'application/zip':
        context.bot.send_message(chat_id=update.effective_chat.id, text="Please send a zip file.")
        return

    file_id = update.message.document.file_id
    file_name = update.message.document.file_name

    # Download the zip file
    file_path = context.bot.get_file(file_id).download(file_name)

    # Extract the contents
    extracted_files = []
    with zipfile.ZipFile(file_path, 'r') as zip_ref:
        for file in zip_ref.namelist():
            # Extract each file from the zip
            zip_ref.extract(file, './temp')
            extracted_files.append(file)

    # Prepare and send the extracted files
    for file in extracted_files:
        file_path = os.path.join('./temp', file)
        with open(file_path, 'rb') as f:
            # Check if it's an image or video file
            if file.endswith(('.jpg', '.jpeg', '.png', '.gif')):
                context.bot.send_photo(chat_id=update.effective_chat.id, photo=f, caption=file)
            elif file.endswith(('.mp4', '.avi', '.mkv')):
                context.bot.send_video(chat_id=update.effective_chat.id, video=f, caption=file)
            else:
                context.bot.send_document(chat_id=update.effective_chat.id, document=f, caption=file)

    # Clean up temporary directory
    os.system('rm -r ./temp')

    # Delete the downloaded zip file
    os.remove(file_path)

def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("unzip", unzip))
    
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
