import wx
from convert_to_opus import converter
import os
import sys


class RedirectText(object):  # Redirects console output to wx panel
    def __init__(self, aWxTextCtrl):
        self.out = aWxTextCtrl

    def write(self, string):
        self.out.WriteText(string)


class windowClass(wx.Frame):
    def __init__(self, *args, **kw):
        super(windowClass, self).__init__(*args, **kw)
        self.Panel = Panel(self)
        self.SetMinSize(self.GetSize())
        self.Show()


class Panel(wx.Panel):
    def __init__(self, *args, **kw):
        super().__init__(*args, **kw)
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        vbox1 = wx.BoxSizer(wx.VERTICAL)
        vbox2 = wx.BoxSizer(wx.VERTICAL)

        hbox1 = wx.BoxSizer(wx.HORIZONTAL)
        fileFolderChoices = ["Folder", "File"]
        self.fileFolder = wx.RadioBox(
            self, label="Folder or File", choices=fileFolderChoices)
        self.fileFolder.Bind(wx.EVT_RADIOBOX, self.onRadioBox)
        hbox1.Add(self.fileFolder)
        fileContainerChoices = [".ogg", ".opus"]
        self.fileContainer = wx.RadioBox(
            self, label="File extension", choices=fileContainerChoices)
        hbox1.Add(self.fileContainer, flag=wx.LEFT, border=10)
        vbox1.Add(hbox1, flag=wx.LEFT | wx.RIGHT |
                  wx.TOP | wx.BOTTOM, border=10)

        self.hbox2 = wx.BoxSizer(wx.HORIZONTAL)
        selectText = wx.StaticText(self, label='Select File/Directory')
        self.hbox2.Add(selectText)
        self.select = wx.DirPickerCtrl(self)
        self.hbox2.Add(self.select, flag=wx.LEFT |
                       wx.EXPAND, border=10, proportion=1)
        vbox1.Add(self.hbox2, flag=wx.EXPAND | wx.LEFT |
                  wx.RIGHT | wx.TOP | wx.BOTTOM, border=10)

        hbox3 = wx.BoxSizer(wx.HORIZONTAL)
        rateText = wx.StaticText(self, label='Select Prefered Bitrate')
        hbox3.Add(rateText)
        self.rate = wx.ComboBox(
            self, choices=['24', '32', '64', '96', '128', '192', '256', '320'])
        self.rate.SetValue(text='128')
        hbox3.Add(self.rate, flag=wx.LEFT | wx.EXPAND, border=10, proportion=1)
        vbox1.Add(hbox3, flag=wx.LEFT | wx.RIGHT |
                  wx.EXPAND | wx.BOTTOM, border=10)

        hbox4 = wx.BoxSizer(wx.HORIZONTAL)
        self.keepFiles = wx.CheckBox(self, label="Keep Original Files")
        self.keepFiles.SetValue(True)
        hbox4.Add(self.keepFiles)
        vbox1.Add(hbox4, flag=wx.LEFT | wx.RIGHT |
                  wx.EXPAND | wx.BOTTOM, border=10)

        hbox6 = wx.BoxSizer(wx.HORIZONTAL)
        Button = wx.Button(self, size=(70, 30), label='CONVERT')
        Button.Bind(wx.EVT_BUTTON, self.threading)
        hbox6.Add(Button)
        vbox1.Add(hbox6, flag=wx.LEFT | wx.RIGHT |
                  wx.EXPAND | wx.BOTTOM, border=10)

        hbox5 = wx.BoxSizer(wx.HORIZONTAL)
        log = wx.TextCtrl(self, -1, style=wx.TE_MULTILINE |
                          wx.TE_READONLY | wx.HSCROLL)
        redir = RedirectText(log)
        sys.stdout = redir
        hbox5.Add(log, proportion=1, flag=wx.EXPAND)
        vbox2.Add(hbox5, flag=wx.LEFT | wx.RIGHT |
                  wx.EXPAND, border=10, proportion=1)

        hbox.Add(vbox1, proportion=1, flag=wx.EXPAND)
        hbox.Add(vbox2, proportion=1, flag=wx.EXPAND |
                 wx.LEFT | wx.TOP | wx.BOTTOM, border=10)

        self.SetSizer(hbox)

    def onRadioBox(self, event):
        self.select.Destroy()
        if self.fileFolder.GetSelection() == 0:
            self.select = wx.DirPickerCtrl(self)
            self.hbox2.Add(self.select, flag=wx.LEFT |
                           wx.EXPAND, border=10, proportion=1)
            self.Layout()
        else:
            self.select = wx.FilePickerCtrl(self)
            self.hbox2.Add(self.select, flag=wx.LEFT |
                           wx.EXPAND, border=10, proportion=1)
            self.Layout()

    def onButton(self, event):
        path = self.select.GetPath()
        if self.fileFolder.GetSelection() == 1:
            tempPath = self.select.GetPath()
            file = tempPath.split('\\')[-1]
            path = path.rsplit('\\', 1)[0]

        bitrate = self.rate.GetValue()

        if self.fileContainer.GetSelection() == 0:
            container = "ogg"
        else:
            container = "opus"

        os.chdir(path)

        if self.keepFiles.GetValue() == 0:  # if not to keep files
            original = 'NONE'
        else:  # if keep files
            original = os.path.join(path, 'original')

        if self.fileFolder.GetSelection() == 0:  # if folder
            converter.convert(path, bitrate, original, container)
        else:  # if file
            converter.convertfile(file, bitrate, original, container)

        print("\nDone converting")

    def threading(self, event):
        import threading
        th = threading.Thread(target=self.onButton, args=(event,))
        th.start()


def main():
    app = wx.App()
    windowClass(None, title='convert_to_opus', size=(800, 300))
    app.MainLoop()


if __name__ == '__main__':
    main()
