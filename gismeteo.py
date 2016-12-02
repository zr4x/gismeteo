import urllib.request
from bs4 import BeautifulSoup
import csv
from datetime import datetime

#BASE_URL = 'https://www.gismeteo.ru/diary/4565/2016/'
BASE_URL_FORMAT = 'https://www.gismeteo.ru/diary/4565/{}/{}'


def get_html(url):
    response = urllib.request.urlopen(url)
    return response.read()


def parse(html):
    soup = BeautifulSoup(html, "html.parser")
    table = soup.find('table')
    date = soup.find('div', class_='cover png')
    month = date.find('h1')

    journals = []
    weather_types = {
    }

    for row in table.find_all('tr')[2:]:
        cols = row.find_all('td')
        journals.append({
            'day': cols[0].text,
            'month': month.text[32:-8],
            'year': month.text[-7:-3],
            'weather day': cols[1].text,
            'pressure': cols[2].text,
            'weather night': cols[6].text,
            'pressure night': cols[7].text,

        })

    for journal in journals:
        print(journal)

    return journals


def save(journals, path):
    with open(path, 'w') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(('Day', 'Month', 'Year', 'Weather day', 'Pressure', 'Weather night', 'Pressure night'))

        for journal in journals:
            writer.writerow((journal['day'], journal['month'], journal['year'], journal['weather day'], journal['pressure'], journal['weather night'], journal['pressure night']))


def main():
    current_year = datetime.now().year
    journal = []
    for year in range(current_year - 2, current_year + 1):
        for i in range(1, 13):
            url = BASE_URL_FORMAT.format(year, i)
            print(url)
            journal.extend(parse(get_html(url)))

    save(journal, 'gismeteo.csv')


if __name__ == '__main__':
    main()
