# -*- coding: utf-8 -*-
"""
Created on Fri Oct 12 23:51:15 2018

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
plt.rcParams['font.sans-serif'] = ['SimHei']  
plt.rcParams['axes.unicode_minus'] = False    
sns.set(font_scale=1.5,font='SimHei')

#导入数据
data = pd.read_excel('项目07城市餐饮店铺选址分析\\上海餐饮数据.xlsx',sheetname = 0)
#清洗为零的值
data = data.replace(0,np.nan)
data.dropna(inplace = True)
#去除各项指标的上限异常值
m = ['口味','环境','服务','人均消费']
for n in m:
    a = data[n].describe()
    iqr = a['75%'] - a['25%'] 
    data = data[(data[n] > a['25%'] - 3 * iqr) & (data[n] < a['75%'] + 3 * iqr)]
#print(data)
    
def f(n):
    x = data.groupby('类别')[str(n)].mean()
    data1 = pd.DataFrame({'类别':x.index,str(n) + '_m':x.values})
    data1[str(n) + '_nor'] = (data1[str(n) + '_m'] - data1[str(n) + '_m'].min()) / (data1[str(n) + '_m'].max() - data1[str(n) + '_m'].min())
    return data1 
y = f('口味')
z = f('人均消费')
data['消费性价比'] = (data['口味'] + data['环境'] + data['服务']) / data['人均消费']
w  = f('消费性价比')
#print(z.head())
data_re = pd.merge(pd.merge(y,z,on = '类别'),w,on = '类别')
data_re = data_re.sort_values(by = ['消费性价比_nor'],ascending= False)
data_re.reset_index(inplace= True,drop = True)
print(data_re.head())

'''绘制不同菜系消费性价比散点图'''
#设置调色盘
from bokeh.palettes import brewer
import bokeh.palettes as bp
colormap1 = {}
for m,n in zip(data_re['类别'].tolist()[:8],bp.OrRd[8]):
    colormap1[m] = n
colormap2 = colormap1
for m,n in zip(data_re['类别'].tolist()[8:19],bp.PRGn[11]):
    colormap2[m] = n
colormap3 = colormap2
for m,n in zip(data_re['类别'].tolist()[19:28],bp.BuPu[9]):
    colormap3[m] = n
#print(colormap3)
data_re['color1'] = [colormap3[x] for x in data_re['类别'].tolist()]
data_re.columns = ['typ','kw_m','kw_nor','xf_m','xf_nor','xjb_m','xjb_nor','color1']
print(data_re.head())

def f_source():
    col = data_re.columns
    data_source1 = {}#kw_nor作为散点图大小
    data_source2 = {}#kw_nor不作为散点图大小
    for i,j in zip(col,col):
        if i == 'kw_nor':#kw_nor 作为散点大小 要乘以40
            data_source1[i] = (data_re[i] *40).tolist()
        else:
            data_source1[i] = data_re[i].tolist()
        data_source2[j] = data_re[j].tolist()
    return data_source1,data_source2
f_source()#字典
kw_nor  = (data_re['kw_nor'] * 40).tolist()
source = ColumnDataSource(data =f_source()[0])
p1 = figure(plot_width = 800,plot_height = 200,title = '不同菜系消费性价比对比')
p1.circle(x = 'xf_m',y = 'xjb_nor',source = source,fill_color = 'color1',
        line_color = 'black',size = 'kw_nor',line_dash = [6,4],
       line_width = 2,fill_alpha = 0.8)
#show(p1)
#绘制口味分柱状图
source = ColumnDataSource(data = f_source()[1])
p2 = figure(plot_width = 800,plot_height = 200,
            x_range = f_source()[1]['typ'],y_range = [0,1.2],title = '不同菜系口味得分')
p2.vbar(x ='typ',top = 'kw_nor',source = source,width = 0.5,color = '#D94F56' )
#show(p2)
#绘制人均消费得分柱状图
source = ColumnDataSource(data = f_source()[1])
p3 = figure(plot_width = 800,plot_height = 200,
            x_range = f_source()[1]['typ'],y_range = [0,1.2],title = '人均消费得分')
p3.vbar(x ='typ',top = 'xf_nor',source = source,width = 0.5,color = '#DAB8C1' )
#show(p3)
from bokeh.layouts import gridplot
p = gridplot([[p1,p2,p3]],toolbar_location = 'above',returns = 'column')
show(p)