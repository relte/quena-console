from app.cli import main
from expects import *


def it_outputs_answers_based_on_user_input(when, capsys):
    when('builtins').input('What are you looking for? ~Quena\n').thenReturn('A')
    when('app.cli.ApiClient').search_answers('A').thenReturn([
        {
            'id': 1,
            'entry': 'A?',
            'content': '*B*'
        }
    ])

    main()
    output, _ = capsys.readouterr()
    expect(output).to(equal('\nA?\n--\n\x1b[03mB\x1b[03m\x1b[39;49;00m\n\n'))


def it_outputs_answers_based_on_an_argument(when, mocker, capsys):
    mocker.patch('sys.argv', ['cli.py', 'A'])
    when('app.cli.ApiClient').search_answers('A').thenReturn([
        {
            'id': 1,
            'entry': 'A?',
            'content': 'B'
        }
    ])

    main()
    output, _ = capsys.readouterr()
    expect(output).to(equal('\nA?\n--\nB\n\n'))
