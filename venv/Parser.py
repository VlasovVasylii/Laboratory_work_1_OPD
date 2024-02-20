from bs4 import BeautifulSoup # импортируем библиотеку BeautifulSoup
import requests # импортируем библиотеку requests
from fake_useragent import UserAgent # импортируем фейкового юзер-агента
import re # импортируем библиотеку для работы с регулярками
from itertools import count # импортируем бесконечный счётчик


def parse():
    url = 'https://www.pepper.ru/' # передаем необходимы URL адреса
    ind = 1

    for i in count(1): # перебираем страницы
        try:
            page = requests.get( # отправляем запрос методом Get на данный адрес и получаем ответ в переменную
                url + ("" if i == 1 else f"?page={i}"),
                headers={'User-Agent': UserAgent().chrome}
            )
        except requests.RequestException: # прекращаем работу
            break

        soup = BeautifulSoup(page.text, "html.parser") # передаем страницу в bs4

        blocks = soup.findAll('div', class_='threadGrid thread-clickRoot') # находим  контейнеры с нужным классом

        for block in blocks: # бегаем по все акциям
            stock = f"Акция номер {ind}\n"

            try: # пытаемся достать нужную информацию
                stock += "Ссылка: " + block.a['href'] + "\nНазвание акции: " + block.a['title'] + "\nКоличество градусов: "
            except KeyError: # если не нашли нужного аттрибута, то способ получения названия акции
                try:
                    stock += "Ссылка: " + block.a['href'] + "\nНазвание акции: " + \
                             block.find('h1', class_="size--all-xl size--fromW3-xxl text--b space--mb-1 space--fromW3-mb-0 text--color-charcoalShade")\
                             + "\nКоличество градусов: "
                except TypeError: # если не нашли нужную информацию, то пропускаем этот блок, так как в этом блоке содержится информация про купоны
                    continue
            except TypeError: # если не нашли нужную информацию, то пропускаем этот блок, так как в этом блоке содержится информация про купоны
                continue

            tmps = [
                block.find('span', class_=re.compile(r"cept-vote-temp vote-temp vote-temp--[a-zA-Z]*")),
                block.find('span', class_="cept-vote-temp vote-temp text--color-charcoal"),
                block.find('span', class_="space--h-2 text--b")
            ]

            for tmp in tmps: # перебираем возможные классы у span-а
                if tmp is not None:
                    stock += tmp.string.strip()
                    break
            else:
                continue # если ни один класс не подошёл переходим на следующую итерацию цикла

            print(stock, end='\n\n')

            ind += 1
