import os
from os import rename, remove
from download import download
from pathHelper import *
from subprocessHelper import *
import subprocess, random, shutil

# Asegurar que USEWINE esté vacío en Windows
USEWINE = []  # Si no usas Wine, déjalo vacío
loglevel = "error"

def getDur(f):
    return eval(subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "default=noprint_wrappers=1:nokey=1", f],
        stdout=subprocess.PIPE).stdout)

def autotune(base, over, filename, strength=75, executableName="c:/Users/DiscordBot/Desktop/Sukira/autotune.exe", reformatAudio=True, hz=48000):
    strength = max(1, min(strength, 512))
    
    if reformatAudio:
        baseDur = getDur(base)
        loud_run(["ffmpeg", "-y", "-hide_banner", "-loglevel", loglevel, "-i", base, "-ac", "1", "-ar", hz, base := chExt(addPrefix(absPath(base), 'AT_'), 'wav')])
        loud_run(["ffmpeg", "-y", "-hide_banner", "-loglevel", loglevel, "-i", over, "-ac", "1", "-ar", hz, '-t', str(baseDur), over := chExt(addPrefix(absPath(over), 'AT_'), 'wav')])
        
    # Ejecutar autotune
    silent_run(USEWINE + [executableName, '-b', strength, base, over, filename])

    if reformatAudio:
        remove(base)
        remove(over)

def autotuneURL(filename, URL, replaceOriginal=True, video=True, executableName="c:/Users/DiscordBot/Desktop/Sukira/autotune.exe"):
    directory = os.path.split(os.path.abspath(filename))[0]
    downloadName = os.path.join(directory, f"download_{randDigits()}.wav")
    
    # Descargar el audio
    result = download(downloadName, URL, video=False, duration=2 * 60)
    
    if result:
        wavName = os.path.join(directory, f'vidAudio_{randDigits()}.wav')
        
        if video:
            loud_run(["ffmpeg", "-hide_banner", "-loglevel", loglevel, "-i", filename, "-ac", "1", wavName])
        else:
            rename(filename, wavName)
        
        autotuneName = os.path.join(directory, f'autotune_{randDigits()}.wav')
        autotune(wavName, downloadName, autotuneName, executableName=executableName)
        
        remove(downloadName)
        remove(wavName)
        
        exportName = os.path.join(directory, f"{randDigits()}{os.path.splitext(filename)[1]}")
        
        if video:
            loud_run(["ffmpeg", "-hide_banner", "-loglevel", loglevel, "-i", filename, "-i", autotuneName, "-map", "0:v", "-map", "1:a", "-ac", "1", exportName])
            remove(autotuneName)
        else:
            rename(autotuneName, exportName)
        
        if replaceOriginal:
            if video:
                remove(filename)
            rename(exportName, filename)
            return filename
        
        return exportName
    else:
        return [f"Error downloading {URL}"]

randDigits = lambda: str(random.random()).replace('.', '')
