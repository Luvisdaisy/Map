# @description
# @Author: F·守坤
# @Date: 2022/10/31 9:51
# @remarks
from pyecharts.charts import Page

# coding:utf-8
from system_controller import Controlloer

if __name__ == '__main__':
    controller = Controlloer()
    # controller.run()
    Page.save_resize_html('./html/中国疫情可视化.html', cfg_file='chart_config.json', dest='./html/中国疫情可视化_draggable.html')
