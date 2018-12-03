import wx
import _thread as thrend
import datetime as dt
import pandas as pd
import matplotlib.pyplot as plt
import my_envirounment
ID_EVENT_REFRESH = 9999
#_cityname = '南京'
class MyfirstFram(wx.Frame,):
    def __init__(self, superior):
        self._cityname = '南京'
        self._time = '20150209'
        self._data = {}
        self._forecas_date = []
        # self._forecas_deg = []
        self._forecas_spd = []
        self._forecas_hum = []
        self._forecas_uv = []
        self._forecas_min = []
        self._forecas_max = []
        self._forecas_pop = []
        self._forecas_vis = []
        self._Dhistory_updatetime = []
        self._Dhistory_windspeed = []
        self._Dhistory_humidity = []
        self._Dhistory_rain = []
        self._Dhistory_feelst = []
        self._Dhistory_temperature = []
        # self._Mhistory_year = ''
        self._Mhistory_month = []
        self._Mhistory_tem_max = []
        self._Mhistory_pre = []
        self._Mhistory_tem_min = []
        self._Mhistory_tem_avg = []
        list_f = list(my_envirounment.palceName())
        dict1 = list_f[0]
        dict2 = list_f[1]
        #print(dict1)
        wx.Frame.__init__(self, parent=superior, title="天气预报&往年数据分析", pos=
        (200, 100), size=(1000, 600))
        self.CreateStatusBar()
        menuBar = wx.MenuBar()
        #menuBar1 = wx.MenuBar()
        filemenu = wx.Menu()
        #filemenu1 = wx.Menu()
        menuBar.Append(filemenu, "&菜单")
        #menuBar1.Append(filemenu1,"&帮助")
        menuforecas = filemenu.Append(0, "&天气预报", "未来七天的天气")
        self.Bind(wx.EVT_MENU, self.forecas, menuforecas)
        menuDhistory = filemenu.Append(1, "&24小时天气", "过去24小时历史天气")
        self.Bind(wx.EVT_MENU, self.Dhistory, menuDhistory)
        menuMhistory = filemenu.Append(2, "&月度天气", "指定年份月度天气")
        self.Bind(wx.EVT_MENU, self.Mhistory, menuMhistory)
        menuYhistory = filemenu.Append(3, "&日天气", "历史某一天天气")
        self.Bind(wx.EVT_MENU, self.Yhistory, menuYhistory)
        ReFesher =  filemenu.Append(4,"&刷新",'刷新当前项目')
        self.Bind(wx.EVT_MENU, self.RFesher, ReFesher)
        Analyzer =  filemenu.Append(5,"&分析",'分析列表中的数据')
        self.Bind(wx.EVT_MENU, self.Analyzers, Analyzer)
        QUit = filemenu.Append(wx.ID_EXIT, "&退出", "")
        self.Bind(wx.EVT_MENU, self.OnQuit, QUit)
        myhelps = filemenu.Append(6, "&帮助", "获得帮助")
        self.Bind(wx.EVT_MENU, self.helps, myhelps)
        self.SetMenuBar(menuBar)
        #self.SetMenuBar(menuBar1)
        panel = wx.Panel(self)
        #codeSizer0 = wx.BoxSizer(wx.HORIZONTAL)
        codeSizer = wx.BoxSizer(wx.HORIZONTAL)
        #codeSizer.AddGrowableRow(2)
        #codeSizer.AddGrowableCol(4)
        #codeSizer.AddGrowableCol(3)
        proviceLable = wx.StaticText(panel, -1, "省份:")
        #codeSizer.Add(proviceLable,-0,wx.ALIGN_BOTTOM)
        proviceComboBox = wx.ComboBox(panel, -1, value=list(dict1.keys())[0], choices=list(dict1.keys()),
                                      style=wx.CB_READONLY)
        cityLable = wx.StaticText(panel, -1, "市区:")
        shiquComboBox = wx.ComboBox(panel, -1, value=dict1[list(dict1.keys())[0]][0],
                                   choices=dict1[list(dict1.keys())[0]], style=wx.CB_READONLY)
        value1 = dict1[list(dict1.keys())[0]][0]
        #list_v = dict2[value1]
        xianquLable = wx.StaticText(panel, -1, "县区:")
        xianquComboBox = wx.ComboBox(panel, -1, value=dict2[value1][0],
                                   choices=dict2[value1], style=wx.CB_READONLY)
        #ch1 = wx.ComboBox(panel, -1, value='南京', choices=list[1], style=wx.CB_SORT)
        #ch1 = wx.ComboBox(panel, -1, value='南京', choices=list[2], style=wx.CB_SORT)
        #text1 = wx.TextCtrl(panel, value="Hello, World!", size=(350, 200))
        codeSizer.AddMany([
            (proviceLable, 0,  wx.ALIGN_RIGHT), (proviceComboBox, 0, wx.SHAPED)
            #(wx.Size(6, 6), 0, wx.SHAPED | wx.ALIGN_RIGHT), (wx.Size(6, 6), 1, wx.EXPAND)
            , (cityLable, 0, wx.ALIGN_RIGHT), (shiquComboBox, 0, wx.SHAPED)
            #(wx.Size(6, 6), 0, wx.SHAPED | wx.ALIGN_RIGHT), (wx.Size(6, 6), 1, wx.EXPAND)
            ,(xianquLable, 0, wx.ALIGN_RIGHT), (xianquComboBox, 0, wx.SHAPED),
            #(wx.Size(6, 6), 0, wx.SHAPED | wx.ALIGN_RIGHT) #(wx.Size(6, 6), 1, wx.EXPAND)
        ])
        # panel.SetSizerAndFit(codeSizer)
        #定义一级列表刷新时响应二级列表的刷新事件
        self.__ProvinceComboBox = proviceComboBox
        self.__SecityDict = dict1
        self.__CityComboBox = shiquComboBox
        panel.Bind(wx.EVT_COMBOBOX, self.__OnComboBoxSelected1, proviceComboBox,)
        #定义二级列表的刷新事件
        self.__SecityDict1 = dict2
        self._XianquCombobox = xianquComboBox
        panel.Bind(wx.EVT_COMBOBOX, self.__OnComboBoxSelected2, shiquComboBox,)
        panel.Bind(wx.EVT_COMBOBOX, self.__OnComboBoxSelected3, xianquComboBox,)
        labelText = wx.StaticText(panel, label="日期:")
        codeSizer.Add(labelText, 0, wx.ALIGN_RIGHT)
        codeText = wx.TextCtrl(panel, value='20181125', style=wx.TE_PROCESS_ENTER)
        self.Bind(wx.EVT_TEXT_ENTER, self.OnTextSubmitted, codeText)
        codeSizer.Add(codeText)
        self.list = wx.ListCtrl(panel, wx.NewId(), style=wx.LC_REPORT,)
        self.list.InsertColumn(0, "开始说明")
        self.list.SetColumnWidth(0, 500)
        self.list.InsertItem(0,"您可以从菜单开始使用,或者点击菜单中的help获取帮助:)")
        # self.list.SetItem(pos,1,"
        # self.list.SetColumnWidth(1, 800)
        #codeSizer.SetDimension()
        # codeSizer.Add(self.list,0,wx.EXPAND)
        #codeSizer.SetDimension(4,5,10,6)
        # print('eeee')
        Mysizers = wx.BoxSizer(wx.VERTICAL)
        Mysizers.Add(codeSizer,0,wx.ALL,5 )
        # print('eeee')
        Mysizers.Add(self.list, -1, wx.ALL | wx.EXPAND, 5)
        # print('eeee')
        # print(Mysizers.GetItemCount())
        # try:
        panel.SetSizerAndFit(Mysizers)

        # except ConnectionError as err:
        #     print(err)
        #print('eeee')
        self.Center()
        # self.OnRefresh(None)
    def __OnComboBoxSelected1(self, event):
        currentProvinceIndex1 = self.__ProvinceComboBox.GetSelection()
        # currentShiquIndex2 = self.__CityComboBox.GetSelection()
        if wx.NOT_FOUND == currentProvinceIndex1 :return
        value1 = self.__ProvinceComboBox.GetItems()[currentProvinceIndex1]
        # value2 = self.__CityComboBox.GetItems()[currentShiquIndex2]

        # 注意中文在List dict 等存储时候, utf-8 格式不一致问题
        # value = value.encode('utf-8')

        cityList = self.__SecityDict[value1]
        # xianquList = self.__SecityDict1[value2]
        self.__CityComboBox.SetItems(cityList)
        self.__CityComboBox.SetValue(cityList[0])
        self.__OnComboBoxSelected2(self)
        # self._XianquCombobox.SetItems(xianquList)
        # self._XianquCombobox.SetValue(xianquList[1])
        #panel.Bind(wx.EVT_COMBOBOX, self.__OnComboBoxSelected2, self._XianquCombobox, )
    def __OnComboBoxSelected2(self, event):
        currentShiquIndex = self.__CityComboBox.GetSelection()
        #print(self.__SecityDict1[self.__CityComboBox.GetItems()[currentShiquIndex]])
        if wx.NOT_FOUND == currentShiquIndex: return
        value = self.__CityComboBox.GetItems()[currentShiquIndex]

        # 注意中文在List dict 等存储时候, utf-8 格式不一致问题
        # value = value.encode('utf-8')

        cityList = self.__SecityDict1[value]
        #print(cityList)
        self._XianquCombobox.SetItems(cityList)
        self._XianquCombobox.SetValue(cityList[0])
    def __OnComboBoxSelected3(self,event):
        currentXianquIndex= self._XianquCombobox.GetSelection()
        value = self._XianquCombobox.GetItems()[currentXianquIndex]
        self._cityname = value
    def OnTextSubmitted(self,event):
        self._time = event.GetString()
    def createHeader2forecas(self):
        self.list.InsertColumn(0, "日期")
        self.list.InsertColumn(1, "最高气温")
        self.list.InsertColumn(2, "最低气温")
        self.list.InsertColumn(3, "相对湿度")
        self.list.InsertColumn(4, "降水概率")
        self.list.InsertColumn(5, "能见度")
        self.list.InsertColumn(6, "紫外线级别")
        self.list.InsertColumn(7, "白天天气现象")
        self.list.InsertColumn(8, "夜晚天气现象")
        self.list.InsertColumn(9, "风向")
        self.list.InsertColumn(10, "风力")
        self.list.InsertColumn(11, "风速")
    def createHeader2history(self):
        self.list.InsertColumn(0, "更新时间")
        self.list.InsertColumn(1, '气温')
        self.list.InsertColumn(2, "天气现象")
        self.list.InsertColumn(3, "体感温度")
        self.list.InsertColumn(4, "相对湿度")
        self.list.InsertColumn(5, "降雨量")
        self.list.InsertColumn(6, "风向")
        self.list.InsertColumn(7, "风力")
        self.list.InsertColumn(8, "风速")
        # self.list.InsertColumn(9, "风向")
        # self.list.InsertColumn(10, "风力")
        # self.list.InsertColumn(11, "风速")
    def createHeader2Mhistory(self):
        self.list.InsertColumn(0, "年份")
        self.list.InsertColumn(1, '月份')
        self.list.InsertColumn(2, "最高气温")
        self.list.InsertColumn(3, "最低气温")
        self.list.InsertColumn(4, "平均气温")
        self.list.InsertColumn(5, "降水量")
        # self.list.InsertColumn(6, "风向")
        # self.list.InsertColumn(7, "风力")
        # self.list.InsertColumn(8, "风速")
    def createHeader2Yistory(self):
        self.list.InsertColumn(0, "日期")
        self.list.InsertColumn(1, '晴好天气比率')
        self.list.InsertColumn(2, "降水天气比率")
        self.list.InsertColumn(3, "总降水量")
        self.list.InsertColumn(4, "平均湿度")
        self.list.InsertColumn(5, "平均温度")
        self.list.InsertColumn(6, "日最低气温")
        self.list.InsertColumn(7, "日品均气温")
        self.list.InsertColumn(8, "最常见风向")
        self.list.InsertColumn(9, "平均风速")
    def createHeader2Analyse(self):
        self.list.InsertColumn(0,'生活指数类型')
        self.list.InsertColumn(1, "生活指数简述")
        self.list.InsertColumn(2, "生活指数详情",)
        self.list.SetColumnWidth(2, 600)
    def createHeader2help(self):
        self.list.InsertColumn(0,'菜单选项')
        self.list.SetColumnWidth(0, 100)
        self.list.InsertColumn(1, "选项说明")
        self.list.SetColumnWidth(1, 800)
    def forecas(self,event):
        # xianquV =str(self._XianquCombobox.GetSelection())
        # print(str(self._cityname))
        self._data = my_envirounment.weather_forecast(str(self._cityname))
        forecastes = self._data['forecast']
        if forecastes:
            self.list.ClearAll()
            self.createHeader2forecas()
            pos = 0
            for row in forecastes:
                # print(row)
                temp = row['tmp']
                temp_mi = temp['max']
                temp_ma = temp['min']
                cond = row['cond']
                cond_n = cond['cond_n']
                cond_d = cond['cond_d']
                wind = row['wind']
                dir = wind['dir']
                sc = wind['sc']
                spd = wind['spd']
                pos = self.list.InsertItem(pos + 1, row['date'])
                # x = dt.datetime.utcfromtimestamp(int(row['date']))
                # Mdatetime = dt.datetime.strftime(x,'%Y-%m-%d')
                self.list.SetItem(pos, 1, temp_mi)
                self.list.SetItem(pos, 2, temp_ma)
                self.list.SetItem(pos, 3, row['hum'])
                self.list.SetItem(pos, 4, row['pop'])
                self.list.SetItem(pos, 5, row['vis'])
                self.list.SetItem(pos, 6, row['uv'])
                self.list.SetItem(pos, 7, cond_n)
                self.list.SetItem(pos, 8, cond_d)
                self.list.SetItem(pos, 9, dir)
                self.list.SetItem(pos, 10, sc)
                self.list.SetItem(pos, 11, spd)
                self._forecas_date.append(row['date'])
                self._forecas_hum.append(int(row['hum']))
                self._forecas_max.append(int(temp_mi))
                self._forecas_min.append(int(temp_ma))
                self._forecas_pop.append(int(row['pop']))
                self._forecas_vis.append(int(row['vis']))
                self._forecas_spd.append(int(spd))
                self._forecas_uv.append(int(row['uv']))
                if pos % 2 == 0:
                    # Set new look and feel for odd lines
                    self.list.SetItemBackgroundColour(pos, (134, 225, 249))
        else:
            wx.MessageBox('Download failed.', 'Message', wx.OK | wx.ICON_INFORMATION)
    def Dhistory(self,event):
        # xianquV =str(self._XianquCombobox.GetSelection())
        self._data = my_envirounment.weather_history(str(self._cityname))
        forecastes = self._data ['history']
        if forecastes:
            self.list.ClearAll()
            self.createHeader2history()
            pos = 0
            for row in forecastes:
                self._Dhistory_updatetime.append(row['updatetime'])
                self._Dhistory_temperature.append(float(row['temperature']))
                self._Dhistory_feelst.append(float(row['feelst']))
                self._Dhistory_humidity.append(float(row['humidity']))
                self._Dhistory_rain.append(float(row['rain']))
                self._Dhistory_windspeed.append(float(row['windspeed']))
                pos = self.list.InsertItem(pos + 1, row['updatetime'])
                self.list.SetItem(pos, 1, row['temperature'])
                self.list.SetItem(pos, 2, row['phenomena'])
                self.list.SetItem(pos, 3, row['feelst'])
                self.list.SetItem(pos, 4, row['humidity'])
                self.list.SetItem(pos, 5, row['rain'])
                self.list.SetItem(pos, 6, row['winddirect'])
                self.list.SetItem(pos, 7, row['windpower'])
                self.list.SetItem(pos, 8, row['windspeed'])
                # self.list.SetItem(pos, 9, dir)
                # self.list.SetItem(pos, 10, sc)
                # self.list.SetItem(pos, 11, spd)
                if pos % 2 == 0:
                    # Set new look and feel for odd lines
                    self.list.SetItemBackgroundColour(pos, (134, 225, 249))
        else:
            wx.MessageBox('Download failed.', 'Message', wx.OK | wx.ICON_INFORMATION)
    def Mhistory(self,event):
        if len(self._time) > 4:
            self._time = self._time[0:4]
        # print(self._time)
        self._data = my_envirounment.weather_month_history(str(self._cityname),self._time)
        forecastes = self._data ['info']
        if forecastes:
            self.list.ClearAll()
            self.createHeader2Mhistory()
            pos = 0
            for row in forecastes:
                self._Mhistory_month.append(int(row['month']))
                self._Mhistory_tem_max.append(float(row['tem_max']))
                self._Mhistory_tem_min.append(float(row['tem_min']))
                self._Mhistory_tem_avg.append(float(row['tem_avg']))
                self._Mhistory_pre.append(float(row['pre']))
                pos = self.list.InsertItem(pos + 1, str(row['year']))
                self.list.SetItem(pos, 1, str(row['month']))
                self.list.SetItem(pos, 2, row['tem_max'])
                self.list.SetItem(pos, 3, row['tem_min'])
                self.list.SetItem(pos, 4, row['tem_avg'])
                self.list.SetItem(pos, 5, row['pre'])
                if pos % 2 == 0:
                    # Set new look and feel for odd lines
                    self.list.SetItemBackgroundColour(pos, (134, 225, 249))
        else:
            wx.MessageBox('Download failed.', 'Message', wx.OK | wx.ICON_INFORMATION)
    def Yhistory(self,event):
        # print(self._time)
        # if len(self._time) == 6:
        #     pos = 1
        #     self._time = self._time[0:4]
        self._data = my_envirounment.weather_date_history(str(self._cityname),self._time)
        row = self._data
        # forecastes = data['info']
        if row:
            self.list.ClearAll()
            self.createHeader2Yistory()
            pos = 0
            print(row)
            print(self._time)
            # for row in data:
            pos = self.list.InsertItem(pos + 1, row['date'])
            self.list.SetItem(pos, 1, str(row['sunny_percent']))
            self.list.SetItem(pos, 2, str(row['rain_percent']))
            self.list.SetItem(pos, 3, str(row['rain_full']))
            self.list.SetItem(pos, 4, str(row['hum_avg']))
            self.list.SetItem(pos, 5, row['tem_max'])
            self.list.SetItem(pos, 6, row['tem_min'])
            self.list.SetItem(pos, 7, row['tem_avg'])
            self.list.SetItem(pos, 8, row['wdir_most'])
            self.list.SetItem(pos, 9, str(row['wspd_avg']))
            # self.list.SetItem(pos, 10, sc)
            # self.list.SetItem(pos, 11, spd)
            if pos % 2 == 0:
                # Set new look and feel for odd lines
                self.list.SetItemBackgroundColour(pos, (134, 225, 249))
        else:
            wx.MessageBox('Download failed.', 'Message', wx.OK | wx.ICON_INFORMATION)
    def RFesher(self,event):
        pass
    def OnQuit(self,event):
        self.Close()
        self.Destroy()
    def helps(self,event):
        self.list.ClearAll()
        self.createHeader2help()
        ANniu = ['天气预报','24小时天气','月度天气',
                 '日天气','刷新','分析','帮助','退出']
        text1 = '获得所选择的城市的未来七天的天气预报,一定要点击县区的下拉选框的内容才可以实现功能(以下按键同上)，否则内容为南京的天气预报'
        text2 = '和forcas一样要首先选定县区,其功能为可以获取到所选城市过去二十四小时的天气情况'
        text3 = '获得所选城市指定年份的每个月的天气情况,需要手动输入年份,并且要按Enter键(日天气同上),若字符串长度超过四,截取前四位字符,仅支持2015年以前的查询'
        text4 = '获得所选城市的指定某一天的历史天气情况'
        text5 = '刷新功能,对于本项目没什么实际意义,pass了'
        text6 = '点击按键之前必须要有分析的数据.即要点击前四个按键其中之一,实现数据分析的功能,其中天气预报还会给出生活指数'
        text7 = '获取帮助信息'
        text8 = '退出该程序'
        text = [text1,text2,text3,text4,text5,text6,text7,text8]
        pos = 0
        for i in range(8):
            pos = self.list.InsertItem(pos + 1, ANniu[i])
            self.list.SetItem(pos, 1, text[i])
            if pos % 2 == 0:
                # Set new look and feel for odd lines
                self.list.SetItemBackgroundColour(pos, (134, 225, 249))
    def Analyzers(self,event):
        # print(self._data)
        data = self._data
        if('suggestion' in data.keys()):
            forecastes = data['suggestion']
            self.list.ClearAll()
            self.createHeader2Analyse()
            pos = 0
            if(forecastes['trav']):
                trdata = forecastes['trav']
                pos = self.list.InsertItem(pos + 1, '旅游指数')
                self.list.SetItem(pos, 1, trdata['brf'])
                self.list.SetItem(pos, 2, trdata['txt'])
                if pos % 2 == 0:
                    # Set new look and feel for odd lines
                    self.list.SetItemBackgroundColour(pos, (134, 225, 249))
            if (forecastes['uv']):
                trdata = forecastes['uv']
                pos = self.list.InsertItem(pos + 1, '紫外线指数')
                self.list.SetItem(pos, 1, trdata['brf'])
                self.list.SetItem(pos, 2, trdata['txt'])
                if pos % 2 == 0:
                    # Set new look and feel for odd lines
                    self.list.SetItemBackgroundColour(pos, (134, 225, 249))
            if (forecastes['flu']):
                trdata = forecastes['flu']
                pos = self.list.InsertItem(pos + 1, '流感指数')
                self.list.SetItem(pos, 1, trdata['brf'])
                self.list.SetItem(pos, 2, trdata['txt'])
                if pos % 2 == 0:
                    # Set new look and feel for odd lines
                    self.list.SetItemBackgroundColour(pos, (134, 225, 249))
            if (forecastes['comf']):
                trdata = forecastes['comf']
                pos = self.list.InsertItem(pos + 1, '舒适度指数')
                self.list.SetItem(pos, 1, trdata['brf'])
                self.list.SetItem(pos, 2, trdata['txt'])
                if pos % 2 == 0:
                    # Set new look and feel for odd lines
                    self.list.SetItemBackgroundColour(pos, (134, 225, 249))
            if (forecastes['sport']):
                trdata = forecastes['sport']
                pos = self.list.InsertItem(pos + 1, '运动感指数')
                self.list.SetItem(pos, 1, trdata['brf'])
                self.list.SetItem(pos, 2, trdata['txt'])
                if pos % 2 == 0:
                    # Set new look and feel for odd lines
                    self.list.SetItemBackgroundColour(pos, (134, 225, 249))
            if (forecastes['air']):
                trdata = forecastes['air']
                pos = self.list.InsertItem(pos + 1, '空气指数')
                self.list.SetItem(pos, 1, trdata['brf'])
                self.list.SetItem(pos, 2, trdata['txt'])
                if pos % 2 == 0:
                    # Set new look and feel for odd lines
                    self.list.SetItemBackgroundColour(pos, (134, 225, 249))
            if (forecastes['cw']):
                trdata = forecastes['cw']
                pos = self.list.InsertItem(pos + 1, '洗车指数')
                self.list.SetItem(pos, 1, trdata['brf'])
                self.list.SetItem(pos, 2, trdata['txt'])
                if pos % 2 == 0:
                    # Set new look and feel for odd lines
                    self.list.SetItemBackgroundColour(pos, (134, 225, 249))
            if (forecastes['drs']):
                trdata = forecastes['drs']
                pos = self.list.InsertItem(pos + 1, '穿衣指数')
                self.list.SetItem(pos, 1, trdata['brf'])
                self.list.SetItem(pos, 2, trdata['txt'])
                if pos % 2 == 0:
                    # Set new look and feel for odd lines
                    self.list.SetItemBackgroundColour(pos, (134, 225, 249))
            Datef = {'spd':self._forecas_spd,'hum':self._forecas_hum,'uv':self._forecas_uv,
                    'temp_max':self._forecas_max,'temp_mix':self._forecas_min,'vis':self._forecas_vis,
                     'pop':self._forecas_pop}
            # print(Datef)
            quotesdf = pd.DataFrame(Datef)
            quotesdf.index = self._forecas_date
            quotesdf.plot()
            plt.show()
        if('history' in data.keys()):
            Datef = {'temperature':self._Dhistory_temperature,'windspeed':self._Dhistory_windspeed,
                     'rain':self._Dhistory_rain,'humidity':self._Dhistory_humidity,
                     'feels':self._Dhistory_feelst}
            quotesdf = pd.DataFrame(Datef)
            quotesdf.index = self._Dhistory_updatetime
            quotesdf.plot()
            plt.show()
        # elif(data[])
        if('info' in data.keys()):
            Datef = {'tem_max':self._Mhistory_tem_max,
                     'tem_min':self._Mhistory_tem_avg,'tem_avg':self._Mhistory_tem_avg,
                     'pre':self._Mhistory_pre}
            quotesdf = pd.DataFrame(Datef)
            quotesdf.index = self._Mhistory_month
            quotesdf.plot()
            plt.show()
        if data.items() == 0:
            wx.MessageBox('Download failed.', 'Message', wx.OK | wx.ICON_INFORMATION)

    # def OnRefresh(self, event):
    #     thrend.start_new_thread(self.forecas,())
    # def retrieve_quotes(self):
    #     xianquV = self._XianquCombobox.GetItems()
    #     data = my_envirounment.weather_forecast(xianquV)
    #     if data:
    #         self.setData(data)
    #     else:
    #         wx.MessageBox('Download failed.', 'Message', wx.OK | wx.ICON_INFORMATION)
if __name__ == '__main__':
    app = wx.App()
    frame = MyfirstFram(None)
    frame.Show(True)
    app.MainLoop()