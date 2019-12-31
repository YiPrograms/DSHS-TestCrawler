#! /usr/bin/env python3
import pandas as pd
import os
from math import isnan

import argparse

parser = argparse.ArgumentParser()
parser.add_argument("Class", help="班級  Ex: 忠")
parser.add_argument("--grade", help="年級 (非必要，確認用)  Ex: 3")
parser.add_argument("-o", "--outfile", help="輸出檔案 [Out.csv]", default="Out.csv")

args = parser.parse_args()

f = open(args.outfile, "w")

res = {}
entries = []

from datetime import datetime
import re
pattern = r"(\d)年.班\((.+)\)"

for filename in os.listdir(os.getcwd()):
    if filename.endswith(".xls"):
        xls = pd.ExcelFile(filename)
        grade, subject = re.match(pattern, xls.sheet_names[0]).groups()
        if args.grade:
            grade = args.grade
        sname = "{}年{}班({})".format(grade, args.Class, subject)
        if sname not in xls.sheet_names:
            print("無法在檔案 {} 中找到工作表 {}, 將忽略此檔案".format(filename, sname))
            continue
        xls = pd.read_excel(filename, header=None, index_col=None, sheet_name=sname)
        date = xls[19][0]
        title = xls[6][0]
        entry = (date, title, subject)
        entries.append(entry)
        print("已讀取 {} {}".format(date.strftime("%m/%d"), subject))
        names = list(xls[1][5:])
        end_idx = names.index(next(n for n in names if str(n)=="nan")) +5
        names = list(xls[1][5:end_idx])
        nums = list(map(int, xls[0][5:end_idx]))
        person = list(zip(nums, names))
        scores = list(xls[3][5:end_idx])
        
        for i in range(len(scores)):
            if str(scores[i])!="nan":
                if person[i] not in res.keys():
                    res[person[i]] = {}
                res[person[i]][title] = scores[i]

entries.sort()

header1 = args.Class + "," + ",".join([e[2] for e in entries])
header2 = "," + ",".join([e[0].strftime("%m/%d") for e in entries])

f.write(header1 + "\n" + header2 + "\n")

for person, sc in sorted(res.items()):
    name = str(person[0]) + " " + str(person[1]).replace("\ue944", "").replace("\ue048", "").replace("\ue716", "")
    f.write(name + "," + ",".join([str(sc[t]) if t in sc.keys() else "X" for _, t, _ in entries]) + "\n")

f.close()

print(res.keys())

print("已讀取 {} 筆資料，輸出到 {}".format(len(entries), args.outfile))