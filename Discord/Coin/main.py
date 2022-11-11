
import discord
import os
from dotenv import load_dotenv
import requests
import json
import random
from Discord.Coin.keep_alive import keep_alive
import Discord.Coin.rpc as rpc
from bitcoinrpc.authproxy import AuthServiceProxy, JSONRPCException
from decimal import Decimal


load_dotenv()

TOKEN = os.getenv('TOKEN')
RPCUSER = os.getenv('RPCUSER')
RPCPASSWORD = os.getenv('RPCPASSWORD')
RPCPORT = os.getenv('RPCPORT')


rpc_connection = AuthServiceProxy(f"http://{RPCUSER}:{RPCPASSWORD}@127.0.0.1:{RPCPORT}")

client = discord.Client(intents=discord.Intents.default())

sad_words = ["sad", "happy", "angry"]

starter_eng = []


class DecimalEncoder(json.JSONEncoder):
  def default(self, obj):
    if isinstance(obj, Decimal):
      return str(obj)
    return json.JSONEncoder.default(self, obj)

def get_qoute():
    response = requests.get("https://zenquotes.io/api/random")
    json_data = json.loads(response.text)
    qoute = json_data[0]['q'] + " -" + json_data[0]['a']
    return qoute


@client.event
async def on_ready():
    print('We have logged')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    msg = message.content
    # print(repr(message))

    if msg.startswith('$qoute'):
        await message.channel.send(get_qoute())

    if msg.startswith('$getinfo'):
        res = rpc.getblockchaininfo(rpc_connection)
        json_object = json.dumps(res, cls=DecimalEncoder, indent = 4)
        # print(json_object)
        await message.channel.send(json_object)

    if any(word in msg for word in sad_words):
        await message.channel.send(random.choice(starter_eng))

# keep_alive()
client.run(os.getenv('TOKEN'))