import asyncio
from telethon.sync import TelegramClient, events
import re

# Replace these with your values
api_id = '25633792'
api_hash = 'a08b847627b6ec55eff653e3f4d56805'
phone_number = '966548503651'
channel_id = -1001940077808  # -1001940077808 #-4249237690 for testing

# Create a new TelegramClient
client = TelegramClient('session_name', api_id, api_hash)

async def main():
    # Connect to Telegram
    await client.start(phone_number)

    # Get the channel entity
    entity = await client.get_entity(channel_id)

    last_message_id = 0

    while True:
        # Get new messages from the channel
        new_messages = await client.get_messages(entity, limit=None, min_id=last_message_id)

        # Process the new messages
        for message in new_messages:
            if message.id > last_message_id:
                try:
                    # Check if the message contains text
                    if message.text:
                        signal_lines = message.text.split('\n')  # Split signal into lines

                        # Initialize variables
                        time_zone = expiry = currency_pair = time_to_execute = direction = first_gale_time = None

                        # Flag variable to indicate if the message contains relevant information
                        contains_info = False

                        # Extract relevant information from the signal
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

                        # Print extracted information or "not related"
                        if contains_info:
                            print("Currency Pair:", currency_pair)
                            print("Time to Execute:", time_to_execute)
                            print("Direction:", direction)
                            print('-------------------------')
                        else:
                            print("not related")
                    else:
                        print("not related")

                except Exception as e:
                    print("Error:", str(e))

                # Update last_message_id after processing all messages
                last_message_id = max(last_message_id, message.id)

        await asyncio.sleep(5)

if __name__ == '__main__':
    client.loop.run_until_complete(main())
