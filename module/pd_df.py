import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import json
from matplotlib import font_manager, rc


# 한글 폰트 사용할 수 있도록
font_path = './D2Coding.ttc'
font = font_manager.FontProperties(fname=font_path).get_name()
rc('font', family=font)

jsonData1 = 'seoul_Casualty.json'           # csvData1로 만든 json 파일
jsonData2 = 'seoul_dead.json'               # csvData2로 만든 json 파일
csvData1 = '도로교통공단_어린이 교통사고 현황_20191231.csv'
csvData2 = '도로교통공단_어린이 사망교통사고 정보_20191231.csv'
csvLoc = '../yellow/res/data/'
staticLoc = '../static/img/'


def getCasualties(loc):
    data = pd.read_csv(csvLoc+loc, encoding="cp949")
    df = pd.DataFrame(data)

    # 표시할 df head
    # 사용할 csv파일이 1인지 2인지에따라 head가 다름으로 구분해 준다.
    if loc == csvData1:
        csvHead = ['발생일', '사망자수', '중상자수', '경상자수', '부상신고자수', '발생지_시도', '발생지_시군구', '피해자_당사자종별']
    elif loc == csvData2:
        csvHead = ['발생년월일시', '사망자수', '중상자수', '경상자수', '부상신고자수', '발생지시도', '발생지시군구', '피해자_당사자종별']
    else:
        print('형식에 맞는 csv파일인지 확인하세요')
        return
    df1 = df[csvHead]
    df2 = df1.loc[df[csvHead[7]] == '보행자']             # 피해자_당사자종별 중 보행자만
    df3 = df2.loc[df[csvHead[5]] == '서울']               # 발생지_시도 중 서울만

    # 강남의 ~~구들
    guList = ['양천구', '구로구', '영등포구', '금천구', '동작구', '관악구', '강남구', '송파구', '은평구', '서대문구', '마포구', '동대문구', '성동구', '중랑구',
              '광진구', '강북구', '도봉구']
    dates = ['2015', '2016', '2017', '2018', '2019']      # 연도별 데이터터

    gangnam_casualties = dict()
    guDict = dict()

    for gu in guList:
        df_1 = df3.loc[df[csvHead[6]] == gu]              # 시군구가 gu인 df
        df_1 = df_1.set_index([csvHead[0]])               # 발생일을 index로
        yearDict = dict()

        for date in dates:        # date가 2015라면 2015-01-01부터 2015-12-31까지의 df를 가지고 옴
            df_1_1 = df_1.loc[f'{date}-01-01':f'{date}-12-31']
            numDict = dict()
            numDict['사망자수'] = int(df_1_1['사망자수'].sum())
            numDict['중상자수'] = int(df_1_1['중상자수'].sum())
            numDict['경상자수'] = int(df_1_1['경상자수'].sum())
            numDict['부상신고자수'] = int(df_1_1['부상신고자수'].sum())
            yearDict[date] = numDict

        guDict[gu] = yearDict

    gangnam_casualties['서울'] = guDict
    total_stores_json = json.dumps(gangnam_casualties, ensure_ascii=False)
    with open(csvLoc+jsonData2, 'w', encoding='utf_8') as f:
        f.write(total_stores_json)

    return gangnam_casualties

# 바 그래프 그리기
def barGraph():
    with open(csvLoc+jsonData1, 'r', encoding='utf_8') as f:
        casualty = json.load(f)

    with open(csvLoc+jsonData2, 'r', encoding='utf_8') as f:
        dead = json.load(f)

    gugun1 = casualty['서울']
    gugun2 = dead['서울']

    # 서울의 각 구들
    guList = ['양천구', '구로구', '영등포구', '금천구', '동작구', '관악구', '강남구',
              '송파구', '은평구', '서대문구', '마포구', '동대문구', '성동구', '중랑구',
              '광진구', '강북구', '도봉구']
    yearList = ['2015', '2016', '2017', '2018', '2019']
    accident1 = list()
    accident2 = list()
    persent = list()

    # 강남의 각 연도별 사상자/사망자 합계
    for year in yearList:
        sum1 = 0
        sum2 = 0
        for gu in guList:
            sum1 = sum1 + gugun2[gu][year]['사망자수'] + gugun1[gu][year]['중상자수'] + gugun1[gu][year]['경상자수'] + gugun1[gu][year]['부상신고자수']
            sum2 = sum2 + gugun2[gu][year]['사망자수']

        accident1.append(sum1)
        accident2.append(sum2)
        a = round(float(sum2/sum1)*100, 2)
        persent.append(a)

    fig = plt.figure()
    ax = fig.subplots()
    x = np.arange(5)

    # 바생성
    ax.bar(x, accident2, color='#ff7b5a', width=0.45, zorder=3, label='사망자')
    ax.bar(x, accident1, color='#ffd400', width=0.45, zorder=3, label='사상자', bottom=accident2)
    ax.set_title('서울 연도별 사고현황')                 # 그래프 제목
    plt.xticks(x, yearList)                          # x축을 각각의 연도로
    plt.legend(loc='upper right')                     # 범례를 좌상단으로
    plt.grid(True, zorder=0, axis='y')               # 그래프 격자 y축만 표시되게

    plt.savefig(f'{staticLoc}seoul_total.png')       # 그래프 png파일로 저장
    plt.clf()

    # plt.show()

def plotGraph(gu):
    with open(jsonData1, 'r', encoding='utf_8') as f:
        casualty = json.load(f)

    with open(jsonData2, 'r', encoding='utf_8') as f:
        dead = json.load(f)

    gugun1 = casualty['서울']
    gugun2 = dead['서울']
    yearList = ['2015', '2016', '2017', '2018', '2019']
    accident1 = list()
    accident2 = list()
    persent = list()

    # 선택한 구의 연도별 사상자/사망자 수를 accident1, 2라는 list에 저장
    # persent는 사망자/사상자의 비율[%]
    for year in yearList:
        sum = gugun2[gu][year]['사망자수'] + gugun1[gu][year]['중상자수'] + gugun1[gu][year]['경상자수'] + gugun1[gu][year]['부상신고자수']
        accident1.append(sum)
        accident2.append(gugun2[gu][year]['사망자수'])
        a = round(float(gugun2[gu][year]['사망자수']/sum)*100, 2)
        persent.append(a)

    # print(accident1, accident2, persent)
    # 그래프 틀(? 프레임?)색 회색으로 설정
    with plt.rc_context({'axes.edgecolor':'lightgray'}):
        fig, ax = plt.subplots()
        # 노랑 사상자 빨강 사망자 파랑 사망률
        ax.plot(yearList, accident1, color='#ffd400', marker='o', label='사상자')
        ax.plot(yearList, accident2, color='#ff7b5a', marker='o', label='사망자')
        ax.plot(yearList, persent, color='#1e90ff', marker='v', label='사망률[%]')
        plt.grid(axis='y')                      # 격자 y축만 표시되도록
        plt.yticks(list(range(0, 91, 10)))      # y축 범위 0~90까지 10씩 증가하도록
        plt.legend(loc=1)                       # 범례위치 upper right
        plt.title(gu)                           # 그래프 제목을 각각의 구 이름으로

    # plt 파일로 저장
    plt.savefig(f'{staticLoc}{gu}.png')
    plt.clf()                       # plt 초기화


if __name__ == '__main__':
    # getCasualties(csvData2)
    # plotGraph('양천구')
    barGraph()
    # # getCasualties(data2)
    #
    # guList = ['양천구', '구로구', '영등포구', '금천구', '동작구', '관악구', '강남구',
    #           '송파구', '은평구', '서대문구', '마포구', '동대문구', '성동구', '중랑구',
    #           '광진구', '강북구', '도봉구']
    #
    # for gu in guList:
    #     plotGraph(gu)
