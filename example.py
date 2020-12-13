import cv2
import os
from img_libs import process_file
from airtable_libs import process_client_airtable

import requests

TOKEN = os.environ.get('PICKME_BOT_TOKEN')
BOT_URL = f'https://api.telegram.org/bot{TOKEN}'


def download_file():
    file_name = 'file_50.jpg'
    url = f'https://api.telegram.org/file/bot{TOKEN}/photos/{file_name}'
    r = requests.get(url, allow_redirects=True)

    open(file_name, 'wb').write(r.content)


def test_process_file():
    path_to_file = 'file_51.jpg'
    image = cv2.imread(path_to_file)
    process_file(image)


def test_airtable():
    client_name = 'test_cient'
    process_client_airtable(client_name)


def main():
    print('Start Testing')
    #test_airtable()
    test_process_file()
    #download_file()


if __name__ == '__main__':
    main()
