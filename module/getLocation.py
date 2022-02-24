import requests

def location_search(add):
    # 사용 api Geocoder API 2.0 https://www.vworld.kr/dev/v4dv_geocoderguide2_s001.do
    service_key = 'D0D83243-3ED3-327C-A5DF-6BBF0F7C7B70'
    url = f'http://api.vworld.kr/req/address?service=address&request=getCoord&key={service_key}&type=ROAD&'
    # add = '한적 2길 51-14'
    search = f'address={add}'

    resp = requests.get(url + search)
    location = resp.json()['response']['result']['point']
    print(location)

    result = dict()
    result['lat'] = location['y']
    result['lon'] = location['x']

    result_list = list()
    result_list.append(result)

    result_json = dict()
    result_json['location'] = result_list
    return result_json

if __name__ == '__main__':
    add = '충청남도 공주시 신관동 번영1로 97-13'
    loca = location_search(add)
    print(loca)