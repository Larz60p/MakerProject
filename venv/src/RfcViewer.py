#!/usr/bin/python
# See for pdf: https://wxpython.org/Phoenix/docs/html/wx.lib.pdfviewer.html#module-wx.lib.pdfviewer
import wx
import fitz
from wx.lib.pdfviewer import pdfViewer, pdfButtonPanel
import wx.aui as aui
import wx.lib.agw.aui as aui
import RfcPaths
import json
# import CheckInternet
import requests


class MainPanel(wx.Panel):
    """
    Just a simple derived panel where we override Freeze and Thaw to work
    around an issue on wxGTK.
    """
    def Freeze(self):
        if 'wxMSW' in wx.PlatformInfo:
            return super(MainPanel, self).Freeze()

    def Thaw(self):
        if 'wxMSW' in wx.PlatformInfo:
            return super(MainPanel, self).Thaw()


class RfcViewer(wx.Frame):
    def __init__(self, parent, id=wx.ID_ANY, title="Rfc Viewer", pos=wx.DefaultPosition,
                 size=(800, 600), style=wx.DEFAULT_FRAME_STYLE, name='RfcViewer'):
        """
        Initialize - inherits from wx.Frame. Instantiates all widgets and variables for application

        :param parent: (wx.Window) The window parent. This may be, and often is, None. If it is not None, the frame
                       will be minimized when its parent is minimized and restored when it is restored (although it
                       will still be possible to minimize and restore just this frame itself).

        :param id:     (wx.WindowID) The window identifier. It may take a value of -1 to indicate a default value.

        :param title:  (string)  The caption to be displayed on the frame’s title bar.

        :param pos:    (wx.point) The window position. The value DefaultPosition indicates a default position,
                       chosen by either the windowing system or wxWidgets, depending on platform.

        :param size:   (wx.Size) – The window size. The value DefaultSize indicates a default size, chosen by either
                       the windowing system or wxWidgets, depending on platform.

        :param style:  (long) – The window style. See wx.Frame class description.

        :param name:   (string) The name of the window. This parameter is used to associate a name with the item,
                       allowing the application user to set Motif resource values for individual windows.
        """
        wx.Frame.__init__(self,
                          parent,
                          id,
                          title,
                          pos,
                          size,
                          style)
        print(f'PyMuPDF version: {fitz.__doc__}')
        self.rpath = RfcPaths.RfcPaths()
        self.rfc_document_data = None

        with self.rpath.rfc_index_json.open() as f:
            self.rfc_index = json.load(f)

        self.pnl = pnl = MainPanel(self)
        self._mgr = aui.AuiManager(pnl)

        # notify AUI which frame to use
        self._mgr.SetManagedWindow(self)

        # First pane is Rfc Selection window located top left
        # ----+----+----+----+----+----+----+----+----+----+----+----+----+----+----+----+----+----+
        self.rfc_selector = wx.ListCtrl(self,
                                        id=wx.ID_ANY,
                                        pos=wx.DefaultPosition,
                                        size=wx.Size(200, 150),
                                        style=wx.NO_BORDER | wx.TE_MULTILINE,
                                        name='RfcSelector')

        self.rfc_selector.InsertColumn(0, 'RFC Id', width=60)
        self.rfc_selector.InsertColumn(1, 'Title', width=200)

        self.rfc_selector.SetMinSize(wx.Size(500, 300))
        self.rfc_selector.SetMaxSize(wx.Size(1000, 800))

        # Need to distinguish between single and double click so
        self.rfc_id = None

        self.dbl_clk_delay = 250
        self.rfc_selector.Bind(wx.EVT_LIST_ITEM_FOCUSED, self.run_summary)
        self.rfc_selector.Bind(wx.EVT_LEFT_DCLICK, self.display_detail)

        self.rfc_selector_load()

        # Second pane is Rfc Summary window Data displayed in this window on single click in
        # selection window.
        # ----+----+----+----+----+----+----+----+----+----+----+----+----+----+----+----+----+----+
        self.summary = wx.TextCtrl(self,
                                   id=wx.ID_ANY,
                                   value="Pane 2 - Summary Text Here",
                                   pos=wx.DefaultPosition,
                                   size=wx.Size(200, 150),
                                   style=wx.NO_BORDER | wx.TE_MULTILINE,
                                   name='RfcSummary')

        # Third pane (left top)  is a two tab notebook, one for text files and one for pdf files. One
        # or both may be populated for any given RFC document.
        # ----+----+----+----+----+----+----+----+----+----+----+----+----+----+----+----+----+----+
        self.nb = aui.AuiNotebook(self,
                                  id=wx.ID_ANY,
                                  pos=wx.DefaultPosition,
                                  size=wx.DefaultSize,
                                  style=0,
                                  agwStyle=wx.lib.agw.aui.AUI_NB_DEFAULT_STYLE,
                                  name="RfcDocumentNotebook")

        self.text_page = wx.TextCtrl(self.nb,
                                     id=wx.ID_ANY,
                                     pos=wx.DefaultPosition,
                                     size=wx.DefaultSize,
                                     style=wx.NO_BORDER | wx.TE_MULTILINE,
                                     name='DetailNotebookTabs')

        self.pdf_page = wx.Panel(self.nb,
                                 id=wx.ID_ANY,
                                 pos=wx.DefaultPosition,
                                 size=wx.DefaultSize,
                                 style=wx.TAB_TRAVERSAL,
                                 name='pdfpage')

        # hsizer = wx.BoxSizer(wx.HORIZONTAL)
        # vsizer = wx.BoxSizer(wx.VERTICAL)
        #
        # self.btnpanl = pdfButtonPanel(self.pdf_page,
        #                               nid=wx.ID_ANY,
        #                               pos=wx.DefaultPosition,
        #                               size=wx.DefaultSize,
        #                               style=None)
        #
        # vsizer.Add(self.btnpanl, 0, wx.GROW | wx.ALIGN_CENTER_VERTICAL | wx.LEFT | wx.RIGHT | wx.TOP, 5)
        #
        # self.viewer = pdfViewer(self.pdf_page,
        #                         nid=wx.ID_ANY,
        #                         pos=wx.DefaultPosition,
        #                         size=wx.DefaultSize,
        #                         style=wx.HSCROLL | wx.VSCROLL | wx.VSCROLL | wx.SUNKEN_BORDER)
        #
        # vsizer.Add(self.viewer, 1, wx.GROW | wx.LEFT | wx.RIGHT | wx.BOTTOM, 5)
        # hsizer.Add(vsizer, 1, wx.GROW | wx.ALIGN_CENTER_HORIZONTAL | wx.ALL, 5)
        #
        # self.SetSizer(hsizer)
        # self.SetAutoLayout(True)
        #
        # self.btnpanl.viewer = self.viewer
        # self.viewer.buttonpanel = self.btnpanl

        self.nb.AddPage(self.text_page, "Text Document")
        self.nb.AddPage(self.pdf_page, "PDF Document")

        self._mgr.AddPane(self.rfc_selector, aui.AuiPaneInfo().Left().Caption("RFC Selection"))
        self._mgr.AddPane(self.summary, aui.AuiPaneInfo().Bottom().Caption("RFC Summary"))
        self._mgr.AddPane(self.nb, aui.AuiPaneInfo().CenterPane().Name('RFC Detail'))

        # tell the manager to "commit" all the changes just made
        self._mgr.Update()

        self.Bind(wx.EVT_CLOSE, self.OnClose)

    def error_msg(self, message):
        """
        Display message in standard wx.MessageDialog
        :param message: (string) Value to be displayed
        :return: None
        """
        msg_dlg = wx.MessageDialog(self, message, '', wx.OK | wx.ICON_ERROR)
        msg_dlg.ShowModal()
        msg_dlg.Show()
        msg_dlg.Destroy()

    def display_detail(self, event):
        """
        Display the actual document. Improvement can be added to print from cache, and
        only fetch from web if not in cache. This would require a update manager which
        would check for new documents. Old documents are not changed at this time, so saving
        documents would not be a problem.

        Will display text documents in the text window. This is the desired mode, but if no text
        document is available, will use a pdf is available (displayed in a separate yab).
        :param event: The event that triggered this method.
        :return: None
        """
        # self.detail.Clear()
        file_format = None
        file_url = None
        print(f'RFC Id: {self.rfc_id}')

        try:
            file_url = self.rfc_index[self.rfc_id]['text_file']
            file_format = 'txt'
        except KeyError:
            try:
                file_url = self.rfc_index[self.rfc_id]['pdf_file']
                file_format = 'pdf'
            except:
                pass

        if file_format is None:
            self.text_page.AppendText("No URL listed for this file.")
        else:
            wx.BeginBusyCursor()
            self.rfc_document_data = self.download_file(file_url, file_format)
            if file_format == 'txt':
                # self.text_page = self.rfc_document_data
                for line in self.rfc_document_data:
                    self.text_page.AppendText(line)
            else:
                print('Pdf viewer not Yet Implemented')
                # self.viewer.LoadFile(fitz.open("pdf", self.rfc_document_data))
                # print(pdf_doc.metadata)
                # self.viewer.LoadFile(pdf_doc)
                # self.viewer.LoadFile(self.rfc_document_data)
            wx.EndBusyCursor()


    def run_summary(self, event):
        """
        Gets the data associated with single or double click in self.rfc_selector ListCtrl.
        calls display_summary to render information.
        :param event: The event that triggered this method.
        :return: None (keeps event with Skip, so double click will still work).
        """
        self.rfc_id = event.GetText()
        self.display_summary()
        event.Skip()

    def display_summary(self):
        """
        Display summary information in bottom pane. Called by run_summary event.
        :return: None
        """
        self.summary.Clear()
        for key, value in self.rfc_index[self.rfc_id].items():
            index = self.rfc_selector.GetItemCount()
            self.summary.AppendText(f'{key}: {value}\n')


    def rfc_selector_load(self):
        """
        Clears, then Loads self.rfc_selector ListCtrl with data from self.rfc_index dictionary.
        :return: None
        """
        self.rfc_selector.DeleteAllItems()
        for key, value in self.rfc_index.items():
            index = self.rfc_selector.GetItemCount()
            self.rfc_selector.InsertItem(index, key)
            self.rfc_selector.SetItem(index, 1, value['title'])

    @staticmethod
    def download_file(url, file_format):
        """
        Download Rfc document
        :return: document
        """
        ok_status = 200
        document = None
        print(f'url: {url}')
        doc = requests.get(url, allow_redirects=False)
        if doc.status_code != ok_status:
            print(f'status: {doc.status_code}')
        if doc:
            if file_format == 'txt':
                document = doc.text
            else:
                document = doc.content
        return document

    def OnClose(self, event):
        """
        Graceful exit, removes aui manager and reissues event
        :param event: The event that triggered this method.
        :return: None
        """
        # deinitialize the frame manager
        self._mgr.UnInit()
        event.Skip()


def main():
    """
    Instanciate and execute wx.App and RfcViewer
    :return:
    """
    app = wx.App()
    frame = RfcViewer(None)
    app.SetTopWindow(frame)
    frame.Show()
    app.MainLoop()

if __name__ == '__main__':
    main()
