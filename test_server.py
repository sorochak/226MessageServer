import pytest
import subprocess
import time

def stop_container():
    print('\n\n')
    cmd = subprocess.run(['sudo', 'docker', 'stop', '226-message-server'], capture_output=True)
    print(cmd)
    cmd = subprocess.run(['sudo', 'docker', 'rm', '226-message-server'], capture_output=True)
    print(cmd)

def setup_module(module):
    stop_container()
    cmd = subprocess.run(['sudo', 'docker', 'build', '-t', '226-message-server', '.'], capture_output=True)
    print(cmd)
    cmd = subprocess.run(['sudo', 'docker', 'run', '-d', '--name', '226-message-server', '-p', '12345:12345', '226-message-server'], capture_output=True)
    print(cmd)
    time.sleep(5) # Ugly; should properly detect when the container is up and running
    print('\n\n')

def teardown_module(module):
    stop_container()
    print('\n\n')

def transmit(message):
    print('----\n')
    input = subprocess.Popen(['echo', message], stdout=subprocess.PIPE)
    print('>', input.args)
    output= subprocess.check_output(['nc', '127.0.0.1', '12345'], stdin=input.stdout)
    print('<', output)
    return output

def test_invalid_command():
    output = transmit('Test')
    assert output == b'NO\n'

def test_missing_key_for_put():
    output = transmit('PUT')
    assert output == b'NO\n'

def test_invalid_key_for_put():
    key = 'PUT'
    for i in range(7):
        key = key + str(i)
        output = transmit(key)
        assert output == b'NO\n'

def test_valid_key():
    output = transmit('PUTabcdefghThis is a test')
    assert output == b'OK\n'
    
    output = transmit('GETabcdefgh')
    assert output == b'This is a test\n'

def test_missing_key_for_get():
    print()
    output = transmit('GET')
    assert output == b'\n'

def test_invalid_key_for_get():
    print()
    key = 'GET'
    for i in range(10):
        key = key + str(i)
        output = transmit(key)
        assert output == b'\n'

def test_message_size():
    print()
    putKey = 'PUTijklmnop'
    getKey = 'GETijklmnop'
    putMsg = ''
    for i in range(160):
        putMsg = putMsg + str(i % 10)
        output = transmit(putKey + putMsg)
        assert output == b'OK\n'

        output = transmit(getKey)
        assert output == (putMsg + '\n').encode('utf-8')

    output = transmit(putKey + putMsg + 'X')
    assert output == b'NO\n'

    output = transmit(getKey)
    assert output == (putMsg + '\n').encode('utf-8')

