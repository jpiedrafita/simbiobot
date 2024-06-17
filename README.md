# simbiobot
Discord bot for Destiny 2 - [Los Simbiontes](https://discord.gg/kj4g4dwD)

Simbiobot is a Discord bot designed to organize events and allow users to sign up using message reactions.

## Requirements

- Python 3.8 or higher
- `pip` (Python package manager)

## Installation

1. Clone this repository:

   ```bash
   git clone https://github.com/yourusername/simbiobot.git
   cd simbiobot

2. Install requirements (virtual environment recommended)

    ```bash
    pip install -r requirements.txt

3. Store the token created in the [Discord Developeer Portal](https://discord.com/developers/docs/resources/application)

    ```bash
    echo "DISCORD_TOKEN=your-discord-token" >> .env

4. Generate an invitation link from the Discord Developer Portal and invite the bot to the server.

## Usage

1. The configuration is stored in yaml format in [common.yaml](./configs/common.yaml) and [config.prod.yaml](./configs/config.prod.yaml).

2. Run the bot

    ```bash
    python3 bot.py 

## Commands
TODO