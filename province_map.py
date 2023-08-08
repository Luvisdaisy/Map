# @description
# @Author: F·守坤
# @Date: 2022/10/30 19:34
# @remarks      省级地图

# coding:utf-8
from pyecharts import options as opts
from pyecharts.charts import Map, Pie, Bar, Grid, Page
import pandas as pd
import datetime
import translate_city

from pyecharts.commons.utils import JsCode

class ProvincesMap(object):
    def __init__(self):
        self.maps = []
        self.pies = []
        self.bars = []
        self.grids = []
        self.provinces = None
        self.data_pairs = []
        self.js_code_str = """
                    function(params) {
                        console.log(params);
                        var n = params.data.name + '<br/>';
                        var v = params.data.value;
                        var res = n + v;
                        return res;
                    }
                    """

    def set_pairs(self):
        for province in self.provinces:
            translate_province = translate_city.provinces[province]
            df = pd.read_csv('./data/province_data/' + translate_province + '_covid_19.csv')  # 利用pandas读取数据
            city_list = list(df['城市'])
            translate_city_list = []
            data_list = []
            for i in range(len(city_list)):
                translate_city_list.append(translate_city.city[province][city_list[i]])
                data_list.append([list(df['现存确诊'])[i], list(df['累计确诊'])[i], list(df['死亡'])[i], list(df['治愈'])[i]])
            self.data_pairs.append([x for x in zip(translate_city_list, data_list)])

    def set_province_map(self):
        # 创建地图实例
        i = 0
        for province in self.provinces:
            translate_province = translate_city.provinces[province]
            map = Map(init_opts=opts.InitOpts(theme='light', width='1850px', height='600px', page_title=translate_province+"疫情地图")) \
                .add(
                series_name="",
                data_pair=self.data_pairs[i],
                maptype=province,
                name_map=translate_city.city[province],
                label_opts=opts.LabelOpts(
                    is_show=True,
                    position='inside'),
                is_map_symbol_show=False, ) \
                .set_global_opts(   # 添加标题
                title_opts=opts.TitleOpts(
                    title=province + "疫情新增确诊",
                    pos_left="center",
                    pos_top="20",
                    title_textstyle_opts=opts.TextStyleOpts(
                        font_size=24,
                        font_family="Microsoft YaHei"),
                    subtitle='统计时间截止至' + str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")) + ' 时',
                    subtitle_textstyle_opts=opts.TextStyleOpts(
                        font_size=12, font_family="Microsoft YaHei"),
                ),
                tooltip_opts=opts.TooltipOpts(
                    is_show=True,
                    formatter=JsCode(self.js_code_str)
                ),
                visualmap_opts=opts.VisualMapOpts(     # 视觉映射配置
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
            self.maps.append(map)
            i += 1

    def set_province_pie(self):
        for province in self.provinces:
            translate_province = translate_city.provinces[province]
            df = pd.read_csv('./data/province_data/' + translate_province + '_covid_19.csv')  # 利用pandas读取数据

            pie = Pie() \
                .add(
                "现存确诊",
                [list(z) for z in zip(list(df['城市']), list(df['现存确诊']))],
                center=["65%", "61%"],
                radius=[60, 80],
            ) \
                .add(
                "治愈",
                [list(z) for z in zip(list(df['城市']), list(df['治愈']))],
                center=["80%", "61%"],
                radius=[60, 80],
            ) \
                .set_global_opts(
                title_opts=opts.TitleOpts(title='现存确诊  治愈', pos_left="67%", pos_bottom="70%"),
                legend_opts=opts.LegendOpts(
                    type_="scroll", pos_top="20%", pos_right="5%", orient="vertical"
                )
            )
            self.pies.append(pie)

    def set_province_bar(self):
        for province in self.provinces:
            translate_province = translate_city.provinces[province]
            df = pd.read_csv('./data/province_data/' + translate_province + '_covid_19.csv')  # 利用pandas读取数据

            bar = Bar(init_opts=opts.InitOpts(width='925px', height='800px'))\
                .add_xaxis(list(df['城市']))\
                .add_yaxis("治愈", list(df['治愈']))\
                .add_yaxis("累计确诊", list(df['累计确诊']))\
                .set_global_opts(xaxis_opts=opts.AxisOpts(name='城市'),
                                 yaxis_opts=opts.AxisOpts(name='人数'),
                                 tooltip_opts=opts.TooltipOpts(is_show=True,
                                                               trigger_on='mousemove|click',
                                                               axis_pointer_type='cross'),
                                 datazoom_opts=[opts.DataZoomOpts(), opts.DataZoomOpts(type_="inside", is_show=False)],
                                 legend_opts=opts.LegendOpts(is_show=True))
            self.bars.append(bar)

    def set_grid(self):
        i = 0
        for province in self.provinces:
            grid = (
                Grid(init_opts=opts.InitOpts(width='1850px', height='400px'))
                .add(self.bars[i], grid_opts=opts.GridOpts(pos_right="55%"))
                .add(self.pies[i], grid_opts=opts.GridOpts(pos_left="50%"))
            )
            self.grids.append(grid)
            i += 1

    def set_page(self):
        i = 0
        for province in self.provinces:
            translate_province = translate_city.provinces[province]
            Page(layout=Page.SimplePageLayout)\
                .add(self.maps[i], self.grids[i])\
                .render('./html/province_html/' + translate_province + '疫情地图.html')
            i += 1
