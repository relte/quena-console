import requests
import consolemd
import sys
from urllib.parse import urljoin


class ApiClient:
    def __init__(self, base_url):
        self.__base_url = base_url

    def search_answers(self, phrase):
        url = urljoin(self.__base_url, '/api/answers.json?entry=%s')
        return requests.get(url % phrase).json()


def main():
    client = ApiClient('http://localhost:8000/')

    if (len(sys.argv) > 1):
        phrase = sys.argv[1]
    else:
        phrase = input('What are you looking for? ~Quena\n')

    renderer = consolemd.Renderer()

    print('\n')
    for answer in client.search_answers(phrase):
        print(answer['entry'])
        print('-' * len(answer['entry']))
        renderer.render(answer['content'])
        print('\n')


if __name__ == '__main__':
    main()
