import aiohttp
import asyncio
import json
import pandas as pd
import seaborn as sns
from matplotlib import pyplot
import numpy as np
# from bokeh.core.property.dataspec import ColorSpec
# from typing_extensions import ParamSpec
# from bokeh.plotting import figure, output_file, show
# import folium
# from folium.plugins import HeatMap
# import webbrowser
# from numpy.lib.function_base import average, place


# data1
# px-10 0 70 80 70 0
# py35 70 70 35 0 0
# 6

# data2 China
# px 73 135 135 73
# py 53 53 3 3

# data3 (Australia)
# px 110 160 160 110
# -15 -15 -40 -40

# data block1
# px -180 -90 -90 -180
# py 90 90 0 0

# data block2
# px -90 0 0 -90
# py 90 90 0 0

# data block3
# px 0 90 90 0
# py 90 90 0 0

# data block4
# px 90 180 180 90
# py 90 90 0 0

# data block5
# px -180 -90 -90 -180
# py 0 0 -90 -90

# data block6
# px -90 0 0 -90
# py 0 0 -90 -90

# data block7
# px 0 90 90 0
# py 0 0 -90 -90

# data block8
# px 90 180 180 90
# py 0 0 -90 -90


async def main():
    async with aiohttp.ClientSession() as session:
        params = {'edge': '4', 'pointx': '110 160 160 110',
                  'pointy': '-15 -15 -40 -40'}
        # port = 8080
        async with session.get('http://localhost:8080/population', params=params) as response:
            JsonData = await response.text()
            # write = open('block1.data', 'w')
            # write.write(JsonData)
            js = json.loads(JsonData)
            # data is illegal
            if 'ERROR' in js['res']:
                print("There're Something Error:")
                print(js['res'])
            else:
                data = np.array(js['res'])
                population = sum(data[:, 2])
                name = ['lon', 'lat', 'population']
                df = pd.DataFrame(columns=name, data=data)
                df = df.pivot('lat', 'lon', 'population')
                # figsize = 20 * 10
                f, ax = pyplot.subplots(figsize=(10, 10))
                # Manually set cmap parameters to modify color matching, refer to:https://seaborn.pydata.org/generated/seaborn.diverging_palette.html#seaborn.diverging_palette
                cmap = sns.color_palette("Reds", 1000)
                sns.heatmap(df, fmt='.2', robust=True, ax=ax, xticklabels=False,
                            yticklabels=False, cmap=cmap, cbar=True, square=True, cbar_kws={"orientation": "horizontal"}).invert_yaxis()
                # set graph title
                title = 'Population='
                population = int(population)
                population = str(population)
                title = title + population
                pyplot.title(title)
                # set x y lables
                pyplot.ylabel('latitude')
                pyplot.xlabel('longitude')
                # Generate an graph with the corresponding name, dpi = 2000
                pyplot.savefig('Australia' + '.png', dpi=2000)
                pyplot.show()
loop = asyncio.get_event_loop()
loop.run_until_complete(main())
