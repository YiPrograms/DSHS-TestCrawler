#! /usr/bin/env python3
from bs4 import BeautifulSoup
import urllib
import requests
import re

import argparse

parser = argparse.ArgumentParser(description="取得數位管理系統週複習考成績", formatter_class=argparse.RawTextHelpFormatter)
parser.add_argument("PHPSESSID", help=\
'''PHP Session ID

取得方法:
1. 登入數位管理系統後按下 F12
2. 選擇 主控台(Console) 頁面
3. 執行 document.cookie
4. 複製 PHPSESSID= 之後的字串
Ex: ji8a9anc6ivljir7ag781acj22''')

filter_group = parser.add_argument_group("篩選", "格式: <學年(-y)><考試類型(-t)>成績第<週(-w)>週-<日期(-d)> (<科目(-s)>)<名稱(-n)>\n也可以同時篩選多個條件 Ex: -w 1 2 3 -n 高一 高1")
filter_group.add_argument("-y", "--year", help="學年  Ex: 108.1", nargs="+")
filter_group.add_argument("-t", "--type", help="考試類型 (週考/複習考/小考/暑輔)", nargs="+")
filter_group.add_argument("-w", "--week", help="週  Ex: 10", nargs="+")
filter_group.add_argument("-d", "--date", help="日期  Ex: 1003", nargs="+")
filter_group.add_argument("-s", "--subject", help="科目  Ex: 化學", nargs="+")
filter_group.add_argument("-n", "--name", help="(部份)名稱 Ex: 高三忠孝", nargs="+")
filter_group.add_argument("-nn", "--noname", help="<不包含> (部份)名稱 Ex: 仁", nargs="+")
filter_group.add_argument("-c", "--custom", help="自訂篩選  Ex: (化學)高三自然組", nargs="+")

parser.add_argument("-l", "--list", help="只列出篩選結果 不下載", action="store_true")

parser.add_argument("--url", help="自訂系統網址 Ex: http://homebook.tshs.tp.edu.tw/schooldongshan",
                    default="http://homebook.tshs.tp.edu.tw/schooldongshan")

args = parser.parse_args()

cookie = {"PHPSESSID": args.PHPSESSID}

url = args.url + "/director/weekgrade_info.php"
file_url = args.url + "/LargeExam/Week/{}"

post = {"EditType": "",
"order_word_type": "desc",
"order_word": "",
"order_word2": "",
"IOUpdate": "",
"DelStatus": "N",
"Status": "",
"Section": "",
"CourseId": "",
"tx_Week": "查詢週次".encode("utf-8"),
"page_limit1": "10000", "page1": "1", "page_limit2": "10000", "page2": "1"}

req = requests.post(url, data=post, cookies=cookie)

soup = BeautifulSoup(req.content, "lxml")

a_tags = soup.find_all("a")[1:]

if len(a_tags) == 0:
    print("取得成績列表失敗")
    exit()


pattern = r"([0-9.]+)(.+)成績第(\d+)週-(\d+) ?\((.+)\)(.+)"

def match(a_str):
    m = re.match(pattern, a_str)
    if m is not None:
        y, t, w, d, s, n = m.groups()
        if args.year:
            if sum([y==k for k in args.year])==0:
                return False
        if args.type:
            if sum([k in t for k in args.type])==0:
                return False
        if args.week:
            if sum([w==k for k in args.week])==0:
                return False
        if args.date:
            if sum([d==k for k in args.date])==0:
                return False
        if args.subject:
            if sum([k in s for k in args.subject])==0:
                return False
        if args.name:
            if sum([k in n for k in args.name])==0:
                return False
        if args.noname:
            if sum([k in n for k in args.noname])!=0:
                return False
    elif args.custom is None:
        return False

    if args.custom:
        if sum([k in a_str for k in args.custom])==0:
            return False
    
    return True

found = []

for a in a_tags:
    if match(a.string[:-4]):
        found.append(a)

if len(found) == 0:
    print("查詢無結果")
    exit()

if args.list:
    print("查詢結果 (共{}筆)：".format(len(found)))
    for a in found:
        print(a.string[:-4])
else:
    print("開始下載...")
    for i in range(len(found)):
        file_name = found[i].get("href")[17:-2]
        print("({}/{}) 下載 {} 中...".format(i+1, len(found), found[i].string))
        down = requests.get(file_url.format(file_name))
        open(found[i].string, "wb").write(down.content)

