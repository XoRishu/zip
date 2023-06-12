import os
import time
import pyrogram

# Set your API ID, API hash, and bot token
API_ID = 27135205
API_HASH = "0996dca78ada710bc31f31b00bb09811"
BOT_TOKEN = "5752952621:AAGO61IiffzN23YuXyv71fbDztA_ubGM6qo"

# Create a bot
bot = pyrogram.Client(
    "UnzipBot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN,
)

# Add a start command
@bot.on_message(filters=pyrogram.filters.command("start"))
async def start(client, message):
    await message.reply("Welcome to the Unzip Bot! Use the /unzip command to unzip files.")

# Add an unzip command
@bot.on_message(filters=pyrogram.filters.command("unzip"))
async def unzip(client, message):
    # Check if the user sent a file
    if not file:
        await message.reply("Please send a file to unzip.")
        return

    # Get the file from the user
    file = await message.reply("Send me the file to unzip.")

    # Check if the file is a zip file
    if file.document.file_type != "zip":
        await message.reply("That's not a zip file!")
        return

    # Download the file
    path = await file.download()

    # Unzip the file
    with zipfile.ZipFile(path) as zip_file:
        for file in zip_file.infolist():
            # Check if the file is an image or video
            if file.filename.endswith(".jpg") or file.filename.endswith(".jpeg") or file.filename.endswith(".png") or file.filename.endswith(".mp4"):
                # Get the file content
                content = await zip_file.read(file.filename)

                # Send the file content to the user
                await message.reply_photo(content, caption=file.filename)
            else:
                # Get the file content
                content = await zip_file.read(file.filename)

                # Send the file content to the user
                await message.reply_document(content, caption=file.filename)

    # Delete the file
    os.remove(path)

# Run the bot
bot.run()
