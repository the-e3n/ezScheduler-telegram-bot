import requests
from bs4 import BeautifulSoup as bs
from os import path
import os
import pickle


def eztv_scrapper(url, page=None, save=False, del_cache=False):
    if page:
        url = f'{url}page_{page}'
    data = requests.get(url).text
    soup = bs(data, 'lxml')
    # print(soup)
    tabels = soup.find_all('table')
    rows = tabels[9].find_all('tr', class_='forum_header_border')
    # print(rows)
    result = {}
    # print(rows[1])
    for i, row in enumerate(rows):
        cells = row.find_all('td')
        episode = {}
        episode['show'] = cells[0].find('a')['title']
        episode['show_link'] = url+cells[0].find('a')['href']
        episode['name'] = cells[1].find('a', class_='epinfo').text
        if cells[2].find('a', class_='magnet'):
            episode['magnet'] = cells[2].find('a', class_='magnet')['href']
        else:
            episode['magnet'] = ''
        if cells[2].find('a', class_='download_1'):
            episode['torrent'] = cells[2].find('a', class_='download_1')['href']
            episode['file_name'] = cells[2].find('a', class_='download_1')['title']
        else:
            episode['torrent'] = ''
        episode['size'] = cells[3].text
        episode['time'] = cells[4].text
        result[episode['name']] = episode
        # file_name = path.join(dest, f'{episode["name"]}.txt')
    if save:
        # if not path.exists(dest):
        #     os.mkdir(dest)
        if del_cache:
            os.remove('.cache')
        with open('.cache', 'w') as f:
            pickle.dump(result, f)

    return result




