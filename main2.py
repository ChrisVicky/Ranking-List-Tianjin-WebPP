from typing import final
from unittest import expectedFailure
from bs4 import BeautifulSoup
from urllib.request import urlopen
from requests import exceptions
from prettytable import PrettyTable
from prettytable.colortable import ColorTable, Themes
import os 
from time import sleep
import time
import sys

clear_command = ""
if sys.platform == 'linux':
    clear_command = "clear"
else:
    clear_command = "cls"
os.system(clear_command)

name_list = [
    'TickTest生物——一站式智能检疫平台',
    '海澹科技——全球激光海洋探测领导者',
    'Z.U.E.S: 应急响应无人机蜂群系统',
    '基于区块链的多层级信用卡风控系统',
    '“醇风致远”一种提升电动汽车冬季续航的热管理技术',
    '淀粉基凝胶食品增韧的革命者',
    '三生万木潮拼玩具 ——新时代榫卯创新领航者',
    '城市电气智能消防系统',
    'AI Optimizer: 基于强化学习的智能化军事作战决策平台',
    '5G毫米波双频收发机芯片',
    '同天医疗——微创外科手术高端培训专家',
    '储能先锋——国际领先的硫化锂纳米晶生产者',
    '硅基射频毫米波频率源芯片',
    '网联智控管道空间蓄热系统',
    'Calino-可利农人工智能监测与数据挖掘系统',
    '智医“神工”—全球首款人工神经康复机器人系统',
    '斗拱Newer——“斗拱你玩”指尖模玩创想家项目计划书',
    '沙盒科技––Consensor AI故障探测器',
]

urls = {
"本科生 创意1组":"http://180.108.46.32:84/LuYanIndex/ItemGroup?id=e6071710-1411-406f-a1de-efd2683bd852",
"本科生 创意2组":"http://180.108.46.32:84/LuYanIndex/ItemGroup?id=e6071710-142e-4c56-bdcd-a1f3c5e845e4",
"本科生 创意3组":"http://180.108.46.32:84/LuYanIndex/ItemGroup?id=e6071710-1524-4975-b862-215386c56596",
"本科生 创意4组":"http://180.108.46.32:84/LuYanIndex/ItemGroup?id=e6071710-1614-4b31-8b15-d05f4562337a",
"本科生 创意5组":"http://180.108.46.32:84/LuYanIndex/ItemGroup?id=e6071710-1625-4104-a25a-4ec005264cac",
"本科生 创意6组":"http://180.108.46.32:84/LuYanIndex/ItemGroup?id=e6071710-162f-4432-84f1-fd239515b1d9",
# "研究生 创意1组":"http://180.108.46.32:84/LuYanIndex/ItemGroup?id=e6071710-1725-4e32-9e06-b6516924b734", 
# "本研 初创成长组":"http://180.108.46.32:84/LuYanIndex/ItemGroup?id=e6071713-1909-4fc6-a6d1-cd92fdb7f72f", 
}

while(1):
    Total = []
    Group = []
    TRY = [0 for i in range(len(urls))]
    for j in range(len(urls)):
        url = list(urls.values())[j]
        i = list(urls.keys())[j]
        print(i,'获取html中','第',TRY[j]+1,'次尝试', end='...\r')
        try:
            TRY[j] = TRY[j] + 1
            html = urlopen(url)
        except exceptions.RequestException:
            print(i,'获取数据失败，重试')
            if TRY[j] >= 4:
                exit(0)
            j = j-1
            continue
        else:
            print(i,html,end=' ')
        # html = open('./page.html','r',encoding='utf-8') 
        # print(i, html, end=' ')
        
        bs = BeautifulSoup(html, 'lxml')

        table = bs.find(attrs={'class':'c-page-ul c-item'})
        teams = table.find_all('div', attrs={"class":"item-info"})

        Team = []
        for team in teams:
            name = team.find('div',attrs={"class":"itemname"}).text
            score_list = []
            scores = team.find('ul', {"class":"item-info-score"})
            for s in scores.find_all('div'):
                score_list.append(float(s.text))
            final_score = float(team.find('span', {'class':"score-result-value"}).text)
            Team.append({'Star':'' if name in name_list else '','name':name, 'score_list':score_list, 'ave_score':final_score,'group':i})
        print('解析完成')
        Group.append([sum(t['ave_score'] for t in Team) / len(Team), len(Team)])
        Total.append(Team)

    print("分组统计结束，进行分数计算")
    
    all_ave = sum([g[1]*g[0] for g in Group]) / sum(g[1] for g in Group)

    for i,T in enumerate(Total):
        t_ave = Group[i][0]
        for t in T:
            t['final_score'] = t['ave_score'] * all_ave / t_ave
    
    Total_result = []
    for t in Total:
        for T in t:
            Total_result.append(T)
    Total_result.sort(key=lambda x:x['final_score'])
    Total_result.reverse()
    Len = len(Total_result)
    for i,t in enumerate(Total_result):
        t['ranking']= f"{i+1}/{Len}"

    Table = ColorTable(Total_result[0].keys(), theme=Themes.OCEAN)
    # Table = PrettyTable(Total_result[0].keys())
    for t in Total_result:
        Table.add_row(t.values())
    os.system(clear_command)
    print('数据统计时间',time.ctime())
    print('组别名称', urls.keys())
    print('平均分', all_ave)
    print('8个组平均分' ,[g[0] for g in Group])
    print('总队数',sum([g[1] for g in Group]), [g[1] for g in Group])
    print("计算规则：最终成绩 = 专家评审平均分数 * （全部参赛项目平均分数 / 项目所在组平均分数）")
    print(Table)
    sleep(5)