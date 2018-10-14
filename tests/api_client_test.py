import requests
from expects import *
from mockito import mock

from app.cli import ApiClient


def it_retrieves_answers_filtered_with_a_phrase(when, unstub):
    test_json = [
        {
            'id': 1,
            'entry': 'A?',
            'content': 'B'
        }
    ]
    response = mock(spec=requests.Response)
    when(response).json().thenReturn(test_json)
    when(requests).get('http://localhost:8000/api/answers.json?entry=a').thenReturn(response)

    client = ApiClient('http://localhost:8000')

    expect(client.search_answers_for('a')).to(equal(test_json))
