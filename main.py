import asyncio
import asyncpraw
import random
import sqlite3
from aiohttp import ClientTimeout
from telegram import Bot
from environs import Env

env = Env()
env.read_env()

# Telegram Bot setup
telegram_bot = Bot(token=env.str('TOKEN'))
chat_id = env.str('CHAT_ID')

# SQLite database setup
connection = sqlite3.connect('hot_posts.db')
cursor = connection.cursor()

# Create table if it doesn't exist
cursor.execute('''
CREATE TABLE IF NOT EXISTS hot_posts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    subreddit TEXT,
    title TEXT,
    preview_image_url TEXT,
    UNIQUE(subreddit, title)
)
''')
connection.commit()

async def get_hot_posts(subreddits, limit=200):
    reddit = asyncpraw.Reddit(
        client_id=env.str('REDDIT_CLIENT_ID'),
        client_secret=env.str('REDDIT_CLIENT_SECRET'),
        user_agent=env.str('REDDIT_USER_AGENT'),
        requestor_kwargs={'timeout': ClientTimeout(total=30)}
    )
    hot_posts = {}
    for subreddit in subreddits:
        subreddit_instance = await reddit.subreddit(subreddit)
        hot_posts[subreddit] = []
        all_posts = []
        async for post in subreddit_instance.hot(limit=limit):
            all_posts.append(post)
        random_posts = all_posts
        for post in random_posts:
            title = post.title
            preview_image_url = None

            if hasattr(post, 'preview') and post.preview and 'images' in post.preview:
                images = post.preview['images']
                if images:
                    preview_image_url = images[0]['source']['url']

            hot_posts[subreddit].append({
                'title': title,
                'preview_image_url': preview_image_url or "No preview image available"
            })

    return hot_posts

def store_hot_posts(hot_posts):
    for subreddit, posts in hot_posts.items():
        for post in posts:
            try:
                cursor.execute('''
                INSERT OR IGNORE INTO hot_posts (subreddit, title, preview_image_url)
                VALUES (?, ?, ?)
                ''', (subreddit, post['title'], post['preview_image_url']))
            except sqlite3.IntegrityError:
                pass
    connection.commit()

def fetch_hot_posts(limit=5):
    cursor.execute('SELECT subreddit, title, preview_image_url FROM hot_posts ORDER BY RANDOM() LIMIT ?', (limit,))
    return cursor.fetchall()


async def send_to_telegram(message):
    await telegram_bot.send_message(chat_id=chat_id, text=message)

async def update_database_periodically(subreddits):
    while True:
        new_data = await get_hot_posts(subreddits)
        store_hot_posts(new_data)
        await asyncio.sleep(360000)

async def main():
    subreddits = env.list('SUBREDDITS')
    
    # Start the database update task
    asyncio.create_task(update_database_periodically(subreddits))
    
    while True:
        stored_posts = fetch_hot_posts()
        
        for subreddit, title, preview_image_url in stored_posts:
            message = f"{title}\n\n{preview_image_url}"
            await send_to_telegram(message)
        
        await asyncio.sleep(3600)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    finally:
        connection.close()
