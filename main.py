import collections
import datetime
from http.server import HTTPServer, SimpleHTTPRequestHandler

import pandas
from jinja2 import Environment, FileSystemLoader, select_autoescape


def catalog_from_excel():
    drinks_catalog = pandas.read_excel(
        "goods.xlsx",
        sheet_name='Лист1',
        usecols=['Категория', 'Название', 'Сорт', 'Цена', 'Картинка', 'Акция'],
        na_values=['N/A', 'NA'],
        keep_default_na=False
    ).sort_values('Категория').to_dict(orient='records')

    formatted_drinks_catalog = collections.defaultdict(list)
    for drink in drinks_catalog:
        formatted_drinks_catalog[drink['Категория']].append(drink)
    return formatted_drinks_catalog


def get_age():
    year_foundation = 1920
    age = datetime.datetime.now().year - year_foundation
    if age % 10 == 1 and age % 100 != 11:
        return f'{age} год'
    if age % 10 in [2, 3, 4] and not (age % 100 in [12, 13, 14]):
        return f'{age} года'
    return f'{age} лет'


def main():
    env = Environment(
        loader=FileSystemLoader('.'),
        autoescape=select_autoescape(['html', 'xml'])
    )

    template = env.get_template('template.html')

    rendered_page = template.render(
        age_text=get_age(),
        drinks_catalog=catalog_from_excel(),
    )

    with open('index.html', 'w', encoding="utf8") as file:
        file.write(rendered_page)

    server = HTTPServer(('0.0.0.0', 8000), SimpleHTTPRequestHandler)
    server.serve_forever()


if __name__ == '__main__':
    main()
