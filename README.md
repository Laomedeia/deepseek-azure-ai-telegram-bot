# Azure DeepSeek AI Telegram Bot

A Simple Telegram bot based Azure DeepSeek AI that can engage in conversations with users

## Prerequisites

- Python 3.8+
- Azure AI service account with DeepSeek model deployment
- Telegram Bot Token

## Setup

1. Install dependencies
2. Create a `.env` file in the project root with your credentials

```env
AZURE_ENDPOINT=your_azure_endpoint
AZURE_KEY=your_azure_key
TELEGRAM_BOT_TOKEN=your_telegram_bot_token
MAX_TOKENS=
```

## Running the Bot

```python app.py```

## Environment Variables

- `AZURE_ENDPOINT`: Your Azure AI service endpoint URL
- `AZURE_KEY`: Your Azure AI service API key
- `TELEGRAM_BOT_TOKEN`: Your Telegram bot token from @BotFather
- `MAX_TOKENS`: Maximum number of tokens for AI response (default: 4096)

## License

MIT License