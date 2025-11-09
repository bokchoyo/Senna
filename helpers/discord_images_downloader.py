import os
import discord
from config import Config
from discord.ext import commands
import json
import asyncio
import requests

config = Config()

intents = discord.Intents.all()  # Enable all intents
client = commands.Bot(command_prefix="!", intents=intents)
output_json_path = r"C:\Users\bokch\PyCharm\W1\data\cars.json"

# Load existing JSON data
if os.path.exists(output_json_path):
    with open(output_json_path, 'r') as json_file:
        cars = json.load(json_file)
else:
    cars = {}


def create_directory(path):
    if not os.path.exists(path):
        os.makedirs(path)

@client.event
async def on_ready():
    print(f'Logged in as {client.user.name} ({client.user.id})')

    channel = client.get_channel(config.get_attachments_channel_id())
    await upload_files(channel)
    print(f"Images have been saved")


# Function to download and save the image using the full URL with query parameters
def save_image(attachment_url, make, model, trim, year):
    try:
        # Make the folder path
        save_folder = rf'C:\Users\bokch\PyCharm\W1\images/{make}/{model}/{trim}/{year}'
        create_directory(save_folder)
        save_path = os.path.join(save_folder, '0.png')
        response = requests.get(attachment_url, stream=True)
        if response.status_code == 200:
            with open(save_path, 'wb') as file:
                for chunk in response.iter_content(1024):
                    file.write(chunk)
            print(f"Image saved to {save_path}")
        else:
            print(f"Failed to download image. Status code: {response.status_code}")
    except Exception as e:
        print(f"Error downloading image: {e}")


async def upload_files(channel):
    for make, models in cars.items():
        for model, trims in models.items():
            for trim, years in trims.items():
                for year, details in years.items():
                    short_url = details.get("url")
                    if short_url:
                        # Construct the full URL for the image with query parameters
                        upload_url = f"https://cdn.discordapp.com/attachments/1299662522600783952/{short_url}"

                        # Upload the image to Discord
                        attachment_url = await get_attachment_url(channel, upload_url)

                        # Download and save the image to the local folder
                        save_image(attachment_url, make, model, trim, year)

                    else:
                        print(f"No URL found for {make} {model} {trim} {year}")


async def get_attachment_url(channel, url):
    try:
        message = await channel.send(url)
        await asyncio.sleep(2)
        # # Download the image to upload it to Discord
        # image_response = requests.get(url)
        # if image_response.status_code == 200:
        #     with open("temp_image.png", "wb") as temp_image:
        #         temp_image.write(image_response.content)
        #
        #     # Send the image to Discord
        #     with open("temp_image.png", "rb") as discord_file:
        #         message = await channel.send(file=discord.File(discord_file, filename="0.png"))

            # Extract the full URL from the uploaded message
        attachment_url = message.attachments[0].url
        print("URL: " + attachment_url)
        return attachment_url

        # Delete the temporary file after upload
        # os.remove("temp_image.png")

        # Update the JSON data with the full URL
        # car_entry = cars.setdefault(make, {}).setdefault(model, {}).setdefault(trim, {}).setdefault(year, {})
        # car_entry["url"] = attachment_url.split("?")[0]  # Get the URL without query params
        # return attachment_url
        # else:
        #     print(f"Failed to fetch image from URL: {url}. Status code: {image_response.status_code}")
    except Exception as e:
        print(f"Error uploading image to Discord: {e}")
        return None

# Replace 'YOUR_BOT_TOKEN' with your actual bot token
client.run(config.get_bot_token())
