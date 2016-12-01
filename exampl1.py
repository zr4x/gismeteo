import urllib.request
from bs4 import BeautifulSoup


def get_html(url):
    response = urllib.request.urlopen(url)
    return response.read()


def month(html):
    soup = BeautifulSoup(html, "html.parser")
    table = soup.find('div', class_='cover png')
    month = table.find('h1')
    return print(month.text[32:])


def parse(html):
    soup = BeautifulSoup(html, "html.parser")
    table = soup.find('table')

    journals = []

    for row in table.find_all('tr')[2:]:
        cols = row.find_all('td')

        journals.append({
            # 'month': ,
            'date': cols[0].text,
            'weather day': cols[1].text,
            'pressure': cols[2].text,
            'weather night': cols[6].text,
            'pressure night': cols[7].text
        })
    return journals


def save(journals, name):
    with open(name, 'w') as f:
        f.write(journals)


def main():
    for month_id in range(1, 13):
        month(get_html('https://www.gismeteo.ru/diary/4565/2016/{}/'.format(month_id)))
        parse(get_html('https://www.gismeteo.ru/diary/4565/2016/{}/'.format(month_id)))



if __name__ == '__main__':
    main()