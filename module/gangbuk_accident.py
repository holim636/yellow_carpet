import numpy as np
import pandas as pd
import json
import matplotlib.pyplot as plt


def GanbukAccident():
    data = pd.read_csv('../yellow/res/data/도로교통공단_어린이 교통사고 현황_20191231.csv', encoding="cp949")
    df = pd.DataFrame(data)

    df1 = df[['발생일', '사망자수', '중상자수', '경상자수', '부상신고자수', '발생지_시도', '발생지_시군구', '피해자_당사자종별']]
    df2 = df1.loc[df['피해자_당사자종별'] == '보행자']
    df3 = df2.loc[df['발생지_시도'] == '서울']

    guname = ['은평구', '서대문구', '마포구', '동대문구', '성동구', '중랑구', '광진구', '강북구', '도봉구']
    years = ['2015', '2016', '2017', '2018', '2019']

    gangbukAccident = dict()
    guDict = dict()


    # 해당하는 구 가져와 반복
    for gu in guname:
        df_gu = df3.loc[df['발생지_시군구'] == gu]
        df_gu = df_gu.set_index(['발생일'])
        yearDict = dict()

        # 연월일 자료 -> 연도 자료
        for year in years:
            df_gu_year = df_gu.loc[f'{year}-01-01':f'{year}-12-31']
            yearDict[year] = len(df_gu_year.index)

        guDict[gu] = yearDict

    gangbukAccident['강북'] = guDict

    return gangbukAccident

gangbuk = GanbukAccident()
print(gangbuk)

# make_json = json.dumps(gangbuk, ensure_ascii=False)
# with open('gangbuk_accident.json', 'w', encoding='utf_8') as f:
#     f.write(make_json)

# 시각화하는 함수 1. 강북구 전체 사고율 bar 그래프로 나타내기
def accident_bar():
    # 만약 인수에 은평구를 넣는다면, 은평구 연도별 사고율이 나오게 하자.
    guList = ['은평구', '서대문구', '마포구', '동대문구', '성동구', '중랑구', '광진구', '강북구', '도봉구']
    gangbuk_gu = gangbuk['강북']
    years = ['2015','2016','2017','2018','2019']
    total_accident = list()

    for year in years:
        acc_sum = 0
        for gu in guList:
            acc_sum += gangbuk_gu[gu][year]

        total_accident.append(acc_sum)

    print(total_accident)

    # x축 만들기
    fig = plt.figure()
    ax = fig.subplots()
    x = np.arange(5)
    ax.bar(x, total_accident, color='#ffd400', width=0.6) # 사고횟수
    # ax.set_title('서울 강북지역 연도별 사고현황') 한글 깨짐, 필요하다면 한글 사용되도록 추가하기
    plt.xticks(x, years, color='orange') # 연도별
    plt.yticks(color='orange')
    ax.set_facecolor('black')
    fig.patch.set_facecolor('xkcd:black')
    # plt.grid(True)
    plt.show()


# 시각화 함수 2. 구별 교통사고 발생 횟수 선 그래프로 나타내기
def gu_line(guname):
    # 만약 인수에 은평구를 넣는다면, 은평구 연도별 사고율이 나오게 하자.
    gangbuk_gu = gangbuk['강북']
    years = ['2015', '2016', '2017', '2018', '2019']
    gu_accident = list()

    for year in years:
        gu_accident.append(gangbuk_gu[guname][year])
    print(gu_accident)

    # 그래프로 나타내기
    fig = plt.figure()
    ax = fig.subplots()
    ax.plot(years, gu_accident, color='#ffd400', marker='o')
    ax.set_facecolor('black')
    fig.patch.set_facecolor('xkcd:black')
    plt.yticks(list(range(0, 101, 10)), color='orange')
    plt.xticks(color='orange')
    # plt.grid(True)


    plt.show()

if __name__ == '__main__':
    accident_bar()
    gu_line('광진구') # 구 이름을 넣어주세요! '은평구', '서대문구', '마포구', '동대문구', '성동구', '중랑구', '광진구', '강북구', '도봉구'