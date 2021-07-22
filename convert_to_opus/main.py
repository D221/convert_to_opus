import wx
from convert_to_opus import converter
import os
import sys


class windowClass(wx.Frame):
    def __init__(self, *args, **kw):
        super(windowClass, self).__init__(*args, **kw)
        self.Panel = Panel(self)
        self.Show()


class RedirectText(object):  # Redirects console output to wx panel
    def __init__(self, aWxTextCtrl):
        self.out = aWxTextCtrl

    def write(self, string):
        self.out.WriteText(string)


class Panel(wx.Panel):
    def __init__(self, *args, **kw):
        super().__init__(*args, **kw)

        # Console log
        self.log = wx.TextCtrl(self, -1, pos=(250, 10), size=(300, 200),
                               style=wx.TE_MULTILINE | wx.TE_READONLY | wx.HSCROLL)
        redir = RedirectText(self.log)
        sys.stdout = redir

        # File or Directory selection box
        fileFolderChoices = ["Folder", "File"]
        self.fileFolder = wx.RadioBox(
            self, label="Folder or File", choices=fileFolderChoices, pos=(10, 10))
        self.fileFolder.Bind(wx.EVT_RADIOBOX, self.onRadioBox)

        # Audio container selection box
        fileContainerChoices = [".ogg", ".opus"]
        self.fileContainer = wx.RadioBox(
            self, label="File extension", choices=fileContainerChoices, pos=(130, 10))
        self.fileContainer.Bind(wx.EVT_RADIOBOX, self.onRadioBox)

        # Directory selection
        wx.StaticText(self, pos=(10, 70), label='Select File/Directory')
        self.select = wx.DirPickerCtrl(self, pos=(10, 90), size=(230, 23))

        # Bitrate selection
        wx.StaticText(self, pos=(10, 120), label='Select Prefered Bitrate')
        self.rate = wx.ComboBox(self, pos=(10, 140), size=(150, 23), choices=[
                                '24', '32', '64', '96', '128', '192', '256', '320'])
        self.rate.SetValue(text='128')

        # Keep original files checkbox
        self.keepFiles = wx.CheckBox(self, pos=(
            10, 170), label="Keep Original Files")
        self.keepFiles.SetValue(True)

        # Convert button
        Button = wx.Button(self, pos=(10, 200),
                           size=(150, 50), label='CONVERT')
        Button.Bind(wx.EVT_BUTTON, self.threading)

    def onRadioBox(self, event):
        self.select.Destroy()
        if self.fileFolder.GetSelection() == 0:
            self.select = wx.DirPickerCtrl(self, pos=(10, 90), size=(230, 23))
        else:
            self.select = wx.FilePickerCtrl(self, pos=(10, 90), size=(230, 23))

    def threading(self, event):
        import threading
        th = threading.Thread(target=self.onButton, args=(event,))
        th.start()

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


def main():
    app = wx.App()
    windowClass(None, title='convert_to_opus', size=(600, 300),
                style=wx.MINIMIZE_BOX | wx.CAPTION | wx.CLOSE_BOX)
    app.MainLoop()


if __name__ == '__main__':
    main()
