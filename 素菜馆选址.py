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
#经 data['口味'].boxplot()观察 口味 环境 服务大于上峰位的异常值 
#并不是很多 所以可直接 对人均消费进行异常值处理  
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
    data_source = {}#kw_nor作为散点图大小 
    for i in col:
        if i == 'kw_nor':#kw_nor 作为散点大小 要乘以40
            data_re['size'] = data_re[i] *40
            data_source[i] = data_re[i].tolist()
        else:
            data_source[i] = data_re[i].tolist()
    data_source['size'] = data_re['size'].tolist()   
    return data_source
f_source()#字典
source = ColumnDataSource(data = f_source())
from bokeh.models import HoverTool#做图表联动
hover = HoverTool(tooltips = [('餐饮类型','@typ'),
                              ('人均消费','@xf_m'),
                              ('性价比得分','@xjb_nor'),
                              ('口味得分','@kw_nor') 
                                ])
from bokeh.models.annotations import BoxAnnotation
kw_nor  = (data_re['kw_nor'] * 40).tolist()

p1 = figure(plot_width = 800,plot_height = 200,title = '不同菜系消费性价比对比',
           tools=[hover,'box_select,reset,xwheel_zoom,pan,crosshair'],
           x_axis_label = '人均消费',y_axis_label = '性价比得分'
           )
p1.circle(x = 'xf_m',y = 'xjb_nor',source = source,fill_color = 'color1',
        line_color = 'black',size = 'size',line_dash = [6,4],
       line_width = 2,fill_alpha = 0.8)
xf_qj = BoxAnnotation(bottom = 0,top = 1.1,left = 40,right = 80,
                     fill_color = '#235789',fill_alpha = 0.1)# 平均消费区间
p1.add_layout(xf_qj)
#show(p1)
#绘制口味分柱状图
p2 = figure(plot_width = 800,plot_height = 200,x_range = f_source()['typ'],
            y_range = [0,1.2],title = '不同菜系口味得分',
           tools=[hover,'box_select,reset,xwheel_zoom,pan,crosshair'])
p2.vbar(x ='typ',top = 'kw_nor',source = source,width = 0.5,color = '#D94F56' )
#show(p2)
#绘制人均消费得分柱状图

p3 = figure(plot_width = 800,plot_height = 200,x_range = f_source()['typ'],
            y_range = [0,1.2],title = '人均消费得分',
            tools=[hover,'box_select,reset,xwheel_zoom,pan,crosshair'])
p3.vbar(x ='typ',top = 'xf_nor',source = source,width = 0.5,color = '#DAB8C1' )
#show(p3)
from bokeh.layouts import gridplot
p = gridplot([[p1],[p2],[p3]],toolbar_location = 'above')
show(p)

'''
素菜馆选址 散点图
'''
df = pd.read_excel('项目07代码\\result_point.xlsx',sheetname = 0)
df.fillna(0,inplace = True)
df.columns = ['rkmd','dlcd','cy_count','sc_count','lng','lat']
df['rkmd_nor'] = (df['rkmd'] - df['rkmd'].min()) / (df['rkmd'].max() - df['rkmd'].min())
df['dlmd_nor'] = (df['dlcd'].max() - df['dlcd']) /(df['dlcd'].max() - df['dlcd'].min())
df['cy_count_nor'] = (df['cy_count'] - df['cy_count'].min()) /(df['cy_count'].max() - df['cy_count'].min())
df['sc_count_nor'] = (df['sc_count'] - df['sc_count'].min()) / (df['sc_count'].max() - df['sc_count'].min())
df['final_result'] = df['rkmd_nor'] *0.4 + df['dlmd_nor'] *0.2 + df['cy_count_nor'] *0.3 + df['sc_count_nor']*0.1
df1 = df.sort_values(by= 'final_result',ascending = False).reset_index(drop = True)

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