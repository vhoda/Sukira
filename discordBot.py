import discord
import asyncio
import random
import json
import os
from concurrent.futures import ThreadPoolExecutor
from subprocessHelper import *
from pathHelper import *
from download import download
from autotune import *
from os import remove, path, makedirs
from re import sub

# Cargar el token del bot desde un archivo JSON
TOKEN = json.load(open("tokens.json"))["discord"]

# Configuración básica
messageCheckAmount = 10
dr = "files"
loglevel = "error"
exts = ["mp4", "webm", "mov", "mkv"]

# Crear directorio si no existe
if not path.isdir(dr):
    makedirs(dr)

# Habilitar intents
intents = discord.Intents.default()
intents.messages = True
# Si necesitas el intent para leer el contenido de los mensajes:
intents.message_content = True  # Habilitar este intent

# Crear el bot
bot = discord.AutoShardedClient(intents=intents)

@bot.event
async def on_ready():
    print("Bot ready.")

@bot.event
async def on_message(message):
    print(f"Message received: {message.content}")  # Debug: Ver el contenido del mensaje

    # Verificar que el bot pueda enviar mensajes
    if (not message.guild) or (not message.channel.permissions_for(message.guild.me).send_messages):
        return
    
    # Reemplazar menciones
    message.content = message.content.replace(f'<@{bot.user.id}>', 'autotune')

    # Comando de ayuda
    if message.content.strip().lower() == "autotune help":
        await message.channel.send("""Bot usage:
Autotune <link or search query> - Autotune a video (attached, replied to, or recent in channel) to another video.""")
    elif (s := message.content.strip().lower()).startswith("autotune"):
        attach = None
        # Verificar si hay un archivo adjunto
        if len(message.attachments) > 0:
            attach = message.attachments[0]
        elif message.reference and len(tmpDat := (await message.channel.fetch_message(message.reference.message_id)).attachments) > 0:
            attach = tmpDat[0]
        else:
            async for m in message.channel.history(limit=messageCheckAmount):
                if len(m.attachments) > 0:
                    attach = m.attachments[0]
                    break
        # Procesar el archivo adjunto
        if attach:
            if getExt(attach.filename) in exts:
                if len(spl := sub(' +', ' ', message.content.strip()).split(' ', 1)) > 1:
                    fileName = dr + '/discord_' + str(random.random()) + attach.filename
                    await attach.save(fileName)
                    loop = asyncio.get_event_loop()
                    result = await loop.run_in_executor(ThreadPoolExecutor(), autotuneURL, fileName, spl[1])
                    if type(result) == str:
                        try:
                            await message.channel.send("Autotuning!", file=discord.File(result))
                            remove(result)
                        except Exception as e:
                            print(e)
                            await message.channel.send("Sorry, something went wrong uploading your video. Maybe the file is too large?")
                    else: 
                        await message.channel.send(result[0])
                else:
                    await message.channel.send("Please send a link or search query.")
            else:
                await message.channel.send("Invalid file type, available formats: " + ', '.join(exts))
        else:
            await message.channel.send("Please attach a video to use autotune.")

print("Starting bot...")
bot.run(TOKEN)
