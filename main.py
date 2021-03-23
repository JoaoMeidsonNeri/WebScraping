import requests
import csv
from bs4 import BeautifulSoup


def generate(product):

    # Monta url de busca do produto
    def search(name):
        url = f'https://www.amazon.com.br/s?k={name}&__mk_pt_BR=%C3%85M%C3%85%C5%BD%C3%95%C3%91&ref=nb_sb_noss_2'
        return url

    html = requests.get(search(product)).content
    soup = BeautifulSoup(html, 'html.parser')
    results = soup.find_all('div', {'data-component-type': 's-search-result'})

    # Extrai o nome e o valor dos produtos na página
    def extract(item):
        tag = item.h2.a
        item_name = tag.text.strip()

        try:
            price_parent = item.find('span', 'a-price')
            price = price_parent.find('span', 'a-offscreen').text

        except AttributeError:
            return

        result = (item_name, price)
        return result

    records = []
    for item in results:
        record = extract(item)
        if record:
            records.append(record)

    with open('Results.csv', 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['Produto', 'Preço'])
        writer.writerows(records)
        print('Planilha gerada')


generate('ps4')
