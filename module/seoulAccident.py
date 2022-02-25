import numpy as np
import pandas as pd
import json
import matplotlib.pyplot as plt


def seoulAccident():
    data = pd.read_csv('C:/workspaces/multiProject1/data/도로교통공단_어린이 교통사고 현황_20191231.csv', encoding="cp949")
    df = pd.DataFrame(data)

    df1 = df[['발생일', '사망자수', '중상자수', '경상자수', '부상신고자수', '발생지_시도', '발생지_시군구', '피해자_당사자종별']]
    df2 = df1.loc[df['피해자_당사자종별'] == '보행자']
    df3 = df2.loc[df['발생지_시도'] == '서울']

    years = ['2015', '2016', '2017', '2018', '2019']
    types = ['사망자수', '중상자수', '경상자수', '부상신고자수']

    seoulDict = dict()

    yearDict = dict()
    for year in years:
        df_gu = df3.set_index(['발생일'])
        df_gu_year = df_gu.loc[f'{year}-01-01':f'{year}-12-31']

        sum_person = 0
        typeDict = dict()
        for type in types:
            sum_person = int(df_gu_year[type].sum())
            # print(sum_person)
            typeDict[type] = sum_person  # {'중상자수': ~~, '경상자수': ~~, '부상신고자수': ~~}

        yearDict[year] = typeDict   # {'2015': ~~}
    seoulDict['서울'] = yearDict    # {'서울': ~~}
    return seoulDict

seoul = seoulAccident()
print(seoul)

make_json = json.dumps(seoul, ensure_ascii=False)
with open('seoul_casualties.json', 'w', encoding='utf_8') as f:
    f.write(make_json)

# accident_bar()

# 서울시 사망자 데이터
def seoulDeath():
    data = pd.read_csv('C:/workspaces/multiProject1/data/도로교통공단_어린이 사망교통사고 정보_20191231.csv', encoding="cp949")
    df = pd.DataFrame(data)

    df1 = df[['발생년월일시', '사망자수', '부상자수', '중상자수', '경상자수', '부상신고자수', '발생지시도', '발생지시군구', '피해자_당사자종별']]
    df2 = df1.loc[df['피해자_당사자종별'] == '보행자'] # 보행자만
    df3 = df2.loc[df['발생지시도'] == '서울'] # 서울지역만

    years = ['2015', '2016', '2017', '2018', '2019']
    types = ['사망자수', '부상자수', '중상자수', '경상자수', '부상신고자수']

    seoulDict = dict()


    yearDict = dict()
    for year in years:
        df_gu = df3.set_index(['발생년월일시'])
        df_gu_year = df_gu.loc[f'{year}-01-01':f'{year}-12-31']

        typeDict = dict()
        sum_person = 0
        for type in types:
            sum_person = int(df_gu_year[type].sum())
            # print(sum_person)
            typeDict[type] = sum_person  # {'중상자수': ~~, '경상자수': ~~, '부상신고자수': ~~}

        yearDict[year] = typeDict  # {'2015': ~~}
    seoulDict['서울'] = yearDict  # {'서울': ~~}
    return seoulDict


seoul2 = seoulDeath()
print(seoul2)

make_json = json.dumps(seoul2, ensure_ascii=False)
with open('seoul_death.json', 'w', encoding='utf_8') as f:
    f.write(make_json)




# accident_bar()

# # 시각화하는 함수 만들기. 서울시 전체 사고율을 bar 그래프로 나타내보자.
# def accident_bar():
#     guList = ['은평구', '서대문구', '마포구', '동대문구', '성동구', '중랑구', '광진구', '강북구', '도봉구', '양천구', '구로구', '영등포구', '금천구', '동작구', '관악구', '강남구', '송파구']
#     seoul1 = seoul['서울']
#     years = ['2015', '2016', '2017', '2018', '2019']
#     total_accident = list()
#
#     # 연도별 사고 수를 다 합치자
#     for year in years:
#         acc_sum = 0
#         for gu in guList:
#             acc_sum += seoul1[gu][year]
#
#         total_accident.append(acc_sum)
#
#     print(total_accident)
#
#     # x축 만들기
#     fig = plt.figure()
#     ax = fig.subplots()
#     x = np.arange(5)
#     ax.bar(x, total_accident, width=0.6) # 사고횟수
#     # ax.set_title('서울시 연도별 사고현황(2015-2019)') 한글 깨짐, 필요하다면 한글 사용되도록 추가하기
#     plt.xticks(x, years) # 연도별
#     plt.show()
#
#
