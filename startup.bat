@echo off
:: Ruta al archivo discordBot.py
set BOT_DIR="C:\Users\DiscordBot\Desktop\Sukira"

:: Cambiar al directorio del bot
cd /d %BOT_DIR%

:: Ejecutar el bot con Python
python discordBot.py

:: Mantener la ventana de cmd abierta después de la ejecución
pause
