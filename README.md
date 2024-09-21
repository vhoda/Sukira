# Sukira Bot

Sukira is a Discord bot designed to apply autotune to videos. With it, you can transform your videos with a musical touch and easily share them on your server.

## Features

- **Video Autotuning**: Apply autotune effects to your videos directly from Discord.
- **Supported Formats**: 
  - mp4
  - webm
  - mov
  - mkv

## Requirements

- **Python**: Make sure you have Python 3.8 or higher installed on your machine.
- **Dependencies**: The bot requires the following Python libraries:
  - `discord.py`
  - `yt-dlp`
  - `ffmpeg` (ensure it is in your PATH)

## Using the Bot

To use the bot, you can type:
`autotune [YouTube Link] + [Video file]`
![image](https://github.com/user-attachments/assets/597176b6-b453-4d4b-842c-278c3a5c0050)


**Important**: The conversion process may take some time. Please be patient; it typically takes around 3-7 seconds.

## Setup Instructions

1. Clone this repository to your local machine.
2. Install the required dependencies using pip:
`pip install discord.py yt-dlp ffmpeg`
3. Make sure `ffmpeg` is installed and accessible from your command line.
4. Add your Discord bot token to a file named `tokens.json`:
```json
{
    "discord": "YOUR_BOT_TOKEN"
}
```
5. Run the Bot
```python discordBot.py```
## Contribution
Feel free to fork this repository and submit pull requests. Any improvements and suggestions are welcome!
