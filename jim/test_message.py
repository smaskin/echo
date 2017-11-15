import json

from message import Message


def test_common():
    message = Message('Test message')
    assert message.dict == {"message": "Test message"}
    assert json.loads(message.pack().decode())['message'] == 'Test message'
