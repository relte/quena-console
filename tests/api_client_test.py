from app.cli import ApiClient
from expects import *
import responses

def it_retrieves_answers_filtered_with_a_phrase():
    with responses.RequestsMock() as requests_mock:
        test_json = [
            {
                'id': 1,
                'question': 'A?',
                'content': 'B'
            }
        ]

        mock_response(
            requests_mock,
            'http://localhost:8000/api/answers.json?question=a',
            test_json
        )

        client = ApiClient('http://localhost:8000')

        expect(client.search_answers('a')).to(equal(test_json))


def mock_response(requests_mock, url, json, status=200):
    requests_mock.add(
        responses.Response(
            method='GET',
            url=url,
            json=json,
            status=status,
            content_type='application/json',
            match_querystring=True
        )
    )
