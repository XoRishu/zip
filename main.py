import os
import shutil
import zipfile
from telegram import Update, InputFile, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

# Handler for the /start command
def start(update: Update, context: CallbackContext):
    update.message.reply_text("Welcome to the Unzip Bot! Send a zip file to unpack it.")

# Handler for when a zip file is sent
def unzip(update: Update, context: CallbackContext):
    # Check if the message has a document
    if update.message.document:
        file = update.message.document
        # Check if the document is a zip file
        if file.file_name.endswith('.zip'):
            # Download the zip file
            file_id = file.file_id
            new_file = context.bot.get_file(file_id)
            new_file.download('temp.zip')
            
            # Unzip the file
            with zipfile.ZipFile('temp.zip', 'r') as zip_ref:
                zip_ref.extractall('unzipped')
            
            # Remove the temporary zip file
            os.remove('temp.zip')
            
            # Get the list of files in the unzipped folder
            files = os.listdir('unzipped')
            file_count = len(files)
            
            # Prepare the response
            response_text = f"Unzipped {file.file_name}:\n"
            response_text += f"Total files: {file_count}\n"
            response_text += "Contents:"
            
            # Send the response
            update.message.reply_text(response_text)
            
            # Send the contents as compressed images or videos
            for file_name in files:
                file_path = os.path.join('unzipped', file_name)
                if file_name.lower().endswith(('.jpg', '.jpeg', '.png')):
                    context.bot.send_photo(update.message.chat_id, photo=open(file_path, 'rb'))
                elif file_name.lower().endswith(('.mp4', '.avi', '.mkv')):
                    context.bot.send_video(update.message.chat_id, video=open(file_path, 'rb'))
                else:
                    # Send other file types as documents
                    context.bot.send_document(update.message.chat_id, document=open(file_path, 'rb'))
            
            # Remove the unzipped folder
            shutil.rmtree('unzipped')

# Handler for any other message
def unknown(update: Update, context: CallbackContext):
    update.message.reply_text("Sorry, I don't understand that command.")
    
def main():
    # Replace 'TOKEN' with your own Telegram bot token
    updater = Updater('5752952621:AAGO61IiffzN23YuXyv71fbDztA_ubGM6qo', use_context=True)
    dispatcher = updater.dispatcher
    
    # Add handlers for commands and messages
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(MessageHandler(Filters.document, unzip))
    dispatcher.add_handler(MessageHandler(Filters.all, unknown))
    
    # Start the bot
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
