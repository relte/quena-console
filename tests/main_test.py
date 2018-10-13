from app.cli import main
from expects import *
from io import StringIO
from unittest.mock import patch


def it_outputs_answers_based_on_user_input(when):
    when('builtins').input('What are you looking for? ~Quena\n').thenReturn('A')
    when('app.cli.ApiClient').search_answers('A').thenReturn([
        {
            'id': 1,
            'entry': 'A?',
            'content': '*B*'
        }
    ])

    with patch('sys.stdout', StringIO()) as stdout:
        main()
        output = stdout.getvalue().strip()
        expect(output).to(equal('A?\n--\n\x1b[03mB\x1b[03m\x1b[39;49;00m'))


def it_outputs_answers_based_on_an_argument(when):
    with patch('sys.argv', ['cli.py', 'A']):
        when('app.cli.ApiClient').search_answers('A').thenReturn([
            {
                'id': 1,
                'entry': 'A?',
                'content': 'B'
            }
        ])

        with patch('sys.stdout', StringIO()) as stdout:
            main()
            output = stdout.getvalue().strip()
            expect(output).to(equal('A?\n--\nB'))
