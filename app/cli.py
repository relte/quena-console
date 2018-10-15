import sys

import click
import consolemd
import requests
import validators
from configparser import ConfigParser
from pathlib import Path
from urllib.parse import urljoin

if getattr(sys, 'frozen', False):
    config_path = sys._MEIPASS / Path('app/config.ini')
else:
    config_path = Path('app/config.ini')


class ApiClient:
    def __init__(self, base_url):
        self.__base_url = base_url

    def search_answers_for(self, phrase):
        url = urljoin(self.__base_url, '/api/answers.json?entry=%s')
        response = requests.get(url % phrase)
        response.raise_for_status()

        return response.json()


def set_api_url(ctx, param, value):
    if not value or ctx.resilient_parsing:
        return

    if validators.url(value):
        config = get_config()
        config['api']['base_url'] = value
        with open(config_path, 'w') as configfile:
            config.write(configfile)
    else:
        print('The provided URL is incorrect.')

    ctx.exit()


def show_api_url(ctx, param, value):
    if not value or ctx.resilient_parsing:
        return

    config = get_config()
    print(config['api']['base_url'])

    ctx.exit()


def get_config():
    config = ConfigParser()
    config.read(config_path)

    return config


@click.command()
@click.option('--url',
              is_flag=True,
              expose_value=False,
              is_eager=True,
              callback=show_api_url,
              help="Show the API base URL and exit.")
@click.option('--set-url',
              expose_value=False,
              is_eager=True,
              callback=set_api_url,
              help="Set the API base URL and exit. Example: https://quena.yourdomain.com")
@click.argument('phrase', required=False)
def main(phrase):
    if (phrase == None):
        phrase = input('What are you looking for? ')

    config = get_config()
    client = ApiClient(config['api']['base_url'])

    try:
        answers = client.search_answers_for(phrase)
        if not answers:
            print('No answers found.')
        else:
            print_answers(answers)
    except requests.exceptions.RequestException:
        print('Could not retrieve answers. Please make sure you use a correct API base URL.')


def print_answers(answers):
    renderer = consolemd.Renderer()
    print()
    for answer in answers:
        print_answer(answer, renderer)


def print_answer(answer, renderer):
    print(answer['entry'])
    print('-' * len(answer['entry']))
    renderer.render(answer['content'])
    print()


if __name__ == '__main__':
    main()
