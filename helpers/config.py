import orjson

def load_config():
    try:
        with open(r'C:\Users\bokch\PyCharm\W1\data\config.json', 'rb') as file:
            return orjson.loads(file.read())
    except Exception as e:
        print(f"Failed to load config: {e}")
        raise

class Config:
    def __init__(self):
        self.config = load_config()

    def get_bot_token(self):
        return self.config.get("Discord", {}).get("bot_token")

    def get_attachment_head(self):
        return f'https://cdn.discordapp.com/attachments/{self.get_attachments_channel_id()}/'

    def get_attachments_channel_id(self):
        return self.config.get("Discord", {}).get("attachments_channel_id")

    def get_embed_color(self):
        color_str = self.config.get("Discord", {}).get("embed_color")
        return int(color_str, 16)

    def get_mongodb_uri(self):
        return self.config.get("MongoDB", {}).get("uri")

    def get_google_api_credentials(self):
        return self.config.get("Google API", {})
