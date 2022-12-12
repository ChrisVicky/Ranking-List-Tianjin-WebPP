#!C:\SoftwareDevelopment\Dependency\anaconda\python.exe
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
    '“醇风致远”一种提升电动汽车冬季续航的热管理技术',
    '淀粉基凝胶食品增韧的革命者',
    '三生万木潮拼玩具 ——新时代榫卯创新领航者',
    '城市电气智能消防系统',
    '5G毫米波双频收发机芯片',
    '智医“神工”—全球首款人工神经康复机器人系统',
    '硅基射频毫米波频率源芯片',
    'Calino-可利农人工智能监测与数据挖掘系统',
    '贝安居——国内气凝胶建筑保温行业引领者',
]

urls = {
"本科生 创意1组":"http://180.108.46.32:84/ZhengBaSaiIndex/ItemGroup?id=e6071b08-2004-453d-b658-1d8a12145cd3",
"本科生 创意2组":"http://180.108.46.32:84/ZhengBaSaiIndex/ItemGroup?id=e6071b08-2032-4fdf-b940-22682976ce40",
"研究生创意 本研初创组":"http://180.108.46.32:84/ZhengBaSaiIndex/ItemGroup?id=e6071b08-2222-464c-9087-e9fc1b8a2aba",
# "红旅":"http://180.108.46.32:84/ZhengBaSaiIndex/ItemGroup?id=e6071b15-3934-404f-a5f4-3c1af95d2e06",
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
            Team.append({'Star':'' if name in name_list else '','name':name, 'score_list':score_list, 'ave_score':final_score,'group':i})
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

    Fiter_result = []
    for T in Total_result:
        if True:
            Fiter_result.append(T)

    Table = ColorTable(Fiter_result[0].keys(), theme=Themes.OCEAN)
    # Table = PrettyTable(Total_result[0].keys())
    for t in Fiter_result:
        Table.add_row(t.values())
    os.system(clear_command)
    print('数据统计时间',time.ctime())
    print('组别名称', urls.keys())
    print('平均分', all_ave)
    print('8个组平均分' ,[g[0] for g in Group])
    print('总队数',sum([g[1] for g in Group]), [g[1] for g in Group])
    print("计算规则：最终成绩 = 专家评审平均分数 * （全部参赛项目平均分数 / 项目所在组平均分数）")
    print(Table)
    sleep(10)
    exit(0)
