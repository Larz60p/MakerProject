import RfcPaths
import GetPage
import GetUrl
import json
import GetRemoteDir
from bs4 import BeautifulSoup


class CreateRfcIndex:
    def __init__(self):
        self.rpath = RfcPaths.RfcPaths()
        self.gp = GetPage.GetPage()
        self.gu = GetUrl.GetUrl()
        self.pno = 0
        self.page = self.get_rfc_index()
        if self.page is not None:
            self.text_index = {}
            self.create_rfc_text_index()

    def get_rfc_index(self):
        url = self.rpath.rfc_index_url
        save = self.rpath.rfc_index_html
        refresh_hrs = 1
        document = self.gp.get_page(url=url, savefile=save, refresh_hours_every=refresh_hrs)
        return document

    def create_rfc_text_index(self):
        """
        Parse rfc_index from rfc-editor.org, create a dictionary and save as json file
        :return: None
        """
        with self.rpath.rfc_index_html.open('rb') as f:
            page = f.read()
        soup = BeautifulSoup(page, 'lxml')

        tr_list = soup.select('tr')

        for tr in tr_list:
            td_list = tr.select('td')
            if td_list[0].find('script'):
                self.extract_data(td_list)

        self.add_file_links()

        with self.rpath.rfc_index_json.open('w') as temp:
            json.dump(self.text_index, temp)

    def get_file_locations(self):
        grd = GetRemoteDir.GetRemoteDir()
        self.text_files = grd.list_file_descriptor(url=self.rpath.rfc_download_page_url,
                                              savefile=self.rpath.rfc_download_dir_html, suffix='txt')
        self.pdf_files = grd.list_file_descriptor(url=self.rpath.rfc_download_page_url,
                                             savefile=self.rpath.rfc_download_dir_html, suffix='pdf')
        self.postscript_files = grd.list_file_descriptor(url=self.rpath.rfc_download_page_url,
                                                    savefile=self.rpath.rfc_download_dir_html, suffix='ps')

    def add_file_links(self):
        self.get_file_locations()
        for key, value in self.text_index.items():
            abbreviated_key = f'rfc{int(key[3:])}'
            filename = f'{abbreviated_key}.txt'
            if filename in self.text_files:
                self.text_index[key]['text_file'] = f'{self.rpath.rfc_download_page_url}{filename}'
            filename = f'{abbreviated_key}.pdf'
            if filename in self.pdf_files:
                self.text_index[key]['pdf_file'] = f'{self.rpath.rfc_download_page_url}{filename}'
            filename = f'{abbreviated_key}.ps'
            if filename in self.postscript_files:
                self.text_index[key]['ps_file'] = f'{self.rpath.rfc_download_page_url}{filename}'

    def extract_data(self, tds):
        """
        Extract data from soup, building dictionary along the way
        :param tds: list of all td's of proper type
        :return: None
        """
        for n, td in enumerate(tds):
            if td is None:
                continue
            if n == 0:
                item_dict = self.extract_header(td)
            else:
                item_dict['title'] = td.find('b').text
                lines = td.text.strip().split('\n')
                lines = list(map(str.strip, lines))
                lines[0] = lines[0][len(item_dict['title']):]
                item_dict['authors'] = lines[0]
                del lines[0]
                self.get_remaining_fields(lines, item_dict)

    def extract_header(self, td):
        """
        Extract the RFC number from the id script
        :param td: td containing script
        :return: key entry of dictionary entry
        """
        rfc_id = td.text[td.text.index('(') + 2:td.text.index(')') - 1]
        self.text_index[rfc_id] = {}
        return self.text_index[rfc_id]

    @staticmethod
    def get_remaining_fields(lines, item_dict):
        """
        Extracts remaining fields and adds them to the dictionary
        :param lines: list of lines from td
        :param item_dict: dictionary key for rfc
        :return: None
        """
        multi = False
        dtag = None
        dtext = None
        mm = False
        for item in lines:
            if item == '':
                continue
            if multi or item.startswith('('):
                # multi line entry
                if item.startswith('('):
                    if multi:
                        item_dict[dtag] = dtext
                    multi = False
                if multi:
                    if '\>)' in item:
                        multi = False
                        item_dict[dtag] = dtext
                        continue
                    if item.startswith('do'):
                        if mm:
                            nd = item[item.index("('")+2:item.index("')")]
                            dtext = f'{dtext}, {nd}'
                        else:
                            dtext = item[item.index("('")+2:item.index("')")]
                            mm = True
                    continue
                if ')' not in item:
                    dtag = item[item.index('(')+1:]
                    multi = True
                    mm = False
                    continue
                # Two formats, with ':' or with '='
                item = item[1:item.index(')')]
                if '=' in item:
                    item = item.split()
                    item_dict['type'] = item[0].lower()
                    item_dict['size'] = item[2]
                else:
                    item = item.split(': ')
                    item_dict[item[0].lower()] = item[1]
            elif item.startswith('['):
                item_dict['pub_date'] = item[item.index('[')+1:item.index(']')-1].strip()
            else:
                print('oddball found: {item}')


if __name__ == '__main__':
    CreateRfcIndex()
