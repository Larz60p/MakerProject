from pathlib import Path
import os


class RfcPaths:
    def __init__(self):
        # Directory paths assure required paths exist
        self.prev_cwd = None
        self.homepath = Path('.')
        self.datapath = self.homepath / 'data'
        self.datapath.mkdir(exist_ok=True)
        self.htmlpath = self.datapath / 'html'
        self.htmlpath.mkdir(exist_ok=True)
        self.jsonpath = self.datapath / 'json'
        self.jsonpath.mkdir(exist_ok=True)
        self.textpath = self.datapath / '/text'
        self.textpath.mkdir(exist_ok=True)
        # self.miscpath = self.datapath / 'MiscData'
        # self.miscpath.mkdir(exist_ok=True)
        # self.pdfpath  = self.datapath / 'pdf'
        # self.pdfpath.mkdir(exist_ok=True)
        # self.samplepath = self.datapath / 'sampledata'
        # self.samplepath.mkdir(exist_ok=True)
        self.temppath = self.datapath / 'temp'
        self.temppath.mkdir(exist_ok=True)
        self.imagepath = self.homepath / 'images'
        self.imagepath.mkdir(exist_ok=True)

        # File paths
        self.text_index = self.textpath / 'rfc-index.txt'
        # self.ien_index = self.miscpath / 'ien_index.txt'
        # self.bcp_index = self.miscpath / 'bcp_index.txt'
        # self.testdoc = self.samplepath / 'rfc110.pdf'
        # self.pdf_index_file = self.pdfpath / 'rfc-index.txt.pdf'
        self.imagedict = self.jsonpath / 'images.json'
        self.text_test_file = self.temppath / 'text.txt'
        self.pdf_test_file = self.temppath / 'pdf.txt'
        self.ps_test_file = self.temppath / 'ps.txt'

        self.rfc_index_html = self.htmlpath / 'rfc_index.html'
        self.rfc_int_std_html = self.htmlpath / 'int_std_index.html'
        self.rfc_filepage = self.htmlpath / 'file_info.html'
        self.rfc_download_dir_html = self.htmlpath / 'download.html'

        self.rfc_index_json = self.jsonpath / 'rfc_index.json'

        # url's
        self.rfc_index_url = 'https://www.rfc-editor.org/rfc-index.html'
        self.int_standards_url = 'https://www.rfc-editor.org/search/rfc_search_detail.php?sortkey=Number' \
                                 '&sorting=DESC&page=All&pubstatus%5B%5D=Standards%20Track&std_trk=Internet' \
                                 '%20Standard'
        self.base_rfc_url = 'https://www.rfc-editor.org/info/'
        self.sitemap_url ='https://www.rfc-editor.org/sitemap/'
        self.rfc_download_page_url = 'https://www.rfc-editor.org/rfc/'
        self.pdfrfc_download_page_url = 'https://www.rfc-editor.org/rfc/pdfrfc/'
        self.std_download_page_url = 'https://www.rfc-editor.org/rfc/std/'
        self.bcp_download_page_url = 'https://www.rfc-editor.org/rfc/bcp/'
        self.fyi_download_page_url = 'https://www.rfc-editor.org/rfc/fyi/'
        self.ien_download_page_url = 'https://www.rfc-editor.org/rfc/ien/'
        self.ien__pdf_download_page_url = 'https://www.rfc-editor.org/rfc/ien/scanned/'
        self.rfc_ref_index = f'{self.rfc_download_page_url}rfc-ref.txt.new'


def testit():
    rp = RfcPaths()
    print(f'{[x for x in rp.datapath.iterdir()]}')
    print(f'{[x for x in rp.imagepath.iterdir()]}')
    print(f'{rp.imagepath.resolve()}')

if __name__ == '__main__':
    testit()
