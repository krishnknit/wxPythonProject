import wx

class MyPanels(wx.Panel):

    def __init__(self, parent, id):
        wx.Panel.__init__(self, parent, style=wx.RAISED_BORDER)
        #wx.SIMPLE_BORDER wx.RAISED_BORDER wx.SUNKEN_BORDER wx.NO_BORDER
        self.parent = parent
