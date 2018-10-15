import pytest
from click.testing import CliRunner
from expects import *

from app.cli import main


def it_outputs_answers_based_on_user_input(when):
    when('builtins').input('What are you looking for? ').thenReturn('A')
    when('app.cli.ApiClient').search_answers_for('A').thenReturn([
        {
            'id': 1,
            'entry': 'A?',
            'content': '*B*'
        }
    ])

    runner = CliRunner()
    result = runner.invoke(main, [])

    expect(result.output).to(equal('\nA?\n--\n\x1b[03mB\x1b[03m\x1b[39;49;00m\n\n'))


def it_outputs_answers_based_on_an_argument(when):
    when('app.cli.ApiClient').search_answers_for('A').thenReturn([
        {
            'id': 1,
            'entry': 'A?',
            'content': 'B'
        }
    ])

    runner = CliRunner()
    result = runner.invoke(main, ['A'])

    expect(result.output).to(equal('\nA?\n--\nB\n\n'))


def it_shows_quena_default_api_base_url():
    runner = CliRunner()
    result = runner.invoke(main, ['--url'])

    expect(result.output).to(equal('http://localhost:8000\n'))


@pytest.mark.parametrize('example_url', [
    'https://quena.com',
    'http://quena.xyz',
    'https://quena.example.com'
])
def it_lets_user_change_quena_api_base_url(fs, example_url):
    fs.create_file('app/config.ini', contents='[api]\nbase_url=http://localhost:8000')

    runner = CliRunner()
    runner.invoke(main, ['--set-url', example_url])

    result = runner.invoke(main, ['--url'])
    expect(result.output).to(equal(example_url + '\n'))


@pytest.mark.parametrize('incorrect_example_url', [
    'some_string',
    'file://localhost/home/example.html',
    'quena.example.com'
])
def it_does_not_let_user_to_set_incorrect_api_base_url(fs, incorrect_example_url):
    fs.create_file('app/config.ini', contents='[api]\nbase_url=http://localhost:8000')

    runner = CliRunner()
    result = runner.invoke(main, ['--set-url', incorrect_example_url])
    expect(result.output).to(equal('The provided URL is incorrect.\n'))

    result = runner.invoke(main, ['--url'])
    expect(result.output).to(equal('http://localhost:8000\n'))


def it_informs_the_user_if_it_cannot_retrieve_answers(when):
    import requests
    when(requests) \
        .get('http://localhost:8000/api/answers.json?entry=a') \
        .thenRaise(requests.exceptions.RequestException)

    runner = CliRunner()
    result = runner.invoke(main, ['a'])

    expect(result.output).to(equal('Could not retrieve answers. Please make sure you use a correct API base URL.\n'))


def it_informs_the_user_if_no_answers_were_found_for_the_phrase(when, unstub):
    import requests
    from mockito import mock

    response = mock(spec=requests.Response)
    when(response).json().thenReturn([])
    when(requests).get('http://localhost:8000/api/answers.json?entry=c').thenReturn(response)

    runner = CliRunner()
    result = runner.invoke(main, ['c'])

    expect(result.output).to(equal('No answers found.\n'))
