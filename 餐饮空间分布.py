# -*- coding: utf-8 -*-
"""
Created on Sat Oct 13 14:58:33 2018

@author: 安东
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
from bokeh.plotting import figure,show,output_file
from bokeh.models import ColumnDataSource
os.chdir('C:\\Users\\安东\\Desktop')
#导入数据
df = pd.read_excel('项目07城市餐饮店铺选址分析\\result_point.xlsx',sheetname = 0)
df.fillna(0,inplace = True)
df.columns = ['rkmd','dlcd','cy_count','sc_count','lng','lat']
df['rkmd_nor'] = (df['rkmd'] - df['rkmd'].min()) / (df['rkmd'].max() - df['rkmd'].min())
df['dlmd_nor'] = (df['dlcd'].max() - df['dlcd']) /(df['dlcd'].max() - df['dlcd'].min())
df['cy_count_nor'] = (df['cy_count'] - df['cy_count'].min()) /(df['cy_count'].max() - df['cy_count'].min())
df['sc_count_nor'] = (df['sc_count'] - df['sc_count'].min()) / (df['sc_count'].max() - df['sc_count'].min())
df['final_result'] = df['rkmd_nor'] *0.4 + df['dlmd_nor'] *0.2 + df['cy_count_nor'] *0.3 + df['sc_count_nor']*0.1
df1 = df.sort_values(by= 'final_result',ascending = False).reset_index(drop = True)

from bokeh.models import HoverTool
hover = HoverTool(tooltips = [('经度','@lng'),
                              ('纬度','@lat'),
                              ('最终得分','@final_result')
                                ])
df1['size'] = df1['final_result'] *20
df1['color_sc'] = '#12B395'
df1['color_sc'].iloc[:10] = 'red'
source = ColumnDataSource(data = df1)
p = figure(plot_width = 800,plot_height = 800,title = '素菜馆最佳位置选址',
           tools=[hover,'box_select,reset,xwheel_zoom,pan,crosshair'])
#p.square(x = 'lng',y = 'lat',source = source,color = 'color_ll',alpha = 0.6)
p.square(x = 'lng',y = 'lat',source = source,color = 'color_sc',
         fill_alpha= 0.3,size = 'size',line_color= 'black')
show(p)
