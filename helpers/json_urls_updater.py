import os
import discord
from config import Config
from discord.ext import commands
import json
import asyncio

config = Config()

intents = discord.Intents.all()  # Enable all intents
client = commands.Bot(command_prefix="!", intents=intents)

folder_path = r"C:\Users\bokch\PyCharm\W1\images"
output_json_path = r"C:\Users\bokch\PyCharm\W1\data\cars.json"

# Load existing JSON data
if os.path.exists(output_json_path):
    with open(output_json_path, 'r') as json_file:
        data_dict = json.load(json_file)
else:
    data_dict = {}


@client.event
async def on_ready():
    print(f'Logged in as {client.user.name} ({client.user.id})')

    channel = client.get_channel(config.get_attachments_channel_id())
    await upload_files(channel)

    # Save the updated data back to cars.json without overwriting existing data
    with open(output_json_path, 'w') as json_file:
        json.dump(data_dict, json_file, indent=4)
    print(f"URLs have been updated in {output_json_path}.")


import subprocess

async def upload_files(channel):
    if not os.path.exists(folder_path) or not os.path.isdir(folder_path):
        await channel.send("Invalid folder path.")
        return

    for root, dirs, files in os.walk(folder_path):
        relative_path = os.path.relpath(root, folder_path)
        path_parts = relative_path.split(os.sep)

        if len(path_parts) == 4:
            make, model, trim, year = [part.replace("_", " ") for part in path_parts]

            model = model.replace("MP4-4", "MP4/4")
            car_entry = data_dict.setdefault(make, {}).setdefault(model, {}).setdefault(trim, {}).setdefault(year, {})

            for file in files:
                file_path = os.path.join(root, file)
                with open(file_path, 'rb') as f:
                    discord_file = discord.File(f, filename=file)
                    message = await channel.send(file=discord_file)

                    attachment_url = message.attachments[0].url
                    url_part = "/".join(attachment_url.split("/attachments/")[-1].split("/")[-2:])
                    url_part = url_part.split(".png")[0] + ".png"
                    car_entry["url"] = url_part
                    print(f"Uploaded: {url_part} for {make} {model} {trim} {year}")

                # await asyncio.sleep(1)  # Optional pause

    # Save updated JSON data
    with open(output_json_path, 'w') as json_file:
        json.dump(data_dict, json_file, indent=4)
    print(f"URLs saved to {output_json_path}.")

    # Update Google Sheet using the script
    subprocess.run(["python", "spreadsheet_url_updater.py"])



# Replace 'YOUR_BOT_TOKEN' with your actual bot token
client.run(config.get_bot_token())
