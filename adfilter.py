import os
import re
import time

from downloader import Downloader
from resolver import Resolver

def GetRuleList(ruleFile):
    ruleList = []
    with open(ruleFile, "r") as f:
        for line in f:
            line = line.replace('\n', '').replace('\r', '')
            if len(line) and not re.match('#', line):
                rule = line.split('|')
                ruleList.append([rule[0], rule[1]])
    return ruleList

def CreatFiters(blockList, unblockList, blockFile, unblockFile):
    # 去重、排序
    def sort(L):
        L = list(set(L))
        L.sort()
        return L

    blockList = sort(blockList)
    if os.path.exists(blockFile):
        os.remove(blockFile)
    f = open(blockFile, 'a')
    f.write("!\n")
    f.write("! Title: adblockfilters\n")
    f.write("! Description: adblockfilters\n")
    f.write("! Homepage: https://github.com/chuanbei32/adguardhome\n")
    f.write("! Source: https://raw.githubusercontent.com/chuanbei32/adguardhome/mian/adblockfilters.txt\n")
    f.write("! Version: %s\n"%(time.strftime("%Y%m%d%H%M%S", time.localtime())))
    f.write("! Last modified: %s\n"%(time.strftime("%Y/%m/%d %H:%M:%S", time.localtime())))
    f.write("! Count: %s\n"%(len(blockList)))
    f.write("!\n")
    for fiter in blockList:
        f.write("%s\n"%(fiter))
    f.close()

    unblockList = sort(unblockList)
    if os.path.exists(unblockFile):
        os.remove(unblockFile)
    f = open(unblockFile, 'a')
    f.write("!\n")
    f.write("! Title: adunblockfilters\n")
    f.write("! Description: adunblockfilters\n")
    f.write("! Homepage: https://github.com/chuanbei32/adguardhome\n")
    f.write("! Source: https://raw.githubusercontent.com/chuanbei32/adguardhome/mian/adunblockfilters.txt\n")
    f.write("! Version: %s\n"%(time.strftime("%Y%m%d%H%M%S", time.localtime())))
    f.write("! Last modified: %s\n"%(time.strftime("%Y/%m/%d %H:%M:%S", time.localtime())))
    f.write("! Count: %s\n"%(len(unblockList)))
    f.write("!\n")
    for fiter in unblockList:
        f.write("%s\n"%(fiter))
    f.close()

def Entry():
    pwd = os.getcwd()
    ruleFile = pwd + '/rules.txt'

    ruleList = GetRuleList(ruleFile)
    # print(ruleList)

    for i in range(0, len(ruleList)):
        Downloader(os.getcwd() + '/rules/' + ruleList[i][0], ruleList[i][1]).Download()

    blockList = []
    unblockList = []
    for i in range(0, len(ruleList)):
        L1, L2 = Resolver(os.getcwd() + '/rules/' + ruleList[i][0]).Resolve()
        blockList += L1
        unblockList += L2

    CreatFiters(blockList, unblockList, pwd + '/adblockfilters.txt', pwd + '/adunblockfilters.txt')

if __name__ == '__main__':
    Entry()
