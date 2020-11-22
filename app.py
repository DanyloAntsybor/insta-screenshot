import os
import logging
import json
import requests
import numpy as np
import cv2

from flask import Flask, request
from img_libs import crop_file, get_user_name

app = Flask(__name__)

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)

TOKEN = os.environ.get('PICKME_BOT_TOKEN')
BOT_URL = f'https://api.telegram.org/bot{TOKEN}'


@app.route('/input_message', methods=['POST'])
def get_message_from_telegram():
    data = request.get_json()
    print(data)

    chat_id = data['message']['chat']['id']
    user_name = data['message']['chat'].get('username')

    prepared_answer = {
        "chat_id": chat_id,
        "text": f'Thank you {user_name} for your message! We received it',
    }

    # message_text = data['message']['text']
    if 'document' in data['message'].keys():
        print('We have your document!')
        print(data['message']['document'])
        doc_id = data['message']['document']['file_id']
        get_file_from_tg(doc_id)

    if 'photo' in data['message'].keys():
        print('We have your photo!')
        print(data['message']['photo'])

        biggest_photo = get_biggest_file_id(data['message']['photo'])
        print(f'Biggest file: {biggest_photo}')
        insta_username = get_file_from_tg(biggest_photo['file_id'])
        prepared_answer['text'] = f'Username on img: {insta_username}'

    if 'text' in data['message'].keys():
        print('We have your text!')
        print(data['message']['text'])

    send_message(prepared_answer)

    return 'Hello, World!'


def get_biggest_file_id(photo_file_list):
    max_size = 0
    biggest_file = None
    for file in photo_file_list:
        if file['file_size'] > max_size:
            biggest_file = file

    return biggest_file


def send_message(prepared_data):
    """
    Prepared data should be json which includes at least `chat_id` and `text`
    """
    message_url = BOT_URL + '/sendMessage'
    requests.post(message_url, json=prepared_data)  # don't forget to make import requests lib


def get_file_from_tg(file_id):
    """
    Prepared data should be json which includes at least `chat_id` and `text`
    """
    get_file_url = BOT_URL + f'/getFile'

    response = requests.get(get_file_url, params={'file_id': file_id})
    json_data = json.loads(response.content)
    print(json_data)
    file_path = json_data['result']['file_path'] if json_data['result'] else None
    print(file_path)

    file_url = f'https://api.telegram.org/file/bot{TOKEN}/{file_path}'
    print(file_url)
    r = requests.get(file_url, allow_redirects=True)

    file_bytes = r.content
    print('got file')

    # test purposes
    file_name = f'debug_test_photo.jpg'
    open(file_name, 'wb').write(file_bytes)

    print(type(file_bytes))
    username = process_file(file_bytes)
    return username


def process_file(file_content):
    # convert string of image data to uint8
    nparr = np.fromstring(file_content, np.uint8)
    # decode image
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    cropped_img = crop_file(img)
    user_name = get_user_name(cropped_img)
    print('user_name: ', user_name)
    print('Finish processing file')
    return user_name


@app.route('/')
def test_main_index():
    print('Hello World!')
