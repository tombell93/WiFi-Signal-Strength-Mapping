#!/usr/bin/python

# bitmap.py

import wx

class MyFrame(wx.Frame):
    def __init__(self, parent, id, title):
        wx.Frame.__init__(self, parent, id, title, size = (788, 616))

        self.bitmap = wx.Bitmap('test.png')
        wx.EVT_PAINT(self, self.OnPaint)

        self.Centre()

    def OnPaint(self, event):
        dc = wx.PaintDC(self)
        dc.DrawBitmap(self.bitmap, 10, 10)


class MyApp(wx.App):
    def OnInit(self):
        frame = MyFrame(None, -1, 'Wi-Fi Signal Strength Plotting')
        frame.Show(True)
        self.SetTopWindow(frame)
        return True

app = MyApp(0)
app.MainLoop()