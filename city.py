from bs4 import BeautifulSoup
from gismeteo import get_html
import re
import csv


DISTRICT_URL = 'https://www.gismeteo.ru{district}'
BASE_URL = 'https://www.gismeteo.ru/catalog/russia/'
FORMAT_URL = 'https://www.gismeteo.ru/catalog/russia/{oblast}'

def parseDistricts(html):
    soup = BeautifulSoup(html, "html.parser")
    urls = []
    table = soup.find('div', class_='catalog_side')
    for items in table.find_all('a', {'class': 'link blue'}):
        name = items.contents[0]
        name = name.replace('\n', '')
        name = name.strip()
        urls.append({"districtName": name, "districtUrl" : DISTRICT_URL.format(district=items.attrs['href'])})
    return urls


def parseRegions(urls):
    regionUrls = []
    for i in range(len(urls)):
        soup = BeautifulSoup(get_html(urls[i]["districtUrl"]), "html.parser")
        if soup.find('div', class_='catalog_side') is None:
            regionUrls.append({
                "regionName": urls[i]["districtName"],
                "regionUrl": urls[i]["districtUrl"],
                "districtName": "-"
            })
        else:
            table = soup.find('div', class_='catalog_side')
            for items in table.find_all('a', {'class': 'link blue'}):
                name = items.contents[0]
                name = name.replace('\n', '')
                name = name.strip()
                regionUrls.append({
                    "districtName": urls[i]["districtName"],
                    "regionUrl": DISTRICT_URL.format(district=items.attrs['href']),
                    "regionName": name
                 })
    return regionUrls

def parseCities(urls):
    citiesUrls = []
    with open("cities.csv", 'a') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(('CityId', 'CityName', 'RegionName', 'DistrictName'))

        for i in range(len(urls)):
            soup = BeautifulSoup(get_html(urls[i]["regionUrl"]), "html.parser")
            table = soup.find('div', class_='catalog_sides')
            for items in table.find_all('a', {'class': 'catalog_item link blue fontM'}):
                name = items.contents[0]
                name = name.replace('\n', '')
                name = name.strip()

                writer.writerow(
                    (str(re.search(r'\d+', items.attrs['href']).group()), name, urls[i]["regionName"], urls[i]["districtName"]))

def main():
    parseCities(parseRegions(parseDistricts(get_html(BASE_URL))))

if __name__ == '__main__':
    main()