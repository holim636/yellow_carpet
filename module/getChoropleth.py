import folium
import pandas as pd
import numpy as np


geo_json = 'https://raw.githubusercontent.com/southkorea/seoul-maps/master/kostat/2013/json/seoul_municipalities_geo_simple.json'

location = '../yellow_carpet/res/data/'
saveLoc = '../static/img/yellowcarpet/'
seoul = '서울특별시_'
filesList = ['11', '동작마포서대문영등포', '송파광진성동', '양천구_구로구_금천구']
dates = range(2015, 2020)
maxYC = 20

def getYearlyYC(intYear):
    guDict = dict()
    persentGu = dict()

    for i in range(len(filesList)):
        data = pd.read_csv(location+seoul+filesList[i]+'.csv', encoding="cp949")

        data['설치일'] = pd.to_datetime(data['설치일'],format='%Y-%m-%d')

        # ['도봉구', '중랑구', '동대문구', '은평구', '강남구', '강북구', '관악구']
        for gu in data['구'].unique():
            df1 = data[data['구'] == gu]

            yearDict = dict()
            persentYear = dict()
            for i in range(len(dates)):
                df2 = df1[df1['설치일'].dt.year == dates[i]]
                if i != 0:
                    yearDict[dates[i]] = yearDict[dates[i-1]] + len(df2)
                else:
                    yearDict[dates[i]] = len(df2)

                persentYear[dates[i]] = yearDict[dates[i]] / maxYC
            guDict[gu] = yearDict
            persentGu[gu] = persentYear

    raw_dict = dict()

    for year in persentGu['강남구'].keys():
        raw_list = list()
        for gu in persentGu.keys():
            gu_data = list()
            gu_data.append(gu)
            gu_data.append(persentGu[gu][year])
            raw_list.append(gu_data)

        raw_dict[year] = raw_list

    data = pd.DataFrame(raw_dict[intYear], columns=['name', 'value'])

    m = folium.Map(location=[37.55778596297204, 126.98987185407555], tiles='Stamentoner',
                   zoom_start=11)

    # a = np.array([0.05, 0.1, 0.15, 0.2, 0.25, 0.3, 0.35, 0.4, 0.45, 0.5, 0.55, 0.6, 0.65, 0.7, 0.75, 0.8 ])

    # bins = list(data['value'].quantile([0 , 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8]))

    # linear = folium.LinearColormap(['red', 'orange'], vmin=0., vmax=0.1)
    folium.Choropleth(geo_data=geo_json,
                      data=data,
                      columns=['name', 'value'],
                      key_on='feature.properties.name',
                      fill_color='YlGn',
                      nan_fill_color='white',
                      fill_opacity=1,
                      line_opacity=1,
                      bins=8).add_to(m)

    m.save(f'{saveLoc}{intYear}yellow.html')

if __name__ == '__main__':
    # for date in dates:
        getYearlyYC(2019)