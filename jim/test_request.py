from request import Request


def test_common():
    response = Request(b'{"message": "Test message"}')
    assert response.dict == {"message": "Test message"}
    assert response.text == "Test message"
