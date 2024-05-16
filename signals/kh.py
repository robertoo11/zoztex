import os
from flask import Flask, request, jsonify
import asyncio
from telethon.sync import TelegramClient, events
import re

app = Flask(__name__)


api_id = '25633792'
api_hash = 'a08b847627b6ec55eff653e3f4d56805'
phone_number = '966548503651'
channel_id = -4249237690 #-1001940077808 #-4249237690 for testing

os.environ['API_ID'] = api_id
os.environ['API_HASH'] = api_hash
os.environ['PHONE_NUMBER'] = phone_number
os.environ['CHANNEL_ID'] = str(channel_id)

class TelegramListener:
    def __init__(self, api_id: str, api_hash: str, phone_number: str, channel_id: int):
        self.client = TelegramClient('session_name', api_id, api_hash)
        self.channel_id = channel_id
        self.last_message_id = 0

    async def start(self):
        await self.client.start(phone_number)

    async def listen(self):
        entity = await self.client.get_entity(self.channel_id)
        while True:
            new_messages = await self.client.get_messages(entity, limit=None, min_id=self.last_message_id)
            for message in new_messages:
                if message.id > self.last_message_id and message.out:
                    try:
                        signal_lines = message.text.split('\n')
                        signal_data = self.parse_signal(signal_lines)
                        await self.execute_actions(signal_data)
                    except Exception as e:
                        print(f"Error: {str(e)}")
                    self.last_message_id = max(self.last_message_id, message.id)
            await asyncio.sleep(5)

    def parse_signal(self, signal_lines: list[str]) -> dict:
        signal_data = {}
        for line in signal_lines:
            if line.startswith('⏰'):
                signal_data['time_zone'] = line.split(':')[-1].strip()
            elif line.startswith('💰'):
                signal_data['expiry'] = line.split()[-2]
            elif '/' in line:
                match = re.search(r'([\w/]+);(\d{2}:\d{2});(PUT|BUY)', line)
                if match:
                    signal_data['currency_pair'], signal_data['time_to_execute'], signal_data['direction'] = match.groups()
            elif 'GALE' in line:
                match = re.search(r'\d{2}:\d{2}', line)
                if match:
                    signal_data['first_gale_time'] = match.group()
        return signal_data

    async def execute_actions(self, signal_data: dict):
        print("Received signal:")
        print("Currency Pair:", signal_data.get('currency_pair'))
        print("Time to Execute:", signal_data.get('time_to_execute'))
        print("Direction:", signal_data.get('direction'))
        print("First Gale Time:", signal_data.get('first_gale_time'))
        print('-------------------------')
        print('Signal Recieved Succesfully...')

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.json
    return jsonify({'status': 'ok'})

if __name__ == '__main__':
    telegram_listener = TelegramListener(api_id, api_hash, phone_number, channel_id)
    loop = asyncio