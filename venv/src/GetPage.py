import GetUrl
import time
import sys


class GetPage:
    def __init__(self):
        """
        Initalize - Instantiate imported modules, initialize class variables
        """
        self.elapsed_hours = 0
        self.gu = GetUrl.GetUrl()
        self.savefile = None

    def get_page(self, url, savefile=None, refresh_hours_every=48):
        self.url = url
        self.savefile = savefile
        self.refresh_hours_every = refresh_hours_every
        self.page = None
        if self.savefile:
            if self.savefile.exists():
                lstats = savefile.lstat()
                self.elapsed_hours = (time.time() - lstats.st_mtime) / 3600
                if lstats.st_size == 0 or (self.elapsed_hours > self.refresh_hours_every):
                    self.page = self.download_new_file()
                else:
                    with self.savefile.open('r') as f:
                        self.page = f.read()
            else:
                self.page = self.download_new_file()
        else:
            self.page = self.download_new_file()
        return self.page


    def download_new_file(self):
        page = None
        try:
            page = self.gu.fetch_url(self.url)
            if page.status_code == 200:
                with self.savefile.open('wb') as f:
                    f.write(page.content)
            else:
                print(f'Invalid status code: {page.st}')
        except AttributeError:
            print('Please enable internet and try again')
        return page

def testit():
    import RfcPaths
    rpath = RfcPaths.RfcPaths()
    # Test url = rfc index download page, save to data/html/rfc_index.html, refresh always
    gp = GetPage()
    page = gp.get_page(url=rpath.rfc_download_page_url, savefile=rpath.rfc_index_html,
                       refresh_hours_every=0)
    if page:
        if page.status_code == 200:
            print(f'Page contents: {page.text}')
        else:
            print('Page is empty or in')

if __name__ == '__main__':
    testit()
