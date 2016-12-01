import urllib.request
from bs4 import BeautifulSoup
import csv

BASE_URL = 'https://www.gismeteo.ru/diary/4565/2016/'


def get_html(url):
    response = urllib.request.urlopen(url)
    return response.read()


def parse(html):
    soup = BeautifulSoup(html, "html.parser")
    table = soup.find('table')
    date = soup.find('div', class_='cover png')
    month = date.find('h1')

    journals = []

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
    journal = []
    for i in range(1, 13):
        print(BASE_URL+str(i))
        journal.extend(parse(get_html(BASE_URL + str(i))))

    save(journal, 'gismeteo.csv')


if __name__ == '__main__':
    main()
