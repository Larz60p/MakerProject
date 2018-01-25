import socket


class CheckInternet:
    def __init__(self):
        self.internet_available = False

    def check_availability(self):
        self.internet_available = False
        if socket.gethostbyname(socket.gethostname()) != '127.0.0.1':
            self.internet_available = True
        return self.internet_available


def testit():
    ci = CheckInternet()
    print('Please turn internet OFF, then press Enter')
    input()
    ci.check_availability()
    print(f'ci.internet_available: {ci.internet_available}')
    if not ci.internet_available:
        print('    Off test successful')
    else:
        print('    Off test failed')
    print('Please turn internet ON, then press Enter')
    input()
    ci.check_availability()
    print(f'ci.internet_available: {ci.internet_available}')
    if ci.internet_available:
        print('    On test successful')
    else:
        print('    On test failed')


if __name__ == '__main__':
    testit()
