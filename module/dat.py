import json
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib as mpl
import matplotlib.font_manager as fm
import csv
import os

font_path = "../yellow/res/font/NanumGothic.ttf"
PATH = "../yellow/res/data/"
dat1 = '도로교통공단_어린이 교통사고 현황_20191231.csv'
dat2 = '도로교통공단_어린이 사망교통사고 정보_20191231.csv'
dat3 = 'yellow.json'
mpl.rcParams['font.family'] = 'NanumGothic'
mpl.rcParams['font.size'] = 10

def load_data(path=PATH, name =''):
    csv_path = os.path.join(path, name)
    return pd.read_csv(csv_path,engine='python',encoding='cp949')
def load_data_json(path=PATH, name = ''):
    json_path = os.path.join(path,name)
    data = dict()
    with open(json_path, 'r') as jsonfile:
        data = json.load(jsonfile)
    return pd.DataFrame(data['yellow'])


def corr_data(): #상관계수 출력
    b = load_data(name=dat1)
    c = load_data_json(name=dat3)
    new_b = b[b['발생지_시도'] == '서울']
    new_b = new_b[new_b['사고유형_대분류'] == '차대사람']
    new_b = new_b.loc[:,['발생일','사망자수','중상자수','경상자수','부상신고자수']]
    new_b['발생일'] = pd.to_datetime(new_b['발생일'])
    new_b['발생일'] = new_b['발생일'].dt.year
    new_b['총사상자'] = new_b['사망자수'] + new_b['중상자수'] + new_b['경상자수'] + new_b['부상신고자수']
    group = new_b.groupby(new_b['발생일'])
    d1 = group.sum()
    c = c.loc[:,['date']]
    c['date'] = pd.to_datetime(c['date'])
    c['date'] = c['date'].dt.year
    c['date'] = pd.to_numeric(c['date'])
    c = c[c['date'] <= 2019]
    d2 = c['date'].value_counts()
    d2 = d2.loc[[2015,2016,2017,2018,2019]]
    d2 = d2.cumsum()
    data = pd.concat([d1,d2],axis=1)
    corr_matirix = data.corr()
    print(corr_matirix['date'].sort_values(ascending=False))


def corr_data_second(name = ''): #상관계수 출력
    b = load_data(name=dat1)
    c = load_data_json(name=dat3)
    new_b = b[b['발생지_시도'] == '서울']

    if name != '':
        new_b = new_b[new_b['발생지_시군구'] == name]############################
        c = c[c['juso'].str.contains(name)]

    new_b = new_b[new_b['사고유형_대분류'] == '차대사람']
    new_b = new_b.loc[:,['발생일','사망자수','중상자수','경상자수','부상신고자수']]
    new_b['발생일'] = pd.to_datetime(new_b['발생일'])
    new_b['발생일'] = new_b['발생일'].dt.year
    new_b['총사상자'] = new_b['사망자수'] + new_b['중상자수'] + new_b['경상자수'] + new_b['부상신고자수']
    group = new_b.groupby(new_b['발생일'])
    d1 = group.sum()
    c = c.loc[:,['date']]
    c['date'] = pd.to_datetime(c['date'])
    c['date'] = c['date'].dt.year
    c['date'] = pd.to_numeric(c['date'])
    c = c[c['date'] <= 2019]
    d2 = c['date'].value_counts()
    #d2 = d2.loc[[2015,2016,2017,2018,2019]]
    #d2 = d2.cumsum()
    data = pd.concat([d1,d2],axis=1)
    data = data.fillna(0)
    corr_matirix = data.corr()
    print(corr_matirix['date'].sort_values(ascending=False))

def plot_data(name = '',year = '',type=1):#지역 현황 그래프
    #a = load_data(name= dat1)
    b = load_data(name= dat2)
    c = load_data_json(name=dat3)
    new_b = b[b['발생지시도']=='서울']
    new_b = new_b[new_b['사고유형_대분류']=='차대사람']
    if name != '':
        new_b = new_b[new_b['발생지시군구']==name]
        c = c[c['juso'].str.contains(name)]
    if year != '':
        new_b = new_b[new_b['발생년']==year]
        c['date'] = pd.to_datetime(c['date'])
        c['year'] = c['date'].dt.year
        c = c[c['year']<=year]
    c['lat'] = pd.to_numeric(c['lat'])
    c['lon'] = pd.to_numeric(c['lon'])
    plt.figure()
    plt.scatter(new_b['경도'],new_b['위도'],color='red',alpha=.1)
    plt.scatter(c['lon'],c['lat'],color='yellow')
    plt.xlabel('경도')
    plt.ylabel('위도')
    plt.show()

def ac_plot_data(name = '',type = 1): #사고 통계 그래프
    if type == 0:
        b = load_data(name= dat1)
        new_b = b[b['발생지_시도'] == '서울']
        new_b = new_b[new_b['사고유형_대분류'] == '차대사람']
        if name != '':
            new_b = new_b[b['발생지_시군구'] == name]
        new_b['발생일'] = pd.to_datetime(new_b['발생일'])
        new_b['발생년'] = new_b['발생일'].dt.year
        new_b['발생년'] = pd.to_numeric(new_b['발생년'])
        p = new_b['발생년'].value_counts()
    else:
        b = load_data(name= dat2)
        new_b = b[b['발생지시도']=='서울']
        new_b = new_b[new_b['사고유형_대분류']=='차대사람']
        if name != '':
            new_b = new_b[b['발생지시군구'] == name]
        new_b['발생년'] = pd.to_numeric(new_b['발생년'])
        p = new_b['발생년'].value_counts()
    order = [2015,2016,2017,2018,2019]
    p = p.loc[order]
    p.plot.bar()
    plt.xlabel('year')
    plt.ylabel('')
    plt.show()

def detail_plot_data(name = '',type = 1): #연도별 사상자 수 그래프
    if type == 0:
        b = load_data(name=dat1)
        # b = load_data(name= dat2)
        new_b = b[b['발생지_시도'] == '서울']
        new_b = new_b[new_b['사고유형_대분류'] == '차대사람']
        if name != '':
            new_b = new_b[b['발생지_시군구'] == name]
        new_b['발생일'] = pd.to_datetime(new_b['발생일'])
        new_b['발생년'] = new_b['발생일'].dt.year
        new_b['발생년'] = pd.to_numeric(new_b['발생년'])
        new_b['사망자수'] = pd.to_numeric(new_b['사망자수'])
        # new_b['부상자수'] = pd.to_numeric(new_b['부상자수'])
        new_b['중상자수'] = pd.to_numeric(new_b['중상자수'])
        new_b['경상자수'] = pd.to_numeric(new_b['경상자수'])
        new_b['부상신고자수'] = pd.to_numeric(new_b['부상신고자수'])
        p = new_b.groupby('발생년').sum()
        p = p.loc[:, ['사망자수', '중상자수', '경상자수', '부상신고자수']]
    #a = load_data(name= dat1)
    else :
        b = load_data(name= dat2)
        new_b = b[b['발생지시도']=='서울']
        new_b = new_b[new_b['사고유형_대분류']=='차대사람']
        if name != '':
            new_b = new_b[b['발생지시군구'] == name]
        new_b['발생년'] = pd.to_numeric(new_b['발생년'])
        new_b['사망자수'] = pd.to_numeric(new_b['사망자수'])
        new_b['부상자수'] = pd.to_numeric(new_b['부상자수'])
        new_b['중상자수'] = pd.to_numeric(new_b['중상자수'])
        new_b['경상자수'] = pd.to_numeric(new_b['경상자수'])
        new_b['부상신고자수'] = pd.to_numeric(new_b['부상신고자수'])
        p = new_b.groupby('발생년').sum()
        p = p.loc[:,['사망자수','부상자수','중상자수','경상자수','부상신고자수']]
    order = [2015,2016,2017,2018,2019]
    p = p.loc[order]
    p.plot.bar()
    plt.xlabel('year')
    plt.ylabel('')
    plt.show()


def accident_data(): #교통사고 분석
    a = load_data(name= dat1)
    #b = load_data(name= dat2)
    new_a = a[a['발생지_시도']=='서울']
    new_a = new_a[new_a['사고유형_대분류']=='차대사람']
    new_a = new_a[new_a['피해자_당사자종별'] == '보행자']### 이런 형식으로 항목을 줄입니다
    pie = new_a['도로형태'].value_counts()### 여기서 분석할 항목 정합니다
    pie.plot.pie()
    plt.xlabel('서울시 보행자 차량 사고 유형')
    plt.ylabel('')
    plt.show()

#개노가다 시작
def distance(x, y, x1, y1):
    newx = abs((x - x1) * 10000)
    newy = abs((y - y1) * 10000)
    return pow(newx, 2) + pow(newy, 2)
def make_list():

def short_cut(x, y):
    #y는 리스트로 넘기는고
    #x는 하나의 점

    #같은 구역에 있는것만 확인을 원함

def make_short_list(name=''):




#여기서 구 이름만 입력해주면 됩니다

#plot_data(name='',year='')
#연도별 설치 완료된 옐로카펫 위치와 연도별 사고 현황을 시각화
#ac_plot_data(name = '강남구',type= 0)
#연도별 사고건수 출력 type1은 사망사고(B데이터), 0은 모든사고(A데이터)
#detail_plot_data(name = '',type=0)
#연도별 사고 현황 출력 type1은 사망사고(B데이터) 0은 모든 사고(A데이터)
accident_data()
#corr_data_second(name = '강남구')