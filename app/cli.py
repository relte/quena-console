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
        return requests.get(url % phrase).json()


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
              help="Show Quena API base URL and exit")
@click.option('--set-url',
              expose_value=False,
              is_eager=True,
              callback=set_api_url,
              help="Set Quena API base URL and exit")
@click.argument('phrase', required=False)
def main(phrase):
    if (phrase != None):
        show_answers_for(phrase)
    else:
        show_answers_for(input('What are you looking for? ~Quena\n'))


def show_answers_for(phrase):
    config = get_config()
    client = ApiClient(config['api']['base_url'])
    renderer = consolemd.Renderer()

    print()
    for answer in client.search_answers_for(phrase):
        show_answer(answer, renderer)


def show_answer(answer, renderer):
    print(answer['entry'])
    print('-' * len(answer['entry']))
    renderer.render(answer['content'])
    print()


if __name__ == '__main__':
    main()
