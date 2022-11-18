
import discord
import os
from dotenv import load_dotenv
import requests
import json
import random
from keep_alive import keep_alive
import rpc
from bitcoinrpc.authproxy import AuthServiceProxy, JSONRPCException
from decimal import Decimal

load_dotenv()


TOKEN = os.getenv('TOKEN')
RPCUSER = os.getenv('RPCUSER')
RPCPASSWORD = os.getenv('RPCPASSWORD')
RPCPORT = os.getenv('RPCPORT')


intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)
# client = discord.Client(intents=discord.Intents.default())

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
    print("Bot is now ready to use!!!")
    print("--------------------------")


@client.event
async def on_message(message):
    if message.author == client.user:
        return
    msg = message.content

    if msg.startswith('$qoute'):
        await message.channel.send(get_qoute())

    if msg.startswith('$getinfo'):
        rpc_connection = AuthServiceProxy(f"http://{RPCUSER}:{RPCPASSWORD}@127.0.0.1:{RPCPORT}")
        res = rpc.getinfo(rpc_connection)
        json_object = json.dumps(res, cls=DecimalEncoder, indent = 4)
        await message.channel.send(json_object)

    if msg.startswith('$help'):
        help = '''
        $qoute   :   for getting random qoute \n$getinfo :   for getting magnus blockchain info
        '''
        await message.channel.send(help)

client.run(TOKEN)