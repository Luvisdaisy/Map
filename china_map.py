# @description
# @Author: F·守坤
# @Date: 2022/10/28 10:44
# @remarks      中国地图
from __future__ import unicode_literals

# coding:utf-8
from pyecharts import options as opts
from pyecharts.charts import Map, Grid, Pie, Bar, Page

import pandas as pd
import datetime

import translate_city
from file_handler import DataHandler

from pyecharts.commons.utils import JsCode


class ChinaMap(object):
    def __init__(self):
        self.page = None
        self.map = None
        self.pie = None
        self.data_bar = None
        self.bar = None
        self.data_pairs = []
        self.js_code_strs = """
                    function(params) {
                        console.log(params);
                        var res = params.data.name + '<br/>';
                        var seriesName = params.seriesName;
                        var value = params.data.value;
                        res += seriesName + ':' + value;
                        return res;
                    }
                    """

    @staticmethod
    def read_csv():
        df = pd.read_csv('./data/china_covid_19.csv', header=[1])  # 利用pandas读取数据
        return df

    def set_pairs(self):
        df = self.read_csv()
        province_list = list(df['地区'])  # 各省/区的名字列表
        # 由于抓包的数据与地图需要显示的数据不同，需要转换
        translate_province_list = []
        for i in range(len(province_list)):
            translate_province_list.append(translate_city.provinces[province_list[i]])
        econ_num_list = list(df['现存确诊'])
        con_num_list = list(df['累计确诊'])
        death_num_list = list(df['死亡'])
        cure_num_list = list(df['治愈'])
        self.data_pairs.append([x for x in zip(translate_province_list, econ_num_list)])
        self.data_pairs.append([x for x in zip(translate_province_list, con_num_list)])
        self.data_pairs.append([x for x in zip(translate_province_list, death_num_list)])
        self.data_pairs.append([x for x in zip(translate_province_list, cure_num_list)])

    def set_china_map(self):
        # 创建一个地图实例
        self.map = Map(init_opts=opts.InitOpts(chart_id='1', width='1000px', height='800px', theme='light')) \
            .add(
            series_name="现存确诊",
            data_pair=self.data_pairs[0],
            maptype="china",
            label_opts=opts.LabelOpts(
                is_show=True,
                position='inside',
            ),
            is_map_symbol_show=False,
        ) \
            .add(
            series_name="累计确诊",
            data_pair=self.data_pairs[1],
            maptype="china",
            label_opts=opts.LabelOpts(
                is_show=True,
                position='inside',
            ),
            is_map_symbol_show=False,
        ) \
            .add(
            series_name="死亡",
            data_pair=self.data_pairs[2],
            maptype="china",
            label_opts=opts.LabelOpts(
                is_show=True,
                position='inside',
            ),
            is_map_symbol_show=False,
        ) \
            .add(
            series_name="治愈",
            data_pair=self.data_pairs[3],
            maptype="china",
            label_opts=opts.LabelOpts(
                is_show=True,
                position='inside',
            ),
            is_map_symbol_show=False,
        ) \
            .set_global_opts(  # 添加标题
            title_opts=opts.TitleOpts(
                title="全国疫情新增确诊",
                pos_left='center',
                pos_top='20',
                title_textstyle_opts=opts.TextStyleOpts(
                    font_size=24,
                    font_family="Microsoft YaHei"),
                subtitle='统计时间截止至' + str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")) + ' 时',
                subtitle_textstyle_opts=opts.TextStyleOpts(
                    font_size=12, font_family="Microsoft YaHei"),
            ),
            tooltip_opts=opts.TooltipOpts(  # 视觉映射配置
                is_show=True,
                formatter=JsCode(self.js_code_strs)
            ),
            visualmap_opts=opts.VisualMapOpts(
                max_=99999,
                is_piecewise=True,
                dimension=0,
                pos_left="10",
                pos_bottom="20",
                pieces=[
                    {'min': 0, 'max': 99, 'label': '0-99', 'color': '#FFFFCC'},
                    {'min': 100, 'max': 499, 'label': '100-499', 'color': '#FFC4B3'},
                    {'min': 500, 'max': 999, 'label': '500-999', 'color': '#FF9985'},
                    {'min': 1000, 'max': 4999, 'label': '1000-4999', 'color': '#F57567'},
                    {'min': 5000, 'max': 9999, 'label': '5000-9999', 'color': '#E64546'},
                    {'min': 10000, 'max': 49999, 'label': '10000-49999', 'color': '#B80909'},
                    {'min': 50000, 'max': 99999, 'label': '>=50000', 'color': '#660000'}
                ]
            )
        )

    def set_china_pie(self):
        df = self.read_csv()
        # 反选除了香港澳门台湾
        # df = df[~df['地区'].isin(['香港'])]
        # df = df[~df['地区'].isin(['澳门'])]
        # df = df[~df['地区'].isin(['台湾'])]

        self.pie = Pie(init_opts=opts.InitOpts(chart_id='2', theme='light'))
        self.pie.add(
            "治愈",
            [list(z) for z in zip(list(df['地区']), list(df['治愈']))],
            center=["30%", "50%"],
            radius=[60, 80],
        ) \
            .add(
            "死亡",
            [list(z) for z in zip(list(df['地区']), list(df['死亡']))],
            center=["60%", "50%"],
            radius=[60, 80],
        ) \
            .set_global_opts(
            title_opts=opts.TitleOpts(title='治愈  死亡', pos_left="42%", pos_bottom="70%"),
            legend_opts=opts.LegendOpts(
                type_="scroll", pos_top="20%", pos_right="5%", orient="vertical"
            )
        )

    def set_china_bar(self):
        df = self.read_csv()
        # 反选除了香港澳门
        # df = df[~df['地区'].isin(['香港'])]
        # df = df[~df['地区'].isin(['澳门'])]
        # df = df[~df['地区'].isin(['台湾'])]

        self.bar = Bar(init_opts=opts.InitOpts(chart_id='3', theme='light'))
        self.bar.add_xaxis(list(df['地区'])) \
            .add_yaxis("治愈", list(df['治愈']), itemstyle_opts=opts.ItemStyleOpts(color='red')) \
            .add_yaxis("累计确诊", list(df['累计确诊'])) \
            .set_global_opts(xaxis_opts=opts.AxisOpts(name='省份'),
                             yaxis_opts=opts.AxisOpts(name='人数'),
                             tooltip_opts=opts.TooltipOpts(
                                 is_show=True,
                                 trigger_on='mousemove|click',
                                 axis_pointer_type='cross'),
                             datazoom_opts=[opts.DataZoomOpts(), opts.DataZoomOpts(type_="inside", is_show=False)],
                             legend_opts=opts.LegendOpts(is_show=True))

    def set_data_bar(self):
        data_handler = DataHandler()
        data_head = data_handler.get_data_head_list()
        data = data_handler.get_data_list()
        self.data_bar = Bar(init_opts=opts.InitOpts(chart_id='4', theme='light', page_title="全国病例数据")) \
            .add_xaxis(data_head) \
            .add_yaxis("", data) \
            .reversal_axis() \
            .set_series_opts(label_opts=opts.LabelOpts(position="right")) \
            .set_global_opts(xaxis_opts=opts.AxisOpts(name='人数'),
                             tooltip_opts=opts.TooltipOpts(  # 视觉映射配置
                                 is_show=True,
                                 trigger_on='mousemove|click',
                                 axis_pointer_type='cross'),
                             datazoom_opts=opts.DataZoomOpts(type_="inside"),
                             legend_opts=opts.LegendOpts(is_show=True),
                             )

    def set_page(self):
        self.page = Page(layout=Page.DraggablePageLayout, page_title='中国疫情可视化')
        self.page.add(self.map, self.bar, self.pie, self.data_bar) \
            .render('./html/中国疫情可视化.html')

    def add_link(self):
        js_code = '''
                    <style>
                    #mySidenav a {
                      position: absolute;
                      left: -80px;
                      transition: 0.3s;
                      padding: 15px;
                      width: 100px;
                      text-decoration: none;
                      font-size: 20px;
                      color: white;
                      border-radius: 0 5px 5px 0;
                    }
                    #mySidenav a:hover {
                      left: 0;
                    }
                    #map_screen {
                      top: 20px;
                      background-color: #4CAF50;
                    }
                    #map {
                      top: 80px;
                      background-color: #2196F3;
                    }
                    </style>
        
                    <script>
                        chart_''' + self.map.chart_id + '''.on('click', function (param){
                            var selected = param.name;
                            if (selected == '香港' || selected == '台湾') {
                            } else {
                                location.href = './province_html/' + selected + '疫情地图.html';
                            }
                        });

                        var div = document.createElement("div");
                        div.innerHTML = '<div id="mySidenav" class="sidenav"><a href="./中国疫情可视化.html" id="map_screen">疫情可视化</a><a href="../html/map.html" id="map">路线分析</a></div>';
                        document.body.appendChild(div);
                    </script>
                    '''
        with open('./html/中国疫情可视化.html', 'a', encoding="utf-8") as f:
            f.write(js_code)
