@echo off
set BOT_PATH="C:\Users\DiscordBot\Desktop\Sukira\discordBot.py"

:: Cambiar al directorio del bot
cd /d %~dp0

:: Ejecutar el bot con Python
python %BOT_PATH%

:: Mantener la ventana de cmd abierta después de la ejecución
pause
