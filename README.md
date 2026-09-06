# Simple Discord Bot

A modular, production-ready Discord bot built with Python.

---

## Modules Included

* `moderation`: `kick`, `ban`, `clear`
* `utility`: `ping`, `serverinfo`, `userinfo`
* `fun`: `roll`, `8ball`
* `music`: `play`, `stop`, `join`, `leave`



---

## Project Structure

```text
Simple-Discord-Bot/
├── cogs/
│   ├── fun.py
│   ├── moderation.py
│   ├── music.py
│   └── utility.py
├── .env.example
├── main.py
└── requirements.txt

```

---

## System Requirements

* **Python**: `3.10` or higher
* **FFmpeg**: Must be installed and added to your system `PATH` for the music module to function.

---

## Installation

1. **Clone the repository**:
```bash
git clone https://github.com/Miaoumap24/Simple-Discord-Bot.git
cd Simple-Discord-Bot

```


2. **Set up a virtual environment**:
```bash
python -m venv venv
# On Linux/macOS:
source venv/bin/activate
# On Windows:
venv\Scripts\activate

```


3. **Install dependencies**:
```bash
pip install -r requirements.txt

```



---

## Configuration

1. Create a `.env` file in the root directory:
```env
DISCORD_TOKEN=PutYourDiscordBotTokenHere

```


2. Enable or disable modules in `main.py`:
```python
ENABLED_EXTENSIONS = [
    "cogs.moderation",
    "cogs.utility",
    "cogs.fun",
    "cogs.music",
]

```


3. Ensure the following **Privileged Gateway Intents** are enabled in the [Discord Developer Portal](https://discord.com/developers/applications):
* `MESSAGE CONTENT INTENT`
* `SERVER MEMBERS INTENT`



---

## Usage

Run the bot:

```bash
python main.py

```

---

## Command Reference

### Moderation

| Command | Arguments | Permissions Required | Description |
| --- | --- | --- | --- |
| `/kick` | `member`, `[reason]` | Kick Members | Kicks a specified member from the server. |
| `/ban` | `member`, `[reason]` | Ban Members | Bans a specified member from the server. |
| `/clear` | `amount` | Manage Messages | Bulk deletes a specified number of messages. |

### Utility

| Command | Arguments | Description |
| --- | --- | --- |
| `/ping` | None | Displays current WebSocket latency. |
| `/serverinfo` | None | Shows information and statistics about the current server. |
| `/userinfo` | `[member]` | Displays details about a specified user or yourself. |

### Fun

| Command | Arguments | Description |
| --- | --- | --- |
| `/roll` | `[dice]` | Rolls dice using `NdX` format (e.g., `2d20`). Default: `1d6`. |
| `/8ball` | `question` | Ask the Magic 8-Ball a question. |

### Music

| Command | Arguments | Description |
| --- | --- | --- |
| `/join` | None | Connects the bot to your current voice channel. |
| `/play` | `query` | Streams audio from a YouTube URL or search term. |
| `/stop` | None | Stops audio playback. |
| `/leave` | None | Disconnects the bot from the voice channel. |

---

## License

Distributed under the AGPL-3.0 License. See `LICENSE` for details.
