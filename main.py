import os
import zipfile
import tempfile
import asyncio
from pyrogram import Client, filters

# Replace with your Telegram API credentials
API_ID = 27135205
API_HASH = '0996dca78ada710bc31f31b00bb09811'
BOT_TOKEN = '5752952621:AAGO61IiffzN23YuXyv71fbDztA_ubGM6qo'

app = Client('unzip_bot', api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)


# Start command handler
@app.on_message(filters.command("start"))
def start_command(client, message):
    client.send_message(
        chat_id=message.chat.id,
        text="Welcome to the Unzip Bot! Send a zip file and reply to it with /unzip command to unzip it.",
    )

# Unzip command handler
@app.on_message(filters.command("unzip") & filters.reply)
def unzip_command(client, message):
    reply_message = message.reply_to_message

    if reply_message.document and reply_message.document.mime_type == "application/zip":
        # Download the zip file
        file_path = client.download_media(
            message=reply_message,
            file_name="temp.zip"
        )

        # Unzip the file
        unzip_directory = os.path.splitext(file_path)[0]
        os.makedirs(unzip_directory, exist_ok=True)
        os.system(f"unzip -qq {file_path} -d {unzip_directory}")

        # Get the contents of the unzipped directory
        contents = os.listdir(unzip_directory)

        # Send the contents as a reply
        for item in contents:
            item_path = os.path.join(unzip_directory, item)
            if os.path.isfile(item_path):
                # Check if it's an image file
                if item.endswith((".jpg", ".jpeg", ".png")):
                    # Compress the image
                    compressed_image = compress_image(item_path)

                    # Send the compressed image
                    client.send_photo(
                        chat_id=message.chat.id,
                        photo=compressed_image
                    )
                # Check if it's a video file
                elif item.endswith((".mp4", ".mkv")):
                    # Send the video
                    client.send_video(
                        chat_id=message.chat.id,
                        video=item_path
                    )
                else:
                    # Send other files as documents
                    client.send_document(
                        chat_id=message.chat.id,
                        document=item_path
                    )

        # Cleanup: remove the zip file and the unzipped directory
        os.remove(file_path)
        os.system(f"rm -rf {unzip_directory}")
    else:
        client.send_message(
            chat_id=message.chat.id,
            text="Please reply to a zip file to unzip it."
        )

# Helper function to compress images
def compress_image(image_path):
    # Your image compression logic goes here
    # You can use libraries like PIL or OpenCV to compress the images
    # Return the path to the compressed image file
    return image_path

# Run the bot
asyncio.run(app.run())
