# #선언
import csv
from selenium import webdriver
import time as tm
from selenium.webdriver.common.keys import Keys
import numpy as np
import pandas as pd
import openpyxl
from pandas import DataFrame as df
chromedriver = '/Users/joone/PycharmProjects/web/chromedriver 3'
driver = webdriver.Chrome(chromedriver)
import requests
from bs4 import BeautifulSoup
import telegram_main

url = 'https://sports.news.naver.com/gameCenter/gameResult.nhn?gameId=20190901KTHH02019&category=kbo'

def result2recurl(url):
    return url.replace('gameResult','gameRecord')

url = result2recurl(url)
driver.get(url)
html = driver.page_source
soup = BeautifulSoup(html, 'html.parser')
#=========================================스코어 보드 ====================================================
def scoreboard():
    s1 = soup.find('div', {'class': 'inner'})  # 전체 테이블
    scorerecord = s1.find('h3',{'class':'h_boxscore'})
    scorerecord_text= scorerecord.text
    scoreboard = s1.find('table',{'summary':'경기 스코어보드'})
    scorecolumns_list= []
    scorecolumns = scoreboard.find('thead')
    scorecolumns2 = scorecolumns.find_all('th')
    score_columnsdict ={}
    for i in scorecolumns2:
        scorecolumns_list.append(i.text)
    score_columnsdict = {scorecolumns_list[0]:scorecolumns_list[1:]}
    score_text = scorerecord_text+'\n'
    for k,v in score_columnsdict.items():
        score_text += str(k)+str(v)+'\n'
    # score_columnsdict.keys = scorecolumns_list[0]
    scorelist = scoreboard.find('tbody')
    score_dict={}
    for i in scorelist.find_all('tr'):
        score_list = []
        team = i.find('th').text
        for data in i.find_all('td'):
            score_list.append(data.text)
        score_dict[team]=score_list
    for k,v in score_dict.items():
        score_text += str(k) + str(v) +'\n'
    return score_text








#=============================================타자기록==========================================================


def gameevent():
    s1 = soup.find('div', {'class': 'inner'})  # 전체 테이블
    gameevent = s1.find_all('ul',{'class':'list_gameevent'}) #게임 이벤트
    for event in gameevent:
        a = event.text
    gameeventext = a+'\n'
    return gameeventext



####################Away타자기록
def Abatrecord():
    s1 = soup.find('div', {'class': 'inner'})  # 전체 테이블
    batrecord = s1.find('h3', {'id': 'box_awayBatTitle'})  # 어웨이타자기록텍스트
    batrecord_list = s1.find_all('table',{'summary':'타자기록'})
    team1 = batrecord_list[0].find('tbody')
    resultBatdict = {}
    Abat_text = ''
    for row in team1.find_all('tr'):
        player = row.find('th').text
        playerlist = {}
        for idx,a in enumerate(row.find_all('td')):
            if idx == 13:
                playerlist['타수']=a.text
            elif idx == 14:
                playerlist['안타']=a.text
            elif idx ==15:
                playerlist['타점']=a.text
            elif idx ==16:
                playerlist['득점']=a.text
            elif idx == 17:
                playerlist['타율']=a.text
            else:
                i = str(idx)
                playerlist[i] = a.text
        resultBatdict[player] = playerlist
        Abat_text += '[' + player + ']' + ' 타수=' + str(resultBatdict[player]['타수']) + ' 안타=' + str(resultBatdict[player]['안타']) + ' 타점=' \
                     + str(resultBatdict[player]['타점']) + ' 득점=' + str(resultBatdict[player]['득점']) + ' 타율=' + str(resultBatdict[player]['타율']) + '\n'
    return Abat_text


###############Home타자기록
def Hbatrecord():
    s1 = soup.find('div', {'class': 'inner'})  # 전체 테이블
    batrecord2 = s1.find('h3', {'id': 'box_homeBatTitle'})  # 홈타자기록텍스트
    resultBatdict2={}
    batrecord_list = s1.find_all('table',{'summary':'타자기록'})
    team2 = batrecord_list[1].find('tbody')
    Hbat_text = ''
    for row in team2.find_all('tr'):
        player2 = row.find('th').text
        playerlist2={}
        for idx, b in enumerate(row.find_all('td')):
            if idx == 13:
                playerlist2['타수'] = b.text
            elif idx == 14:
                playerlist2['안타'] = b.text
            elif idx == 15:
                playerlist2['타점'] = b.text
            elif idx == 16:
                playerlist2['득점'] = b.text
            elif idx == 17:
                playerlist2['타율'] = b.text
            else:
                i = str(idx)
                playerlist2[i] = b.text
        resultBatdict2[player2] = playerlist2
        Hbat_text += '['+player2+']'+' 타수='+str(resultBatdict2[player2]['타수'])+' 안타='+str(resultBatdict2[player2]['안타'])+' 타점=' \
                 +str(resultBatdict2[player2]['타점'])+' 득점='+str(resultBatdict2[player2]['득점'])+' 타율='+str(resultBatdict2[player2]['타율'])+'\n'
    return Hbat_text
#====================================================투수기록==========================================================
#원정투수 기록
def Apitrecord():
    s1 = soup.find('div', {'class': 'inner'})  # 전체 테이블
    pitrecord1 =s1.find('h3',{'id':'box_awayPitTitle'})
    pitrecord_list = s1.find_all('table', {'summary': '투수기록'})
    Apitcolumns_list = []
    Apitcolumns = pitrecord_list[0].find_all('th')  # 투수기록
    for i in Apitcolumns:
        Apitcolumns_list.append(i.text)
    teamA = pitrecord_list[0].find('tbody')
    Apitrecord = teamA.find_all('tr')
    Apit_dict = {}
    for i in Apitrecord:
        Apit_list=[]
        playername = i.find('th').text
        for data in i.find_all('td'):
            Apit_list.append(data.text)
        Apit_dict[playername] = Apit_list
    Apit_text = ''
    for key, data in Apit_dict.items():
        Apit_text += '[{}] '.format(key)
        for i, column in zip([9, 10, 11, 12, 13, 15], ['피안타', '사구', '피홈런', '삼진', '실점', '방어율(평균자책)']):
            Apit_text += '{}={} '.format(column, data[i])
        Apit_text += '\n'
    return Apit_text
#홈투수 기록
def Hpitrecord():
    s1 = soup.find('div', {'class': 'inner'})  # 전체 테이블
    pitrecord2 = s1.find('h3', {'id': 'box_homePitTitle'})
    pitrecord_list = s1.find_all('table', {'summary': '투수기록'})
    Hpitcolumns_list =[]
    Hpitcolumns = pitrecord_list[1].find_all('th')
    for i in Hpitcolumns:
        Hpitcolumns_list.append(i.text)
    teamH = pitrecord_list[1].find('tbody')
    Hpitrecord = teamH.find_all('tr')
    Hpit_dict = {}
    for i in Hpitrecord:
        Hpit_list =[]
        playername2 = i.find('th').text
        for data in i.find_all('td'):
            Hpit_list.append(data.text)
        Hpit_dict[playername2]= Hpit_list
    Hpit_text = ''
    for key, data in Hpit_dict.items():
        Hpit_text += '[{}] '.format(key)
        for i,column in zip([9,10,11,12,13,15],['피안타','사구','피홈런','삼진','실점','방어율(평균자책)']):
            Hpit_text +='{}={} '.format(column,data[i])
        Hpit_text += '\n'
    return Hpit_text



def maker(url):

    url = result2recurl(url)
    driver.get(url)
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')











if __name__ == '__main__':
    ##Home팀
    record2 = Hbatrecord(),Hpitrecord()
    for data in record2:
        record_result2 = data
        file = open("Hometeam.txt","a",encoding='utf8')
        file.write(record_result2)
    file.close()
    ##Away팀
    record = Abatrecord(), Apitrecord()
    for data in record:
        record_result= data
        file = open("Awayteam.txt","a", encoding='utf8')
        file.write(record_result)
    file.close()
    #스코어
    file = open("score.txt","a",encoding='utf8')
    file.write(scoreboard()+'\n\n')
    file.write(gameevent())
    file.close();  Hbatrecord(); Hpitrecord(); Abatrecord();  Apitrecord(); driver.quit()
