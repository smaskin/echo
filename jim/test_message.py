import message


def test_create():
    pack = message.create('Test message')
    decoded = message.decode(pack)
    decoded.pop('time')
    assert decoded == {
        'message': 'Test message',
        'status': 200,
        'type': 'default'
    }


def test_encode():
    assert message.encode({'status': message.MESSAGE_STATUS_OK}) == b'{"status": 200}'


def test_decode():
    assert message.decode(b'{"status": 200}') == {'status': message.MESSAGE_STATUS_OK}
