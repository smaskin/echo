import console

DEFAULT_SERVER = (console.DEFAULT_IP, console.DEFAULT_PORT)


def test_argv():
    assert console.host_params(['server.py']) == DEFAULT_SERVER
    assert console.host_params(['server.py', '192.168.0.1']) == ('192.168.0.1', DEFAULT_SERVER[1])
    assert console.host_params(['server.py', '192.168.0.1', 8888]) == ('192.168.0.1', 8888)

    assert console.host_params(['client.py'], True) == DEFAULT_SERVER
    assert console.host_params(['client.py', '-a', '192.168.0.1'], True) == ('192.168.0.1', DEFAULT_SERVER[1])
    assert console.host_params(['client.py', '-p', 9999], True) == (DEFAULT_SERVER[0], 9999)
