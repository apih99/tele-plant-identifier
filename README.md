# Plant Identifier Telegram Bot

A Telegram bot that uses Google's Gemini 2.0 Flash AI model to identify plants from images and provide detailed information about them.

## Features

- Identifies plants from user-submitted photos
- Provides detailed information including:
  - Common name
  - Scientific name
  - Colors
  - Brief history/origin
  - Treatment plan (care instructions)
- Handles unclear or non-plant images with appropriate feedback

## Setup

### Prerequisites

- Python 3.8 or higher
- A Telegram Bot Token (obtained from [@BotFather](https://t.me/botfather))
- A Google Gemini API Key (obtained from [Google AI Studio](https://makersuite.google.com/app/apikey))

### Installation

1. Clone this repository or download the files
2. Install the required dependencies:

```bash
pip install -r requirements.txt
```

3. Set up environment variables:

Create a `.env` file in the project directory with the following content:

```
TELEGRAM_TOKEN=your_telegram_bot_token
GEMINI_API_KEY=your_gemini_api_key
```

Alternatively, you can set these environment variables in your system.

### Running the Bot

Run the bot using the following command:

```bash
python bot.py
```

## Usage

1. Start a chat with your bot on Telegram
2. Send the bot a clear photo of a plant
3. The bot will analyze the image and respond with information about the plant
4. If the image is unclear or doesn't contain a plant, the bot will ask for a clearer image

## Commands

- `/start` - Introduces the bot and explains its purpose
- `/help` - Provides information on how to use the bot

## Technical Details

This bot uses:
- `python-telegram-bot` for Telegram API integration
- Google's Gemini 2.0 Flash AI model for plant identification and information generation
- `python-dotenv` for environment variable management

## Troubleshooting

If you encounter any issues:

1. Ensure your API keys are correctly set in the environment variables
2. Check that your Telegram bot token is valid
3. Verify that you have a stable internet connection
4. Make sure the image you're sending is clear and focused on the plant