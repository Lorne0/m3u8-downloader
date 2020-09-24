import re

from bs4 import BeautifulSoup

import requests


def get_date(soup):
    date = soup.find('time').contents[0].strip().split(' ')[0]
    Y, M, D = date.split('/')
    return Y[-2:]+M+D


def get_title(soup):
    date = get_date(soup)
    title = soup.find('title').contents[0].replace(
        '<title>', '').replace('</title>', '').split(' -')[0]
    # ex: Radio 気まぐれな雪 #608312633
    if not date and title:
        return '{}.mp4'.format(title)
    if not title:
        return ''
    if date and title:
        return '[{}] {} [TC].mp4'.format(date, title)


def url_to_m3u8_uri(url):

    r = requests.get(url=url)
    m3u8_uri = re.search(r'"url":"(.*?)\.m3u8"', r.text)
    # vid = ''
    if m3u8_uri:
        m3u8_uri = m3u8_uri.group(1)
        m3u8_uri = m3u8_uri.replace('\\', '')
        m3u8_uri += '.m3u8'
        # vid = m3u8_uri.split('/')[5].split('-')[0]

    # meta info
    soup = BeautifulSoup(r.text, 'lxml')
    title = get_title(soup)

    return m3u8_uri, title
