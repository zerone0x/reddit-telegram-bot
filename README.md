# Reddit Hot Posts to Telegram

This Python script fetches hot posts from random subreddits and sends them to a Telegram chat. It uses asyncio for asynchronous operations and environment variables for configuration.

## Preview
![CJjZxptest](https://cdn.jsdelivr.net/gh/h3x311/upic@main/LC3/2024/CJjZxptest.png)

## Features

- Randomly selects subreddits from a predefined list
- Fetches hot posts from selected subreddits
- Sends post titles and preview images to a Telegram chat
- Runs continuously with a 15-minute interval between updates

## Prerequisites

- Python 3.7+
- pip

## Setup

1. Clone the repository:
   ```
   git clone https://github.com/zerone0x/reddit-telegram-bot.git
   cd reddit-telegram-bot
   ```

2. Set up a virtual environment:
   ```
   python -m venv venv
   ```

3. Activate the virtual environment:
   - On Windows:
     ```
     venv\Scripts\activate
     ```
   - On macOS and Linux:
     ```
     source venv/bin/activate
     ```

4. Install the required packages:
   ```
   pip3 install -r requirements.txt
   ```

## Environment Variables

This project uses environment variables for configuration. Create a `.env` file in the project root with the following variables:

Replace the placeholder values with your actual credentials and preferences.

- `TOKEN`: Your Telegram Bot API token
- `CHAT_ID`: The ID of the Telegram chat where messages will be sent
- `REDDIT_CLIENT_ID`: Your Reddit application client ID
- `REDDIT_CLIENT_SECRET`: Your Reddit application client secret
- `REDDIT_USER_AGENT`: A unique identifier for your Reddit application
- `SUBREDDITS`: A comma-separated list of subreddit names to fetch posts from
- `SUBREDDITS_COUNT`: The number of subreddits to fetch posts from

## Usage

After setting up the environment and configuring the variables, run the script:

```
python main.py
```
or 
```
nohup python3 main.py &
```
The bot will start fetching hot posts from random subreddits and sending them to the specified Telegram chat every 15 minutes.

## Use with Github Actions

- write env variables to github secrets

## License

[MIT License](https://opensource.org/licenses/MIT)

## Contributing

Contributions, issues, and feature requests are welcome. Feel free to check [issues page](https://github.com/zerone0x/reddit-telegram-bot/issues) if you want to contribute.

## Author

zerone0x - [GitHub](https://github.com/zerone0x)
