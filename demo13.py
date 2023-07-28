import json
import logging
import requests
from bs4 import BeautifulSoup
import time

logging.basicConfig(level=logging.INFO)

bot_token = "6247275701:AAHvVrfJRTek0cO9kYqw4PDmj-oat5YBTNk"
chat_id = "-1001953447226"

def send_inline_keyboard():
    base_url = f'https://api.telegram.org/bot{bot_token}/sendMessage'
    text = 'please Choose the button:'
    keyboard = {
        'inline_keyboard': [
            [{'text': 'News', 'callback_data': 'https://www.capitalethiopia.com/category/arts-and-culture/'}],
            [{'text': 'local News', 'callback_data': 'https://www.capitalethiopia.com/category/capital/'}],
            [{'text': 'Sport', 'callback_data': 'https://www.capitalethiopia.com/category/sports/'}],
            [{'text': 'Business', 'callback_data': 'https://www.ethio360media.com/our-programs'}],
         
        ]
    }
    data = {
        'chat_id': chat_id,
        'text': text,
        'reply_markup': json.dumps(keyboard)
    }
    response = requests.post(base_url, data=data)
    if response.status_code != 200:
        logging.error('Failed to send inline keyboard')
    else:
        logging.info('Inline keyboard sent')

def handle_callback(update):
    callback_query = update['callback_query']
    callback_data = callback_query['data']
    message = callback_query['message']
    chat_id = message['chat']['id']
    logging.info(f'Callback data: {callback_data}')
    # Scrape the selected URL based on the callback data
    data = scrape_data(callback_data)
    # Post the scraped data to the Telegram channel
    post_to_telegram(data)
    # Send the inline keyboard again
    send_inline_keyboard()

def scrape_data(url):
    data = []
    try:
        response = requests.get(url)
        response.raise_for_status()
        content = response.content
        soup = BeautifulSoup(content, 'html.parser')
        if 'news' in url:
            articles = soup.find_all('article')
            for article in articles:
                item = {}
                heading = article.find('h2')
                if heading:
                    heading_text = heading.get_text()
                    item['heading'] = heading_text
                image = article.find('img')
                if image:
                    image_url = image.get('src')
                    item['image'] = image_url
                paragraph = article.find('p')
                if paragraph:
                    paragraph_text = paragraph.get_text()
                    item['paragraph'] = paragraph_text
                data.append(item)
        elif 'politics' in url:
            articles = soup.find_all('article')
            for article in articles:
                item = {}
                heading = article.find('h2')
                if heading:
                    heading_text = heading.get_text()
                    item['heading'] = heading_text
                image = article.find('img')
                if image:
                    image_url = image.get('src')
                    item['image'] = image_url
                paragraph = article.find('p')
                if paragraph:
                    paragraph_text = paragraph.get_text()
                    item['paragraph'] = paragraph_text
                data.append(item)
        elif 'business' in url:
            articles = soup.find_all('article')
            for article in articles:
                item = {}
                heading = article.find('h2')
                if heading:
                    heading_text = heading.get_text()
                    item['heading'] = heading_text
                image = article.find('img')
                if image:
                    image_url = image.get('src')
                    item['image'] = image_url
                paragraph = article.find('p')
                if paragraph:
                    paragraph_text = paragraph.get_text()
                    item['paragraph'] = paragraph_text
                data.append(item)
        else:
            paragraphs = soup.find_all('p')
            for paragraph in paragraphs:
                item = {}
                heading = paragraph.find_previous(['h3',])
                if heading:
                    heading_text = heading.get_text()
                    item['heading'] = heading_text
                image = paragraph.find_previous('img')
                if image:
                    image_url = image.get('src')
                    item['image'] = image_url
                paragraph_text = paragraph.get_text()
                item['paragraph'] = paragraph_text
                data.append(item)
    except requests.exceptions.RequestException as e:
        logging.error(f'Error scraping data: {e}')
    return data

def post_to_telegram(data):
    for item in data:
        message = ""
        if 'heading' in item:
            message += f"<b>{item['heading']}</b>\n\n"
        if 'paragraph' in item:
            message += f"{item['paragraph']}\n\n"
        if 'image' in item:
            image_url = item['image']
            base_url = f'https://api.telegram.org/bot{bot_token}/sendPhoto?chat_id={chat_id}&photo={image_url}&caption={message}&parse_mode=HTML'
            requests.get(base_url)
        else:
            base_url = f'https://api.telegram.org/bot{bot_token}/sendMessage?chat_id={chat_id}&text={message}&parse_mode=HTML'
            requests.get(base_url)
        time.sleep(1)




if __name__ == '__main__':
    # Send the inline keyboard to the Telegram channel
    send_inline_keyboard()

    # Listen for updates from the Telegram Bot API
    offset = None
    while True:
        url = f'https://api.telegram.org/bot{bot_token}/getUpdates'
        params = {'offset': offset, 'timeout': 60}
        response = requests.get(url, params=params)
        updates = response.json()['result']
        for update in updates:
            if 'callback_query' in update:
                # Handle the inline keyboard callback
                handle_callback(update)
            offset = max(offset, update['update_id'] + 1) if offset else update['update_id'] + 1


