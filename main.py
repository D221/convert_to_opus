import wx
import converter
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

        # Displays console log
        self.log = wx.TextCtrl(self, -1, pos=(250, 10), size=(300, 200),
                               style=wx.TE_MULTILINE | wx.TE_READONLY | wx.HSCROLL)
        redir = RedirectText(self.log)
        sys.stdout = redir

        wx.StaticText(self, pos=(10, 10), label='Select Directory')
        self.select = wx.DirPickerCtrl(self, pos=(10, 30), size=(230, 23))
        wx.StaticText(self, pos=(10, 60), label='Select Prefered Bitrate')
        self.rate = wx.ComboBox(self, pos=(10, 80), size=(150, 23), choices=[
                                '24', '32', '64', '96', '128', '192', '256', '320'])
        self.rate.SetValue(text='128')
        Button = wx.Button(self, pos=(10, 130),
                           size=(150, 50), label='CONVERT')
        Button.Bind(wx.EVT_BUTTON, self.threading)

    def threading(self, event):
        import threading
        th = threading.Thread(target=self.onButton, args=(event,))
        th.start()

    def onButton(self, event):
        path = self.select.GetPath()
        bitrate = self.rate.GetValue()

        os.chdir(path)
        if not os.path.exists('original'):
            os.makedirs('original')
        original = os.path.join(path, 'original')

        converter.convert(path, bitrate, original)
        print("\nDone converting")


def main():
    app = wx.App()
    windowClass(None, title='convert_to_opus', size=(600, 300),
                style=wx.MINIMIZE_BOX | wx.CAPTION | wx.CLOSE_BOX)
    app.MainLoop()


if __name__ == '__main__':
    main()
