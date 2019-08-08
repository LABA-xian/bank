# -*- coding: utf-8 -*-
"""
Created on Sat Sep  8 11:45:36 2018

@author: MB207-1
"""

from urllib.request import urlopen
from bs4 import BeautifulSoup
from urllib.parse import quote
import re
import csv
import time

def gethtml(url):
    tmp = url
    html = urlopen(tmp)
    bsobj = BeautifulSoup(html, 'lxml')
    return bsobj


def witerfile(arr = []):
    pattern = re.compile("[^\u4e00-\u9fa5^.^a-z^A-Z^0-9^(^)^，^。^?]")
    with open("output.csv", "w", encoding = "utf-8-sig") as file:
        writer = csv.writer(file)
        for context in arr:
            context = pattern.sub("", context)
            writer.writerows(zip([context]))

def remove(arr = []):
    
    l2 = list(set(arr))
    l2.sort(key = arr.index)
    return l2
    

bs = gethtml("https://law.banking.gov.tw/Chi/FSYS/tree.aspx")
list_a = bs.find_all('a')

save_url = [] #分類
aa = None

for a in list_a:
    if a.text == ':::': #去掉第一筆沒用資料
        pass
    else:
        try:
            bs =  gethtml("https://law.banking.gov.tw/Chi/FSYS/" + a.get("href"))
            list_a_l2 = bs.find_all('a')
            for a2 in list_a_l2:
                try:
                    save_url.append(a2.get("href"))
                except:
                    pass
        except:
            pass
 
       
save_url = remove(save_url)
savecontext = []

for url in save_url:
    try:
        search = re.search(r'lsid.*', str(url))
        bs = gethtml("https://law.banking.gov.tw/Chi/FLAW/FLAWDAT0202.aspx?" + str(search.group(0)))
        time.sleep(0.5)
        for context in bs.select(".ContentArea-law"):
            print(context.text)
            savecontext.append(context.text)
    except:
        pass

savecontext = remove(savecontext)
witerfile(savecontext)

