import pandas as pd
import requests  as re
import json
import pinyin
import numpy as np

file_path = '/home/tlxy/tulingxueyuan/python玩转数据/可视化数据/areaid.csv'
def city2code(cityname):
    csv_file = pd.read_csv(file_path)
    list_index = [i for i in csv_file.NAMEEN]
    #pd.DataFrame(csv_file,index = list_index,columns= list_columns)
    csv_file.index = list_index
    csv_file1 = csv_file.drop(['NAMECN'], axis = 1)
    value = csv_file1.at[cityname, 'AREAID']
    #value_f = list(value)
    #print(type(value))
    if type(value) is np.int64:
        return value
    else:
        return value[0]
    #try:
    #     name = csv_file1.loc[cityname, 'AREAID']
    # except:
    #     name = csv_file.at[cityname,'AREAID']
    #print(csv_file1.loc[cityname,'AREAID'])
    #dir(csv_file1.loc[cityname,'AREAID'])
    #return value[1]
    # return name

#使用pandas读取excel文件
def palceName():
    csv_file = pd.read_csv(file_path)
    #list_columns = ['PROVCN','DISTRICTCN','NAMECN','AREAID']
    list_index = [i for i in csv_file.NAMEEN]
    #pd.DataFrame(csv_file,index = list_index,columns= list_columns)
    csv_file.index = list_index
    csv_file1 = csv_file.drop(['NAMEEN'], axis = 1)
    list_P = csv_file1.PROVCN
    list_D = csv_file1.DISTRICTCN
    #list_N = csv_file1.NAMECN
    #print(csv_file1)#显示出读入excel文件中的表名字
    Shengfen_1 = set(i for i in list_P)
    Shengfen = list(Shengfen_1)
    #print(Shengfen)
    list1_W = []
    for i in Shengfen:
        #dict2 = {}
        #name_py = pinyin.get(i, format="strip", delimiter="")
        #print(name_py)
        #citycode_f = city2code(name_py)
        #print(citycode_f)
        # list_n_index = []
        # for i in csv_file.PROVCN:
        #     name_py = pinyin.get(i, format="strip", delimiter="")
        #     list_n_index.append(name_py)
        csv_file_c = csv_file.copy()
        #print(csv_file_c)
        csv_file_c.index = [i for i in csv_file_c.PROVEN]
        #print(csv_file_c)
        shenfen_py = pinyin.get(i, format="strip", delimiter="")
        csv_file_c_s =  csv_file_c.loc[shenfen_py,'DISTRICTCN']
        #print(csv_file_c_s)
        set_F = set(csv_file_c_s)
        #print(set_F)
        list_f = [i for i in set_F]
        # print(list_f)
        list1_W.append(list_f)
        #Datfram_D = csv_file_c.groupby('PROVEN').DISTRICTCN
        #print(Datfram_D)
        #list_s = Datfram_D.DISTRICTCN
        #list1_D.append(list_s)
        #print(list_D)
    dict_1 = dict(zip(Shengfen,list1_W))
    #print(dict_1)
        # for i in list_s:
        #     name_py = pinyin.get(i, format="strip", delimiter="")
        #     citycode_f = city2code(name_py)
        #     Datfram_L = csv_file1.groupby(citycode_f)
        #     list_L = Datfram_L.DISTRICTCN
        #Dict = dict(list_D)

    Shiqu_1 =  set(i for i in list_D)
    Shiqu = list(i for i in Shiqu_1)
    #print(Shiqu)
    list1_N = []
    for i in Shiqu:
        #name_py = pinyin.get(i, format="strip", delimiter="")
        #citycode_f = city2code(name_py)
        #csv_file_c = csv_file.copy()
        #print(i)
        csv_file_c_f = csv_file.copy()
        csv_file_c_f.index = [i for i in csv_file.DISTRICTEN]
        shiqu_py = pinyin.get(i, format="strip", delimiter="")
        csv_file_c_s = csv_file_c_f.loc[shiqu_py, 'NAMECN']
        #print(type(csv_file_c_s))
        if type(csv_file_c_s) is str:
            str_list = [csv_file_c_s]
            #print(str_list)
            list1_N.append(str_list)
        else:
            set_g = set(csv_file_c_s)
            #print(type(set_g))
            list_q = [i for i in set_g]
            # if len(set_g) == 1:
            #     list_g = list(set_g)
            # else:
            #     list_g = [i for i in set_g]
            #print(list_q)
            list1_N.append(list_q)

        #Datfram_D = csv_file1.groupby(list_n_index)
        #list_s = Datfram_D.NAMECN
        #list1_N.append(list_s)
    dict_2 = dict(zip(Shiqu, list1_N))
    #r_list = list(dict_1,dict_2)
    #print(r_list)
    # XianQu_1 = csv_file1.NAMECN
    # XianQu = list(i for i in XianQu_1)
    #list_v = list(Shengfen+Shiqu+XianQu)
    #print(list_v)
    # print(dict_1,dict_2)
    return dict_1,dict_2
    #print(Shengfen,Shiqu,XianQu)

def weather_forecast(cityname):
    name_py = pinyin.get(cityname, format="strip", delimiter="")
    citycode_f = city2code(name_py)
    citycode = citycode_f
    #print(citycode_f)
    # if(len(citycode_f) > 1):
    #     citycode = citycode_f[0]
    # else:
    #     citycode = citycode_f
    #print(citycode)
    url = 'http://service.envicloud.cn:8082/v2/weatherforecast/AMFJAY1JYWKXNTQYOTCXMJK2NZM0/%s'%citycode
    payload = ""
    headers = {
        'cache-control': "no-cache"
    }

    response = re.request("GET", url, data=payload, headers=headers)
    #r = re.get('http://service.envicloud.cn:8082//v2/weatherforecast/AMFJAY1JYWKXNTQYOTCXMJK2NZM0/%s',(citycode))
    #print()
    return json.loads(response.text)
def weather_history(cityname):
    name_py = pinyin.get(cityname, format="strip", delimiter="")
    citycode = city2code(name_py)
    # for i in city2code(name_py):
    #     citycode_f.append(i)
    #citycode_f = list(i for i in city2code(name_py))
    #print(citycode_f)
    # if(len(citycode_f) > 1):
    #     citycode = citycode_f[0]
    # else:
    #     citycode = citycode_f
    #print(citycode)
    url = 'http://service.envicloud.cn:8082/v2/weatherhistory/AMFJAY1JYWKXNTQYOTCXMJK2NZM0/%s' % citycode
    payload = ""
    headers = {
        'cache-control': "no-cache"
    }

    response = re.request("GET", url, data=payload, headers=headers)
    return json.loads(response.text)
def weather_month_history(city,year):
    name_py = pinyin.get(city, format="strip", delimiter="")
    #citycode_f = list(city2code(name_py))
    #print(citycode_f)
    citycode = city2code(name_py)
    # for i in city2code(name_py):
    #     citycode_f.append(i)
    # if(len(citycode_f) > 1):
    #     citycode = citycode_f[0]
    # else:
    #     citycode = citycode_f
    #print(citycode)
    url = 'http://service.envicloud.cn:8082/v2/monthlymete/AMFJAY1JYWKXNTQYOTCXMJK2NZM0/%s/%s' % (citycode,year)
    payload = ""
    headers = {
        'cache-control': "no-cache"
    }
    response = re.request("GET", url, data=payload, headers=headers)
    return json.loads(response.text)
def weather_date_history(city,date):
    name_py = pinyin.get(city, format="strip", delimiter="")
    # citycode_f = list(i for i in city2code(name_py))
    citycode = city2code(name_py)
    #print(citycode_f)
    # if(len(citycode_f) > 1):
    #     citycode = citycode_f[0]
    # else:
    #     citycode = citycode_f
    #print(citycode)
    url = 'http://service.envicloud.cn:8082/v2/weatherhistory/AMFJAY1JYWKXNTQYOTCXMJK2NZM0/%s/%s' % (citycode,date)
    payload = ""
    headers = {
        'cache-control': "no-cache"
    }
    response = re.request("GET", url, data=payload, headers=headers)
    return json.loads(response.text)

if __name__ == '__main__':
    name = '南京'
    Mlist = list(palceName())
    Mdict0 = Mlist[1]
    Mlist1 = Mdict0.values()
    list1 = []
    for i in Mlist1:
        list1 +=i
    csv_file = pd.read_csv(file_path)
    list_B = csv_file.loc[:,['NAMEEN']]
    list2 =[i for i in list_B.NAMEEN]
    for i in range(len(list1)):
        shiqu_py = pinyin.get(list1[i], format="strip", delimiter="")
        try:
            if shiqu_py not in list2:
                print(list1[i],shiqu_py)
        except:
            pass
    # print(list2)
    # print(list1)
    #name_py = pinyin.get(name, format="strip", delimiter="")
    #help()
    # w = weather_date_history(name,20170722)
    # print(w)
    #w1 = json.loads(w) #将文本格式转化为字典格式
    # for i in w1:
    #      print(i)
    # print(w1['rdesc'])
    #palceName()
    # Y = palceName()
    # print(w)