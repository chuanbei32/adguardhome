import os
import re
import time

from downloader import Downloader
from resolver import Resolver

class Rule(object):
    def __init__(self, name, url):
        self.Name = name
        self.URL = url
        self.Downloader = Downloader(os.getcwd() + '/rules/' + self.Name, self.URL)
        self.Downloader.Download()

def GetRuleList(fileName):
    ruleList = []
    with open(fileName, "r") as f:
        for line in f:
            if len(line) != 0:
                rule = line.split('|')
                ruleList.append([rule[0] + '.filter', rule[1].replace('\n', '').replace('\r', '')])
    return ruleList

def CreatFiters(blackList, whiteList, fileName):
    # 去重、排序
    def sort(L):
        L = list(set(L))
        L.sort()
        return L
    blackList = sort(blackList)
    whiteList = sort(whiteList)

    if os.path.exists(fileName):
        os.remove(fileName)

    f = open(fileName, 'a')
    f.write("!\n")
    f.write("! Title: Adblack DNS Filters\n")
    f.write("! Description: test\n")
    f.write("! Homepage: test\n")
    f.write("! Source: test\n")
    f.write("! Version: %s\n"%(time.strftime("%Y%m%d%H%M%S", time.localtime())))
    f.write("! Last modified: %s\n"%(time.strftime("%Y/%m/%d %H:%M:%S", time.localtime())))
    f.write("! BlackList domains: %s\n"%(len(blackList)))
    f.write("! WhiteList domains: %s\n"%(len(whiteList)))
    f.write("!\n")
    for fiter in blackList:
        f.write("%s\n"%(fiter))
    for fiter in whiteList:
        f.write("%s\n"%(fiter))
    f.close()

def Entry():
    pwd = os.getcwd()
    ruleFile = pwd + '/rules.txt'

    ruleList = GetRuleList(ruleFile)

    for i in range(0, len(ruleList)):
        relue = Rule(ruleList[i][0], ruleList[i][1])

    blackList = []
    whiteList = []
    for i in range(0, len(ruleList)):
        resolver = Resolver(os.getcwd() + '/rules/' + ruleList[i][0])
        L1, L2 = resolver.Resolve()
        blackList += L1
        whiteList += L2

    CreatFiters(blackList, whiteList, pwd + '/adblacklist.txt')

if __name__ == '__main__':
    Entry()
