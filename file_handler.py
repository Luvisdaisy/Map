# @description
# @Author: F·守坤
# @Date: 2022/10/31 10:01
# @remarks      csv文件处理

# coding:utf-8
import pandas as pd
import translate_city

class FileHandler(object):
    def __init__(self):
        # 利用pandas读取数据,     handle[0]表示选取文件的第一行作为表头， handle[1]表示选取文件的第二行作为表头
        self.df = pd.read_csv('./data/province_covid_19.csv', header=[1])

    def get_provinces(self):
        # 列csv文件中所有列
        self.df.columns = ['province', '城市', '现存确诊', '累计确诊', '死亡', '治愈']
        # 删除省份列中的重复项,得到全部唯一省份
        data_cate = self.df.drop_duplicates(subset=['province'])
        return data_cate.province

    def div_provinces_file(self, provinces):
        for province in provinces:
            translate_province = translate_city.provinces[province]
            self.df[self.df.province == province].to_csv("./data/province_data/" + translate_province + "_covid_19.csv", index=False)

class DataHandler(object):
    def __init__(self):
        # 利用pandas读取数据,     handle[0]表示选取文件的第一行作为表头， handle[1]表示选取文件的第二行作为表头
        self.df = pd.read_csv('./data/china_total_data.csv', header=[1])

    def get_data_head_list(self):
        return list(self.df.columns.values)

    def get_data_list(self):
        return list(self.df.iloc[0])
