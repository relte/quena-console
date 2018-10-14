from click.testing import CliRunner
from expects import *

from app.cli import main


def it_outputs_answers_based_on_user_input(when):
    when('builtins').input('What are you looking for? ~Quena\n').thenReturn('A')
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


def it_lets_user_change_quena_api_base_url(fs):
    fs.create_file('app/config.ini', contents='[api]\nbase_url=http://localhost:8000')

    runner = CliRunner()
    runner.invoke(main, ['--set-url', 'https://quena.example'])

    result = runner.invoke(main, ['--url'])
    expect(result.output).to(equal('https://quena.example\n'))
