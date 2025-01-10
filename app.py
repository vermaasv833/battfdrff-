from pyrogram import Client, filters
from downloader import get_video_url, download_video
import os

from config import API_ID, API_HASH, BOT_TOKEN

app = Client("xhamster_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

@app.on_message(filters.command("start"))
async def start(client, message):
    await message.reply("Welcome to xHamster Video Downloader Bot! Send me a link to download.")

@app.on_message(filters.text & ~filters.command)
async def download_handler(client, message):
    url = message.text.strip()

    if "xhamster.com" not in url:
        await message.reply("Please send a valid xHamster URL.")
        return

    await message.reply("Fetching the video... Please wait.")
    video_url = get_video_url(url)

    if not video_url:
        await message.reply("Failed to fetch the video URL. The link might be invalid or unsupported.")
        return

    await message.reply("Downloading the video...")
    output_path = f"{message.chat.id}_video.mp4"
    downloaded_file = download_video(video_url, output_path)

    if downloaded_file:
        await message.reply("Uploading the video...")
        await client.send_video(
            chat_id=message.chat.id,
            video=downloaded_file,
            caption="Here is your downloaded video!"
        )
        os.remove(downloaded_file)  # Clean up after sending the file
    else:
        await message.reply("Failed to download the video.")

app.run()
