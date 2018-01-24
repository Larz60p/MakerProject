import RfcPaths
import requests
import CheckInternet
import sys


class GetUrl:
    def __init__(self):
        self.rpath = RfcPaths.RfcPaths()
        self.ci = CheckInternet.CheckInternet()
        self.ok_status = 200
        self.r = None

    def fetch_url(self, url):
        self.r = None
        if self.ci.check_availability():
            self.r = requests.get(url, allow_redirects=False)
        return self.r


def testit():
    gu = GetUrl()
    page = gu.fetch_url('https://www.google.com/')
    count = 0
    maxcount = 20
    try:
        if page.status_code == 200:
            ptext = page.text.split('/n')
            for line in ptext:
                print(f'{line}\n')
                count += 1
                if count > maxcount:
                    break
        else:
            print(f'Error retreving file status code: {page.status_code}')
    except AttributeError:
        print('Please enable internet and try again')

if __name__ == '__main__':
    testit()
