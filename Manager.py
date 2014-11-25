#!/usr/bin/python

import wx
import Scanner
import pickle
import json

class MyFrame(wx.Frame):
    def __init__(self, parent, id, title):
        wx.Frame.__init__(self, parent, id, title, size = (1598, 723))

        # TODO: Define 1598 x 723 2D matrix for each WAP on each nework
        self.listOfWAPS = list()

        self.floor1_image = wx.Bitmap('b59_1.png')
        self.floor4_image = wx.Bitmap('b59_4.png')

        wx.EVT_PAINT(self, self.OnPaint)
        self.Bind(wx.EVT_LEFT_UP, self.OnClick)

        self.Centre()

    def OnPaint(self, event):
        self.dc = wx.PaintDC(self)
        self.dc.DrawBitmap(self.floor1_image, 0, 0)
        self.load('name' )
        self.RedrawAllPoints()

    def RedrawAllPoints(self):
        #self.dc.Clear()
        #self.dc.DrawBitmap(self.floor1_image, 0, 0)
        for point in self.listOfWAPS:

            self.dc.BeginDrawing()
            yellowIntensity = (-int(point['power'])*1.5 + (-int(point['power'])))
            colour = wx.Colour(255,yellowIntensity,0)
            self.dc.SetPen(wx.Pen(colour,style=wx.TRANSPARENT))
            self.dc.SetBrush(wx.Brush(colour, wx.SOLID))
            # set x, y, w, h for rectangle
            self.dc.DrawCircle(point['point'][0], point['point'][1], 10)
            self.dc.DrawText(str(point['power']), point['point'][0], point['point'][1])

            self.dc.EndDrawing()

    def OnClick(self, event):
        point = event.GetLogicalPosition(self.dc)
        pointTuple = point.Get()
        print 'Click at point ' + str(pointTuple)
        parsedListOfWAPDicts = Scanner.scan()
        #print parsedListOfWAPDicts

        # TODO: Get signal strength at this location and put in matrix
        if (parsedListOfWAPDicts is not None) and (len(parsedListOfWAPDicts) != 0):
            print 'NOTE: Wi-Fi data is available.'

            # ESSID's of networks being used
            ESSIDList = ['eduroam', 'ISS', 'ECS-WLAN', 'The House of Fun']

            for WAPItem in parsedListOfWAPDicts:
                # TODO: If WAPItem is being used, check if it's the strongest signal
                essid = WAPItem['ESSID']
                bssid = WAPItem['BSSID']
                power = int(WAPItem['Power'])

                if essid in ESSIDList:
                    print 'WAP is in ESSIDList'
                    
                    pointDict = {'ESSID': essid, 'BSSID': bssid, 'power': power, 'point': pointTuple}
                    self.listOfWAPS.append(pointDict)
                    #print 'STORED--> Point: ' + str(pointTuple) + ' ESSID: ' + essid + ', BSSID: ' + bssid + ', Power: ' + str(power);
                    print 'STORED--> ' + str(pointTuple) + ' ' + essid + ' ' + bssid + ' ' + str(power);
                else:   
                    pass         
                    #print 'IGNORED-> Point: ' + str(pointTuple) + 'ESSID: ' + essid + ', BSSID: ' + bssid + ', Power: ' + str(power);

        else:
            print 'WARNING: Wi-Fi data not available.'

        # Redraw all points
        self.RedrawAllPoints()
        self.save(self.listOfWAPS, 'list')


        # Print dict
        for x in self.listOfWAPS:
            print (x)

    def save(self, obj, name ):
        with open('data.pickle', 'wb') as handle:
            pickle.dump(obj, handle)


    def load(self, name ):
        with open('data.pickle', 'rb') as handle:
            b = pickle.load(handle)
            self.listOfWAPS = b
            print self.listOfWAPS

class MyApp(wx.App):
    def OnInit(self):
        frame = MyFrame(None, -1, 'Wi-Fi Signal Strength Plotting')
        frame.Show(True)
        self.SetTopWindow(frame)
        return True

app = MyApp(0)
app.MainLoop()