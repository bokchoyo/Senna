from datetime import datetime
from aiologger import Logger as AioLogger
from aiologger.formatters.json import JsonFormatter
from aiologger.handlers.files import AsyncFileHandler

class Logger(AioLogger):
    def __init__(self, file_name):
        super().__init__()
        self._setup(file_name)

    def _setup(self, file_name):
        file_handler = AsyncFileHandler(
            filename=fr'C:\Users\bokch\PyCharm\W1\logs\{file_name}', mode='a'
        )
        file_handler.formatter = JsonFormatter()
        self.add_handler(file_handler)

    async def log(self, level, function, message_key, message):
        log = {
            "time": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            "function": function,
            message_key: message
        }
        try:
            await getattr(super(), level)(log)
        except Exception as e:
            print(f"Failed to log {level}: {e}")

    async def log_info(self, function, message):
        await self.log("info", function, "message", message)

    async def log_error(self, function, message):
        await self.log("error", function, "error", message)

    async def log_warning(self, function, message):
        await self.log("warning", function, "error", message)

    async def close(self):
        await super().shutdown()