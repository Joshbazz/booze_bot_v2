import os
import json
import asyncio
import discord
from discord.ext import commands

class WhiskeyBot:
    def __init__(self, token, channel_id):
        self.token = token
        self.channel_id = channel_id

        # Dynamically construct the path to the JSON file in the data directory
        data_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data')
        self.json_file_path = os.path.join(data_dir, 'whiskey_data.json')

        self.bot = commands.Bot(command_prefix="!", intents=discord.Intents.default())
        self.last_known_data = None  # To track updates in the JSON file

    def load_json_data(self):
        """
        Load the current JSON data from the file.
        """
        if os.path.exists(self.json_file_path):
            with open(self.json_file_path, 'r') as file:
                return json.load(file)
        return {}

    async def check_for_updates(self, channel):
        """
        Periodically checks for updates in the JSON file and sends alerts to Discord.
        """
        while True:
            try:
                # Load the current data from the JSON file
                current_data = self.load_json_data()

                # If this is the first check, initialize last_known_data
                if self.last_known_data is None:
                    self.last_known_data = current_data

                # If new data is found, send an alert
                if current_data != self.last_known_data:
                    # Convert dictionaries to tuples of sorted key-value pairs for comparison
                    last_known_set = {tuple(sorted(entry.items())) for entry in self.last_known_data}
                    current_set = {tuple(sorted(entry.items())) for entry in current_data}

                    # Find new entries
                    new_entries = current_set - last_known_set

                    # Send alerts for new entries
                    for entry in new_entries:
                        dict_entry = dict(entry)  # Convert back to dictionary for display
                        await channel.send(f"New data added: {dict_entry}")
                    # new_entries = [entry for entry in current_data if entry not in self.last_known_data]

                    # for entry in new_entries:
                    #     await channel.send(f"New data added: {entry}")

                    # # Update the last known data
                    self.last_known_data = current_data
            except Exception as e:
                print(f"Error checking for updates: {e}")

            # Wait 10 seconds before checking again
            await asyncio.sleep(10)

    async def send_initial_data(self, channel):
        """
        Sends the current JSON data to the channel when the bot starts.
        """
        current_data = self.load_json_data()
        if current_data:
            await channel.send("Current Bottles Detected:")
            for entry in current_data:
                await channel.send(f"{entry}")
        else:
            await channel.send("No data found in JSON file.")

        # Initialize last_known_data with current data
        self.last_known_data = current_data

    async def on_ready(self):
        """
        Triggered when the bot is ready. Sends initial data and starts update monitoring.
        """
        print(f'Bot connected as {self.bot.user}')
        channel = self.bot.get_channel(self.channel_id)

        if channel is None:
            print(f"Error: Channel ID {self.channel_id} not found.")
            return

        # Send initial data
        await self.send_initial_data(channel)

        # Start checking for updates
        self.bot.loop.create_task(self.check_for_updates(channel))

    async def start(self):
        """
        Starts the bot and initializes event handlers.
        """
        @self.bot.event
        async def on_ready():
            await self.on_ready()

        await self.bot.start(self.token)  # Use bot.start() instead of bot.run()
