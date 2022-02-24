import csv
import copy
import requests
import json
##### 옐로카펫 데이터 만들기 위한 소스입니다 이후 프로젝트에서 더이상 사용되지 않습니다.####
class schoolLoc:
    def __init__(self):
        self.schoolDict = dict()
        f = open('../yellow/res/data/seoul_elementary.csv', 'r', encoding='cp949')
        readCsv = csv.reader(f)
        for line in readCsv:
            self.schoolDict[line[3]]=line[7]
        f.close()

    ## 함수 선언부
    def find(self, schoolName):
        if self.schoolDict.get(schoolName):
            return self.schoolDict[schoolName]
        else:
            return ('없음')

def location_search(add):
    # 사용 api Geocoder API 2.0 https://www.vworld.kr/dev/v4dv_geocoderguide2_s001.do
    service_key = 'D0D83243-3ED3-327C-A5DF-6BBF0F7C7B70'
    url = f'http://api.vworld.kr/req/address?service=address&request=getCoord&key={service_key}&type=ROAD&'
    # add = '한적 2길 51-14'
    search = f'address={add}'

    resp = requests.get(url + search)
    location = resp.json()['response']['result']['point']
    #print(location)

    result = dict()
    result['lat'] = location['y']
    result['lon'] = location['x']

    result_list = list()
    result_list.append(result)

    result_json = dict()
    result_json['location'] = result_list
    return result_json


def make_list():
    addr = 'https://www.juso.go.kr/addrlink/addrCoordApiJsonp.do'
    dataPath = 'res/data/서울특별시_'  # 데이터 경로
    gulist = ['강남구', '강북구', '관악구', '동작마포서대문영등포', '송파광진성동', '양천구_구로구_금천구', '1']
    filetype = '.csv'  # 파일 형식
    school_num = [2, 1, 0, 1, 1, 1, 1]
    date = [4, 4, 2, 2, 2, 2, 2]
    data = dict()
    data_list = []
    data_date = []
    buf = []
    result = []
    for i , gu in enumerate(gulist):# enumrate로 몇번째 행인지와 구 각각 불러오기

        file_name = dataPath + gu + filetype # 위에서 지정한 경로와 구 명, 파일형식합쳐서 파일위치 만들기
        with open(file_name, "r",encoding="cp949") as f:#파일열어서

            data = csv.reader(f)# csv리더로 csv 객체 생성
            for line in data:#csv객체 각 줄 불러서
                if(line[school_num[i]].find("초등학교")!=-1):
                    #print(line[school_num[i]]+','+line[date[i]])
                    data_list.append(line[school_num[i]])
                    data_date.append(line[date[i]])
    data_list, data_date
    juso = schoolLoc()

    for i, j in enumerate(data_list):
        buf.append(j)
        buf.append(data_date[i])
        buf.append(juso.find(j))
        buf.append(location_search(juso.find(j))['location'][0]['lat'])
        buf.append(location_search(juso.find(j))['location'][0]['lon'])
        result.append(copy.deepcopy(buf))
        buf.clear()
    return result

school = make_list()


title = ['school','date','juso','lat','lon']
file_path = "../yellow/res/data/yellow.json"

data = {}
data['yellow'] = []
for i in school:
    data['yellow'].append({
        title[0]:i[0],
        title[1]: i[1],
        title[2]: i[2],
        title[3]: i[3],
        title[4]: i[4],
    })
with open(file_path, 'w') as outfile:
    json.dump(data, outfile)

