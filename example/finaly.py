import asyncio
import sys
import time
import schedule
import re
import json
from telethon.sync import TelegramClient
from termcolor import colored
from quotexpy import Quotex
from quotexpy.utils import asset_parse  
from quotexpy.utils.account_type import AccountType
from quotexpy.utils.operation_type import OperationType
from quotexpy.utils.duration_time import DurationTime
from my_connection import MyConnection
import config




api_id = config.api_id
api_hash = config.api_hash
phone_number = config.phone_number
channel_id = config.channel_id

client = Quotex(
    email = config.email_qtx, 
    password = config.password_qtx
)

async def signal():
    teleclient = TelegramClient('bot', api_id, api_hash)
    await teleclient.start(phone_number)
    entity = await teleclient.get_entity(channel_id)
    last_message_id = 0

    while True:
        new_messages = await teleclient.get_messages(entity, limit=None, min_id=last_message_id)

        for message in new_messages:
            if message.id > last_message_id:
                try:
                    if message.text:
                        signal_lines = message.text.split('\n')

                        time_zone = expiry = currency_pair = time_to_execute = direction = first_gale_time = None
                        contains_info = False

                        for line in signal_lines:
                            if line.startswith('⏰'):
                                time_zone = line.split(':')[-1].strip()
                                contains_info = True
                            elif line.startswith('💰'):
                                expiry = line.split()[-2]
                                contains_info = True
                            elif '/' in line:
                                match = re.search(r'([\w/]+);(\d{2}:\d{2});(PUT|BUY)', line)
                                if match:
                                    currency_pair, time_to_execute, direction = match.groups()
                                    contains_info = True
                                elif 'GALE' in line:
                                    match = re.search(r'\d{2}:\d{2}', line)
                                    if match:
                                        first_gale_time = match.group()
                                        contains_info = True

                        if contains_info:
                            data = {
                                "Currency Pair": currency_pair,
                                "Time to Execute": time_to_execute,
                                "Direction": direction,
                                "Time Zone": time_zone,
                                "Expiry": expiry,
                                "First Gale Time": first_gale_time
                            }
                            with open('signals.json', 'w') as json_file:
                                json.dump(data, json_file, indent=4)

                            print(colored('SIGNAL', 'yellow'))
                            print(colored("Currency Pair:", 'cyan'), currency_pair)
                            print(colored("Time to Execute:", 'red'), time_to_execute)
                            print(colored("Direction:", 'magenta'), direction)
                            print(colored('--------------', 'green'))
                            
                            return data  # Return the signal data as a dictionary

                except Exception as e:
                    print("Error:", str(e))

                last_message_id = max(last_message_id, message.id)

        await asyncio.sleep(5)

def load_signal_data(file_path):
    try:
        with open('signals.json', 'r') as json_file:
            signal_data = json.load(json_file)
            return signal_data
    except FileNotFoundError:
        print("Signal file not found.")
        return None
    except json.JSONDecodeError:
        print("Error decoding JSON.")
        return None
    
async def print_signal(): #for error checks
    # Load signal data from the JSON file
    signal_data = load_signal_data('signals.json')
    if signal_data:
        currency_pair = signal_data.get("Currency Pair")
        currency_pair = currency_pair.replace('/', '')
        time_to_execute = signal_data.get("Time to Execute")
        direction = signal_data.get("Direction")
        print("Currency Pair:", currency_pair)
        print("Time to Execute:", time_to_execute)
        print("Direction:", direction)

def check_asset(asset):
    asset_query = asset_parse(asset)
    asset_open = client.check_asset_open(asset_query)
    if not asset_open[2]:
        print(colored("[WARN]: ", "yellow"), "Asset is closed.")
        asset = f"{asset}_otc"
        print(colored("[WARN]: ", "yellow"), "Try OTC Asset -> " + asset)
        asset_query = asset_parse(asset)
        asset_open = client.check_asset_open(asset_query)
    return asset, asset_open




async def trade():
    prepare_connection = MyConnection(client)
    check_connect, message = await prepare_connection.connect()
    signal_data = load_signal_data('signals.json')
    if signal_data:
        
        currency_pair = signal_data.get("Currency Pair")
        time_to_execute = signal_data.get("Time to Execute")
        direction = signal_data.get("Direction")
    if check_connect:
        amount = 50
        asset, asset_open = check_asset(currency_pair)
        if asset_open[2]:
            if direction == 'PUT':
                action = [OperationType.PUT_RED]
            elif direction == 'BUY':
                action = [OperationType.CALL_GREEN]
            print(colored('--------------', 'blue'))
            print(colored('[EXECUTING TRADE]', 'blue'))
            status, trade_info = await client.trade(direction, amount, currency_pair, DurationTime.FIVE_MINUTES)
            if status:
                print('Waiting for result...')
                if await client.check_win(currency_pair, trade_info['id']):
                    print(colored("[WIN]", "green"))
                    print(colored('--------------', 'blue'))
                else:
                    print(colored("[LOSS]", 'red'))
                    print(colored('[GALE]', 'blue'))
                    status_gale, gale_info = await client.trade(action, amount, currency_pair, DurationTime.FIVE_MINUTES)
                    if status_gale:
                        print(colored('Waiting for gale...'))
                        if await client.check_win(currency_pair, gale_info['id']):
                            print(colored('[WIN GALE]', 'green'))
                            print(f'Profit: {client.get_profit()}')
                            print(colored('--------------', 'blue'))
                        else:
                            print(colored("[LOSS]", 'red'))
                            print(colored('--------------', 'blue'))
async def main():
    while True:
        new_signal = await signal()
        if new_signal:
            await trade()

# Run the main function
asyncio.run(main())
