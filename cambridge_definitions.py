import requests
import csv

from bs4 import BeautifulSoup

FILE_NAME = "raw_words_example.csv"

BASE_URL = 'https://dictionary.cambridge.org/search/english/direct/'
HEADERS = {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_3) '
                        'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'}

with open(FILE_NAME) as csv_input:
    word_reader = csv.reader(csv_input)

    with open('words.csv', mode='w+') as csv_output:
        for row in word_reader:
            word = row[0].strip().replace(" ", "+")

            response = requests.get(BASE_URL + f'?q={word}', headers=HEADERS)

            if response.status_code == 200:

                soup = BeautifulSoup(response.text, "html.parser")
                pronunciation = soup.find_all('span', {'class': 'ipa'})
                pronunciation = pronunciation[-1].text if pronunciation else ''

                variants = soup.find_all('div', {'class': 'sense-body'})

                for var in variants:
                    def_block = var.find_all('div', {'class': 'def-block'})
                    for d in def_block:

                        csv_output.write(f'"{word}","{d.text}",{pronunciation}\n')
