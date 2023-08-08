# @description
# @Author: F·守坤
# @Date: 2022/10/31 9:49
# @remarks      核心控制

# coding:utf-8
from spider import Spider
from china_map import ChinaMap
from province_map import ProvincesMap
from file_handler import FileHandler

class Controlloer(object):
    def __init__(self):
        self.spider = Spider()
        self.china_map = ChinaMap()
        self.file_handler = FileHandler()
        self.province_map = ProvincesMap()

    def __run_spider(self):
        html = self.spider.post_html()
        self.spider.write_china_file(html)
        self.spider.write_province_file(html)
        self.spider.write_china_total_data(html)

    def __run_china_map(self):
        self.china_map.set_pairs()
        self.china_map.set_china_map()
        self.china_map.set_china_pie()
        self.china_map.set_china_bar()
        self.china_map.set_data_bar()
        self.china_map.set_page()

    def __run_province_map(self):
        provinces = self.file_handler.get_provinces()
        self.file_handler.div_provinces_file(provinces)
        self.province_map.provinces = provinces
        self.province_map.set_pairs()
        self.province_map.set_province_map()
        self.province_map.set_province_pie()
        self.province_map.set_province_bar()
        self.province_map.set_grid()
        self.province_map.set_page()
        self.china_map.add_link()

    def run(self):
        self.__run_spider()
        self.__run_china_map()
        self.__run_province_map()
