import RfcPaths
import os
import wx


class FreshStart():
    def __init__(self):
        self.app = wx.App()
        self.rpath = RfcPaths.RfcPaths()
        val = self.warning('YOU ARE ABOUT TO DELETE ALL HTML AND JSON DATA')
        if val == wx.ID_OK:
            self.delete_data_files()

    def warning(self, message):
        """
        Display message in standard wx.MessageDialog
        :param message: (string) Value to be displayed
        :return: None
        """
        msg_dlg = wx.MessageDialog(None, message, '', wx.OK | wx.CANCEL| wx.ICON_ERROR)
        val = msg_dlg.ShowModal()
        msg_dlg.Show()
        msg_dlg.Destroy()
        return val

    def delete_data_files(self):
        # html_files = [x for x in self.rpath.htmlpath.iterdir() if x.is_file()]
        html_files = [x for x in self.rpath.htmlpath.iterdir() if x.is_file() and (x.name.endswith('.html')
                      or x.name.endswith('.htm'))]
        json_files = [x for x in self.rpath.jsonpath.iterdir() if x.is_file() and x.name.endswith('.json')]
        all_files = html_files + json_files
        print(f'all_files: {all_files}')
        for file in all_files:
            os.remove(file.resolve())

if __name__ == '__main__':
    FreshStart()
