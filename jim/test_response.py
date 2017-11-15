import json

from response import Response


def test_create():
    response = Response(b'{"message": "Test message"}')
    assert response.request_text() == 'Test message'


def test_decode():
    response = Response(b'{"message": "Test message"}')
    assert response.request() == {"message": "Test message"}


def test_reply():
    response = Response(b'{"message": "Test message"}')
    assert json.loads(response.pack().decode())['message'] == 'Ответ сервера на сообщение - Test message'
