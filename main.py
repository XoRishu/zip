import os
import zipfile
import tempfile
from pyrogram import Client, filters

# Replace with your Telegram API credentials
API_ID = 27135205
API_HASH = '0996dca78ada710bc31f31b00bb09811'
BOT_TOKEN = '5752952621:AAGO61IiffzN23YuXyv71fbDztA_ubGM6qo'

app = Client('unzip_bot', api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)


@app.on_message(filters.command(['unzip']) & filters.reply)
def unzip_command(client, message):
    # Check if the replied message has a zip file
    if message.reply_to_message.document and message.reply_to_message.document.file_name.endswith('.zip'):
        zip_file = message.reply_to_message.download()

        with tempfile.TemporaryDirectory() as temp_dir:
            with zipfile.ZipFile(zip_file, 'r') as zip_ref:
                # Extract all files to the temporary directory
                zip_ref.extractall(temp_dir)

            for file_name in os.listdir(temp_dir):
                file_path = os.path.join(temp_dir, file_name)

                if os.path.isfile(file_path):
                    # Compress image files to zip format
                    if file_name.lower().endswith(('.jpg', '.jpeg', '.png', '.gif')):
                        temp_zip = tempfile.NamedTemporaryFile(suffix='.zip')
                        with zipfile.ZipFile(temp_zip.name, 'w') as image_zip:
                            image_zip.write(file_path, arcname=file_name)

                        with open(temp_zip.name, 'rb') as f:
                            client.send_document(message.chat.id, f, caption=file_name)

                    # Convert video files to MP4 format
                    elif file_name.lower().endswith(('.mp4', '.avi', '.mkv')):
                        temp_mp4 = tempfile.NamedTemporaryFile(suffix='.mp4')
                        os.system(f'ffmpeg -i "{file_path}" -vcodec copy -acodec copy "{temp_mp4.name}"')

                        with open(temp_mp4.name, 'rb') as f:
                            client.send_video(message.chat.id, f, caption=file_name)

                    # Stream other files directly
                    else:
                        with open(file_path, 'rb') as f:
                            client.send_document(message.chat.id, f, caption=file_name)

        # Remove the downloaded zip file
        os.remove(zip_file)


app.run()
