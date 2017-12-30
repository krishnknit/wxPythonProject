import wx
import sys
import traceback
import pymssql
import logging
import subprocess
import pandas as pd
import numpy as np
import databaseconfig as cfg
from myPanels import MyPanels
from scenariosSelection import ScenariosSelection
from autoWidthListCtrl import AutoWidthListCtrl
from sqlalchemy import create_engine

# setting to create log file
logging.basicConfig(filename='panelControls.log', format='%(asctime)s %(message)s', level=logging.DEBUG)

def show_error():
    message = ''.join(traceback.format_exception(*sys.exc_info()))
    dialog = wx.MessageDialog(None, message, 'Error!', wx.OK|wx.ICON_ERROR)
    dialog.ShowModal()

class MyFrame(wx.Frame):
    def __init__(self, parent, id, title):
        wx.Frame.__init__(self, parent, id, title, size=(1000, 700))
        self.parent = parent

        self.panel = wx.Panel(self, -1)
        self.panel.SetBackgroundColour("grey")

        self.leftpanel = MyPanels(self.panel, 1)
        self.rightpanel = MyPanels(self.panel, 2)
        self.bottompanel = MyPanels(self.panel, 3)
        self.scenariopanel = MyPanels(self.panel, 4)
        #self.leftpanel.SetBackgroundColour("red")
        #self.rightpanel.SetBackgroundColour("green")
        #self.bottompanel.SetBackgroundColour("yellow")

        self.basicsizer = wx.BoxSizer(wx.HORIZONTAL)
        self.vsizer = wx.BoxSizer(wx.VERTICAL)

        self.basicsizer.Add(self.leftpanel, proportion=1, flag=wx.EXPAND)
        self.basicsizer.Add(self.rightpanel, proportion=2, flag=wx.EXPAND)
        self.basicsizer.Add(self.scenariopanel, proportion=2, flag=wx.EXPAND)
        self.vsizer.Add(self.basicsizer, 1, wx.EXPAND)
        self.vsizer.Add(self.bottompanel, 1, wx.EXPAND)
        self.panel.SetSizer(self.vsizer)
        self.panel.Fit()

        self.prodBtn =  wx.Button(self.leftpanel, 1, 'Prod', (50, 50))
        self.devBtn = wx.Button(self.leftpanel, 2, 'Dev', (50, 100))
        self.qaBtn = wx.Button(self.leftpanel, 3, 'QA', (50, 150))

        self.prodBtn.Bind(wx.EVT_BUTTON, self.onProdClick)
        self.devBtn.Bind(wx.EVT_BUTTON, self.onDevClick)
        self.qaBtn.Bind(wx.EVT_BUTTON, self.onQAClick)

    def createRightPanel(self):
        self.rightpanel = MyPanels(self.panel, 2)
        #self.rightpanel.SetBackgroundColour("blue")
        #self.basicsizer.Add(self.leftpanel, 1, wx.EXPAND)
        #self.basicsizer.Add(self.rightpanel, 1, wx.EXPAND)
        #self.vsizer.Add(self.basicsizer, 1, wx.EXPAND)
        #self.vsizer.Add(self.bottompanel, 1, wx.EXPAND)
        #self.panel.Layout()

        #self.Show(True)
        #self.Centre()

    def createScenarioPanel(self):
        self.scenariopanel = MyPanels(self.panel, 4)

    def createBottomPanel(self):
        self.bottompanel = MyPanels(self.panel, 3)

    def destroyRightPanel(self):
        self.rightpanel.Hide()
        self.panel.Layout()

    def destroyScenarioPanel(self):
        self.scenariopanel.Hide()
        self.panel.Layout()

    def destroyBottonPanel(self):
        self.bottompanel.Hide()
        self.panel.Layout()

    def onProdClick(self, event):
        self.destroyRightPanel()
        self.createRightPanel()
        #self.rightpanel.SetBackgroundColour("yellow")
        self.basicsizer.Add(self.rightpanel, proportion=2, flag=wx.EXPAND)

        self.btn4 = wx.Button(self.rightpanel, 4, 'Run', (20, 120))
        self.rpText = wx.StaticText(self.rightpanel, 1, "Welcome to Production panel!", (10, 20))
        self.rStartLabel = wx.StaticText(self.rightpanel, 2, "Start Date:", (10, 50))
        self.rEndLabel = wx.StaticText(self.rightpanel, 3, "End Date:", (10, 80))
        self.rStartDate = wx.TextCtrl(self.rightpanel, 2, wx.EmptyString, pos=(100, 50), size=(120, -1))
        self.rEndDate = wx.TextCtrl(self.rightpanel, 3, wx.EmptyString, pos=(100, 80), size=(120, -1))

        self.pvSizer = wx.BoxSizer(wx.VERTICAL)
        self.hs1 = wx.BoxSizer(wx.HORIZONTAL)
        self.hs2 = wx.BoxSizer(wx.HORIZONTAL)

        self.hs1.Add(self.rStartLabel, 2, wx.ALIGN_LEFT)
        self.hs1.Add(self.rStartDate, 2, wx.ALIGN_RIGHT)
        self.hs2.Add(self.rEndLabel, 3, wx.ALIGN_LEFT)
        self.hs2.Add(self.rEndDate, 3, wx.ALIGN_RIGHT)

        self.pvSizer.Add(self.rpText, 1, wx.ALIGN_LEFT)
        self.pvSizer.Add(self.hs1, 2, wx.ALIGN_LEFT)
        self.pvSizer.Add(self.hs2, 3, wx.ALIGN_LEFT)
        self.pvSizer.Add(self.btn4, proportion = 0, flag = wx.ALIGN_LEFT)

        self.SetSizer(self.pvSizer)
        self.panel.Layout()

        self.btn4.Bind(wx.EVT_BUTTON, self.onClickProdRun)

    def onClickProdRun(self, event):
        pass

    def onDevClick(self, event):
        self.destroyRightPanel()
        self.createRightPanel()
        #self.rightpanel.SetBackgroundColour("green")
        self.basicsizer.Add(self.rightpanel, proportion=2, flag=wx.EXPAND)

        self.btn4 = wx.Button(self.rightpanel, 4, 'Run', (20, 120))
        self.rpText = wx.StaticText(self.rightpanel, 1, "Welcome to Development panel!", (10, 20))
        self.rStartLabel = wx.StaticText(self.rightpanel, 2, "Start Date:", (10, 50))
        self.rEndLabel = wx.StaticText(self.rightpanel, 3, "End Date:", (10, 80))
        self.rStartDate = wx.TextCtrl(self.rightpanel, 2, wx.EmptyString, pos=(100, 50), size=(120, -1))
        self.rEndDate = wx.TextCtrl(self.rightpanel, 3, wx.EmptyString, pos=(100, 80), size=(120, -1))

        self.pvSizer = wx.BoxSizer(wx.VERTICAL)
        self.hs1 = wx.BoxSizer(wx.HORIZONTAL)
        self.hs2 = wx.BoxSizer(wx.HORIZONTAL)

        self.hs1.Add(self.rStartLabel, 2, wx.ALIGN_LEFT)
        self.hs1.Add(self.rStartDate, 2, wx.ALIGN_RIGHT)
        self.hs2.Add(self.rEndLabel, 3, wx.ALIGN_LEFT)
        self.hs2.Add(self.rEndDate, 3, wx.ALIGN_RIGHT)

        self.pvSizer.Add(self.rpText, 1, wx.ALIGN_LEFT)
        self.pvSizer.Add(self.hs1, 2, wx.ALIGN_LEFT)
        self.pvSizer.Add(self.hs2, 3, wx.ALIGN_LEFT)
        self.pvSizer.Add(self.btn4, proportion = 0, flag = wx.ALIGN_LEFT)

        self.SetSizer(self.pvSizer)
        self.panel.Layout()

        self.btn4.Bind(wx.EVT_BUTTON, self.onClickDevRun)

    def onClickDevRun(self, event):
        pass

    def onQAClick(self, event):
        self.destroyRightPanel()
        self.destroyScenarioPanel()
        self.createRightPanel()
        self.createScenarioPanel()
        #self.rightpanel.SetBackgroundColour("blue")
        self.basicsizer.Add(self.rightpanel, proportion=2, flag=wx.EXPAND)
        self.basicsizer.Add(self.scenariopanel, proportion=2, flag=wx.EXPAND)

        self.btn4 = wx.Button(self.rightpanel, 4, 'RunProc', pos=(20, 150))
        self.btn5 = wx.Button(self.rightpanel, 5, 'RunRscript', pos=(120, 150))
        self.btn6 = wx.Button(self.rightpanel, 6, 'RunAnalysis', pos=(220, 150))
        self.rpText = wx.StaticText(self.rightpanel, 1, "Welcome to QA panel!", (100, 20))
        self.rStartLabel = wx.StaticText(self.rightpanel, 2, "Start Date:", (10, 50))
        self.rEndLabel = wx.StaticText(self.rightpanel, 3, "End Date:", (10, 80))
        self.rStartDate = wx.TextCtrl(self.rightpanel, 2, wx.EmptyString, pos=(100, 50), size=(120, -1))
        self.rEndDate = wx.TextCtrl(self.rightpanel, 3, wx.EmptyString, pos=(100, 80), size=(120, -1))

        self.pvSizer = wx.BoxSizer(wx.VERTICAL)
        self.hs1 = wx.BoxSizer(wx.HORIZONTAL)
        self.hs2 = wx.BoxSizer(wx.HORIZONTAL)
        self.hs3 = wx.BoxSizer(wx.HORIZONTAL)

        self.hs1.Add(self.rStartLabel, 2, wx.ALIGN_LEFT)
        self.hs1.Add(self.rStartDate, 2, wx.ALIGN_RIGHT)
        self.hs2.Add(self.rEndLabel, 3, wx.ALIGN_LEFT)
        self.hs2.Add(self.rEndDate, 3, wx.ALIGN_RIGHT)
        self.hs3.Add(self.btn4, proportion = 0, flag = wx.ALIGN_LEFT)
        self.hs3.Add(self.btn5, proportion = 1, flag = wx.ALIGN_LEFT)
        self.hs3.Add(self.btn6, proportion = 2, flag = wx.ALIGN_LEFT)

        self.pvSizer.Add(self.rpText, 1, wx.ALIGN_LEFT)
        self.pvSizer.Add(self.hs1, 2, wx.ALIGN_LEFT)
        self.pvSizer.Add(self.hs2, 3, wx.ALIGN_LEFT)
        self.pvSizer.Add(self.hs3, 4, wx.ALIGN_LEFT)

        self.SetSizer(self.pvSizer)
        self.panel.Layout()

        self.btn4.Bind(wx.EVT_BUTTON, self.onClickQARunProc)
        self.btn5.Bind(wx.EVT_BUTTON, self.onClickQARunRscript)
        self.btn6.Bind(wx.EVT_BUTTON, self.onClickQARunAnalysis)

    def onClickQARunRscript(self, event):
        self.rpText = wx.StaticText(self.scenariopanel, 1, "Scenarios", (150, 20))
        self.radioBtn7 = wx.RadioButton(self.scenariopanel, wx.ID_ANY, "scenario1", (50, 40))

        self.vSizer = wx.BoxSizer(wx.VERTICAL)
        self.vSizer.Add(self.rpText, 0, wx.ALL, 5)
        self.vSizer.Add(self.radioBtn7, 0, wx.ALL, 5)
        self.SetSizer(self.vSizer)
        self.panel.Layout()

        self.Bind(wx.EVT_RADIOBUTTON, self.OnRadiogroup)

    def OnRadiogroup(self, event):
        rb = event.GetEventObject()
        # print rb.GetLabel()
        l = ["AND", "OR", "XOR", "NOT"]
        #app = wx.PySimpleApp()
        dlg = ScenariosSelection(None, 'Please select both PC and Index file', 'Scenarios selection', choices = l)

        if dlg.ShowModal() == wx.ID_OK:
            result = dlg.GetSelections()
            wx.MessageBox(str(result) + ' were chosen')

        #dlg.Destroy()


    def onClickQARunAnalysis(self, event):
        preMonPCDF = pd.read_excel("/home/krishna/dev_coding/python/wxPython/exFile/r_SGD_PC_set1.xlsx", sheetname = "Sheet1")
        newMonPCDF = pd.read_excel("/home/krishna/dev_coding/python/wxPython/exFile/r_SGD_PC_set2.xlsx", sheetname = "Sheet1")
        preMonIdxDF = pd.read_excel("/home/krishna/dev_coding/python/wxPython/exFile/r_SGD_indx_set1.xlsx", sheetname = "Sheet1")
        newMonIdxDF = pd.read_excel("/home/krishna/dev_coding/python/wxPython/exFile/r_SGD_indx_set2.xlsx", sheetname = "Sheet1")

        preMonPCDF.reset_index(inplace = True)
        newMonPCDF.reset_index(inplace = True)
        preMonIdxDF.reset_index(inplace = True)
        newMonIdxDF.reset_index(inplace = True)
        preMonPCDF.rename(columns = {"index": "Date"}, inplace = True)
        newMonPCDF.rename(columns = {"index": "Date"}, inplace = True)
        preMonIdxDF.rename(columns = {"index": "Date"}, inplace = True)
        newMonIdxDF.rename(columns = {"index": "Date"}, inplace = True)

        missDF = preMonPCDF[~preMonPCDF.Date.isin(newMonPCDF.Date.values)]
        newDF = newMonPCDF[~newMonPCDF.Date.isin(preMonPCDF.Date.values)]

        self.destroyBottonPanel()
        self.createBottomPanel()
        self.vsizer.Add(self.bottompanel, 1, wx.EXPAND)
        # wx.MessageBox('Result found...', 'OK', wx.OK | wx.ICON_WARNING)

        self.list = AutoWidthListCtrl(self.bottompanel)
        self.list.InsertColumn(0, "Selection", wx.LIST_FORMAT_CENTER)
        self.list.InsertColumn(1, "GSD", wx.LIST_FORMAT_CENTER)
        self.list.InsertColumn(2, "y1", wx.LIST_FORMAT_CENTER)
        self.list.InsertColumn(3, "y2", wx.LIST_FORMAT_CENTER)
        self.list.InsertColumn(4, "y3", wx.LIST_FORMAT_CENTER)
        self.list.InsertColumn(5, "y5", wx.LIST_FORMAT_CENTER)
        self.list.InsertColumn(6, "y7", wx.LIST_FORMAT_CENTER)
        self.list.InsertColumn(7, "y10", wx.LIST_FORMAT_CENTER)
        self.list.InsertColumn(8, "y20", wx.LIST_FORMAT_CENTER)
        self.list.InsertColumn(9, "y30", wx.LIST_FORMAT_CENTER)
        self.list.InsertColumn(10, "Drives", wx.LIST_FORMAT_CENTER)

        if not newDF.empty:
            self.createAnalysisDataFrame(newDF, newMonIdxDF, 'new')
        if not missDF.empty:
            self.createAnalysisDataFrame(missDF, preMonIdxDF, 'miss')

        if newDF.empty and missDF.empty:
            wx.MessageBox('No new or missing date found...', 'Warning', wx.OK | wx.ICON_WARNING)
            self.panel.Layout()
            return

        self.hbox = wx.BoxSizer(wx.HORIZONTAL)
        self.hbox.Add(self.list, 1, wx.EXPAND)
        self.SetSizer(self.hbox)
        self.panel.Layout()

    def createAnalysisDataFrame(self, newmissdf, idxDF, sln):
        for index, row in newmissdf.iterrows():
            date = row['Date']
            y1 = row['y1']
            y2 = row['y2']
            y3 = row['y3']
            y5 = row['y5']
            y7 = row['y7']
            y10 = row['y10']
            y20 = row['y20']
            y30 = row['y30']
            driver = row['driver']
            idxDF.sort_values(by=[str(driver)], ascending = True, inplace = True)
            dfLength = len(idxDF.index)

            # get rank
            rtext = self.getRank(idxDF, driver, date, dfLength)

            indx = self.list.InsertStringItem(sys.maxint, str(sln))
            self.list.SetStringItem(indx, 1, str(date))
            self.list.SetStringItem(indx, 2, str(y1))
            self.list.SetStringItem(indx, 3, str(y2))
            self.list.SetStringItem(indx, 4, str(y3))
            self.list.SetStringItem(indx, 5, str(y5))
            self.list.SetStringItem(indx, 6, str(y7))
            self.list.SetStringItem(indx, 7, str(y10))
            self.list.SetStringItem(indx, 8, str(y20))
            self.list.SetStringItem(indx, 9, str(y30))
            self.list.SetStringItem(indx, 10, str(rtext))

    def getRank(self, df, driver, date, dfLength):
        rank = ''
        for idx, r in df.iterrows():
            rr = r['Date']
            if str(date) == str(rr):
                if idx > dfLength / 2:
                    rank = dfLength - idx
                    rank = '-' + str(rank)
                else:
                    rank = idx

        rtext = driver + " Relative ranking (" + rank + ")"
        return rtext

    def onClickQARunProc(self, event):
        startDate = self.rStartDate.GetValue()
        endDate = self.rEndDate.GetValue()

        if not startDate or not endDate:
            wx.MessageBox('Operation could not be completed, please enter required date...', 'Warning', wx.OK | wx.ICON_WARNING)
            return

        dlg = wx.MessageDialog(None, "Stress run is running from " + startDate + " to " + endDate + ". Do you want to continue?", 'RUN Dialog', wx.YES_NO | wx.ICON_QUESTION)
        result = dlg.ShowModal()

        if result == wx.ID_YES:
            self.rStartDate.SetValue('')
            self.rEndDate.SetValue('')
            
            self.destroyBottonPanel()
            self.createBottomPanel()
            #self.rightpanel.SetBackgroundColour("blue")
            self.vsizer.Add(self.bottompanel, 1, wx.EXPAND)

            df = getDataFromTable(startDate, endDate)

            if df.empty:
                wx.MessageBox('No result found, please choose correct date range...', 'Warning', wx.OK | wx.ICON_WARNING)
                self.panel.Layout()
                return

            self.list = AutoWidthListCtrl(self.bottompanel)
            self.list.InsertColumn(0, 'Date', wx.LIST_FORMAT_CENTER)
            self.list.InsertColumn(1, 'Term', wx.LIST_FORMAT_CENTER)
            self.list.InsertColumn(2, 'Yield', wx.LIST_FORMAT_CENTER)

            for idx, row in df.iterrows():
                date = row['dt']
                term = row['term']
                yld = row['yield']

                index = self.list.InsertStringItem(sys.maxint, str(date))
                self.list.SetStringItem(index, 1, str(term))
                self.list.SetStringItem(index, 2, str(yld))

            self.hbox = wx.BoxSizer(wx.HORIZONTAL)

            self.hbox.Add(self.list, 1, wx.EXPAND)
            self.SetSizer(self.hbox)
            self.panel.Layout()

            #self.Centre()
            #print "Welcome Back: "
        else:
            logging.warning('This is a warning')

def getDataFromTable(startDate, endDate):
    ## instance a python db connection object (same as python-mysql drivers)
    conn = pymssql.connect(
                server   = cfg.mssql['host'],
                database = cfg.mssql['db'], 
                user     = cfg.mssql['user'],
                password = cfg.mssql['passwd'], 
                port     = cfg.mssql['port']
                      )   

    # sql query
    stmt = "SELECT * FROM yld_crv_hist_v WHERE dt > '" + startDate + "' and dt < '" + endDate + "'"

    # Excute Query here
    df = pd.read_sql(stmt, conn)
    if df is not None:
        #print df.head(5)
        return df

def callRScript():
    subprocess.check_call(['Rscript', 'myrscript.R'], shell = False)


def main():
    # Set up all the stuff for a wxPython application
    app = wx.App()
    try:
        # Add a top level frame
        frame = MyFrame(None, -1, 'My Application')
        # Display the frame and panel within it
        frame.Show()
        # Wait for events and process each one you receive
        app.MainLoop()
    except:
        show_error()

if __name__ == '__main__':
    main()
