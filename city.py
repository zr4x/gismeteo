from bs4 import BeautifulSoup
from gismeteo import get_html
import re

BASE_URL = 'https://www.gismeteo.ru/catalog/russia/'
FORMAT_URL = 'https://www.gismeteo.ru/catalog/russia/{oblast}'


def parse(html):
    soup = BeautifulSoup(html, "html.parser")
    table = soup.find('div', class_='catalog_side')
    urls = []
    for items in table.find_all('a', {'class': 'link blue'}):
        ready_items = re.findall(r'\/catalog\/russia/(\w.*)', str(items))
        urls.append(ready_items)
    return urls


def main():
    urls = []
    urls.extend(parse(get_html(BASE_URL)))
    for i in range(len(urls)):
        print(FORMAT_URL.format(oblast=str(urls[i])[2:-4]))



if __name__ == '__main__':
    main()