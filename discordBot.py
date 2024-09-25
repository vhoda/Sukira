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
import time  
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
intents.message_content = True  # Habilitar este intent para leer contenido de los mensajes

# Crear el bot
bot = discord.AutoShardedClient(intents=intents)

@bot.event
async def on_ready():
    print("Bot ready.")

@bot.event
async def on_message(message):
    # Ignorar mensajes enviados por el bot mismo
    if message.author == bot.user:
        return

    print(f"Message received: {message.content}")  # Debug: Ver el contenido del mensaje

    # Verificar que el bot pueda enviar mensajes
    if not message.guild or not message.channel.permissions_for(message.guild.me).send_messages:
        return
    
    # Reemplazar menciones
    message.content = message.content.replace(f'<@{bot.user.id}>', 'autotune')

    # Comando de ayuda
    if message.content.strip().lower() == "autotune help":
        await message.channel.send("""Bot usage:
Autotune <link or search query> - Autotune a video (attached, replied to, or recent in channel) to another video.""")
        return
    # Comando ping para calcular la latencia
    if message.content.strip().lower() == "autotune ping":
        start_time = time.time()  # Guardar el tiempo inicial
        msg = await message.channel.send("Pinging...")
        end_time = time.time()  # Guardar el tiempo final
        ping = round((end_time - start_time) * 1000)  # Calcular la latencia en milisegundos
        await msg.edit(content=f"Pong! {ping}ms")
        return

    if message.content.strip().lower().startswith("autotune"):
        attach = None
        # Verificar si hay un archivo adjunto
        if message.attachments:
            attach = message.attachments[0]
        elif message.reference:
            ref_message = await message.channel.fetch_message(message.reference.message_id)
            if ref_message.attachments:
                attach = ref_message.attachments[0]
        else:
            # Buscar mensajes anteriores
            async for m in message.channel.history(limit=messageCheckAmount):
                if m.attachments:
                    attach = m.attachments[0]
                    break
        
        # Procesar el archivo adjunto
        if attach:
            if getExt(attach.filename) in exts:
                if len(spl := sub(' +', ' ', message.content.strip()).split(' ', 1)) > 1:
                    fileName = os.path.join(dr, f'discord_{random.random()}{attach.filename}')
                    await attach.save(fileName)
                    try:
                        loop = asyncio.get_event_loop()
                        # Añadir un límite de tiempo para el autotune
                        result = await asyncio.wait_for(
                            loop.run_in_executor(ThreadPoolExecutor(), autotuneURL, fileName, spl[1]), 
                            timeout=300  # 5 minutos de espera máxima
                        )
                        
                        if isinstance(result, str):
                            try:
                                await message.channel.send("Autotuned! Any Problems please contact @vhodita on Twitter!", file=discord.File(result))
                                remove(result)
                            except Exception as e:
                                print(e)
                                await message.channel.send("Sorry, something went wrong uploading your video. Maybe the file is too large?")
                        else: 
                            await message.channel.send(result[0])
                    except asyncio.TimeoutError:
                        await message.channel.send("Sorry, the process took too long. Try again with a shorter video.")
                    except Exception as e:
                        print(f"Error processing video: {e}")
                        await message.channel.send("An error occurred while processing the video.")
                    finally:
                        if path.exists(fileName):
                            remove(fileName)
                else:
                    await message.channel.send("Please send a link or search query.")
            else:
                await message.channel.send(f"Invalid file type. Available formats: {', '.join(exts)}")
        else:
            await message.channel.send("Please attach a video to use autotune.")

print("Starting bot...")
bot.run(TOKEN)
