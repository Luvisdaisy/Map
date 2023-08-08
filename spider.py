# @description
# @Author: F·守坤
# @Date: 2022/10/28 9:03
# @remarks      数据抓取

import datetime

# coding:utf-8
import json
import requests
import re
import translate_city

class Spider(object):
    def __init__(self):
        self.url = 'https://news.sina.com.cn/project/fymap/ncp2020_full_data.json?_=1674449419691'  # 全国新增

        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36"
        }

    def post_html(self):
        html = requests.get(url=self.url, headers=self.headers).text
        # 去除抓取到json的前后无用数据
        html = re.sub('^jsoncallback\(', '', html)
        html = re.sub('\);$', '', html)
        html = json.loads(html)
        return html

    @staticmethod
    def __get_data(html):
        return html['data']

    def write_china_file(self, html):
        provinces = self.__get_data(html)['list']
        with open("./data/china_covid_19.csv", "w+", encoding="utf-8") as f:
            f.write(str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")) + "\n")
            f.write("地区,现存确诊,累计确诊,死亡,治愈\n")

            for province in provinces:
                province_name = province['name']
                # translate_province_name = translate_city.provinces[province_name]
                econ_num = province['econNum']                  # 现存确诊
                value = province['value']                       # 累计确诊
                death_num = province['deathNum']                # 死亡
                cure_num = province['cureNum']                  # 治愈

                f.write(province_name + "," + str(econ_num) + "," + str(value) + "," + str(death_num) + "," + str(cure_num) + "\n")

    def write_province_file(self, html):
        provinces = self.__get_data(html)['list']
        with open("./data/province_covid_19.csv", "w+", encoding="utf-8") as f:
            f.write(str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")) + "\n")
            f.write("province,城市,现存确诊,累计确诊,死亡,治愈\n")

            for province in provinces:
                province_name = province['name']               # 省份
                # translate_province_name = translate_city.provinces[province_name]
                cities = province['city']                      # 城市
                for city in cities:
                    city_name = city['name']
                    result = re.search(r'外', city_name)
                    if result != None or city_name == "经济开发区" \
                            or city_name == "省十里丰监狱" or city_name == "高新区" \
                            or city_name == "两江新区" or city_name == "公主岭" \
                            or city_name == "平潭综合实验区" or city_name == "赣江新区"\
                            or city_name == "韩城" or city_name == "杨凌示范区"\
                            or city_name == "雄安新区" or city_name == "第四师"\
                            or city_name == "第七师" or city_name == "第九师"\
                            or city_name == "第十二师" or city_name == "宁东":
                        continue
                    econ_num = city['econNum']                          # 现存确诊
                    con_num = city['conNum']                            # 累计确诊
                    death_num = city['deathNum']                        # 死亡
                    cure_num = city['cureNum']                          # 治愈

                    f.write(province_name + "," + city_name + "," + str(econ_num) + "," + con_num + "," + death_num + "," + cure_num + "\n")

    def write_china_total_data(self, html):
        data = self.__get_data(html)
        with open("./data/china_total_data.csv", "w+", encoding="utf-8") as f:
            f.write(str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")) + "\n")
            f.write("现存本土确诊,现存确诊,现存重症,累计确诊,累计境外输入,累计治愈, 累计死亡\n")
            f.write(str(data['locIncrNum']) + ',' + str(data['econNum']) + ',' + str(data['heconNum'])
                    + ',' + str(data['gntotal']) + ',' + str(data['jwsrNum']) + ',' + str(data['curetotal']) + ',' + str(data['deathtotal']))
