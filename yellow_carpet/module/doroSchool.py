import csv
import sys

f = open('../yellow/res/data/seoul_elementary.csv', 'r', encoding='cp949')
readCsv = csv.reader(f)
schoolDict={}

for line in readCsv:
    schoolDict[line[3]]=line[7]
f.close()

## 함수 선언부
def schoolLoc(schoolName):
    if schoolDict.get(schoolName):
        return schoolDict[schoolName]
    else:
        return ('없음')

if __name__ == '__main__':
    schoolName = sys.stdin.readline().strip()
    print(schoolLoc(schoolName))
