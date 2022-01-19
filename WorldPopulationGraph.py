import json
import pandas as pd
import seaborn as sns
from matplotlib import pyplot
import numpy as np
# 以下注释部分为计算8个block人口的可视化程序,将结果保存为图片
# i = 1
# fileprename = 'block'
# robust = True
# while i <= 8:
#     filepath = fileprename + str(i) + '.data'
#     filename = fileprename + str(i) + '.png'
#     data = np.array(json.load(open(filepath))['res'])
#     population = sum(data[:, 2])
#     name = ['lon', 'lat', 'population']
#     df = pd.DataFrame(columns=name, data=data)
#     df = df.pivot('lat', 'lon', 'population')
#     f, ax = pyplot.subplots(figsize=(10, 10))
#    # Manually set cmap parameters to modify color matching, refer to:https://seaborn.pydata.org/generated/seaborn.diverging_palette.html#seaborn.diverging_palette
#     cmap = sns.color_palette("Reds", 1000)
#     if(i == 5):
#         robust = False
#     else:
#         robust = True
#     sns.heatmap(df, fmt='.2', robust=robust, ax=ax, xticklabels=False,
#                 yticklabels=False, cmap=cmap, cbar=True, square=True, cbar_kws={"orientation": "horizontal"}).invert_yaxis()
#     population = int(population)
#     population = str(population)
#     pyplot.title(fileprename + str(i) + " Population = " + population)
#     pyplot.savefig(filename, dpi=2000)
#     i += 1


# 下面为计算世界人口可视化的程序
data = np.array(json.load(open('8_block_data.data'))['res'])
population = sum(data[:, 2])
name = ['lon', 'lat', 'population']
df = pd.DataFrame(columns=name, data=data)
df = df.pivot('lat', 'lon', 'population')
f, ax = pyplot.subplots(figsize=(10, 10))
# Manually set cmap parameters to modify color matching, refer to:https://seaborn.pydata.org/generated/seaborn.diverging_palette.html#seaborn.diverging_palette
cmap = sns.color_palette("Reds", 1000)
sns.heatmap(df, fmt='.2', robust=True, ax=ax, xticklabels=False,
            yticklabels=False, cmap=cmap, cbar=True, square=True, cbar_kws={"orientation": "horizontal"}).invert_yaxis()
population = int(population)
population = str(population)
pyplot.title('World Population Density Map' +
             "(World Population≈" + population+")")
pyplot.savefig('World Population Density Map' + '.png', dpi=2000)
pyplot.show()
