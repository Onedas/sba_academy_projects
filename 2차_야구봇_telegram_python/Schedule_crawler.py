# -*- coding: utf-8 -*-
"""
Created on Tue Sep 17 17:35:42 2019

@author: 찬
"""

from selenium import webdriver
from bs4 import BeautifulSoup
import time
import input_filter

chromedriver = 'chromedriver.exe'
driver = webdriver.Chrome(chromedriver)
driver.implicitly_wait(3)
url = 'https://sports.news.naver.com/kbaseball/schedule/index.nhn'
driver.get(url)
#time.sleep(5)
html = driver.page_source
soup = BeautifulSoup(html, 'html.parser')
driver.quit()

def print_dailySchedule(date):
    resultDict = crawler()
    text = ""
    for idx, game in enumerate(resultDict[date]):
        if game['nogame'] == True:
            text = "오늘은 경기가 없는 날입니다\n"
            return text
        if game['iscanceled'] == True:
            text += '[취소된 경기]' + game['leftTeam'] + ' VS ' + game['rightTeam'] + '\n'

        text += game['leftTeam'] +" "+ game['score'] +" "+ game['rightTeam'] + '\n'
    return text


def get_game_url(date, team):
    resultDict = crawler()
    for game in resultDict[date]:
        if game['iscanceled'] == True:
            return ""
        if game['leftTeam'] == team or game['rightTeam'] == team:
            return game['url']


def makeGameDict(gameInfo,time,team_lft,team_rgt,score,stadium,url):

    if score == 'VS':
        score = ""

    iscanceled = False

    if time == "-":
        nogame = True

    else:
        nogame = False
        if url == "":
            iscanceled = True

    gameInfo['time'] = time
    gameInfo['leftTeam'] = team_lft
    gameInfo['rightTeam'] = team_rgt
    gameInfo['score'] = score
    gameInfo['stadium'] = stadium
    gameInfo['url'] = url
    gameInfo['iscanceled'] = iscanceled
    gameInfo['nogame'] = nogame

    return gameInfo

def crawler():

    calendar = soup.find('div', {'class': 'tb_wrap'})

    tb1 = calendar.find_all('div', {'class': 'sch_tb'})
    tb2 = calendar.find_all('div', {'class': 'sch_tb2'})
    games = tb1+tb2

    resultDict = {}

    for game in games:

        gameList=[]
        date=""
        rows = game.find_all('tr')

        for idx, row in enumerate(rows):
            gameInfo={}

            if(idx==0):
                temp = (row.find('span',{'class':'td_date'})).text.replace(" ","").split("(")[0]
                date = input_filter.date_filter(temp)
            time = row.find('span',{'class':'td_hour'}).text
            if time != '-': #경기있는날

                team_lft = row.find('span',{'class':'team_lft'}).text
                score = row.find('strong',{'class':'td_score'}).text
                team_rgt = row.find('span',{'class':'team_rgt'}).text
                stadium = row.find_all('span',{'class' : 'td_stadium'})[1].text


                if "경기취소" in row.text:
                    url = ""
                else:
                    url = 'https://sports.news.naver.com'+ (row.find_all('a')[0])["href"]

            else:
                team_lft = "";team_rgt = ""; score = ""; stadium = ""; url = ""

            gameInfo = makeGameDict(gameInfo,  time, team_lft, team_rgt, score, stadium, url)
            gameList.append(gameInfo)

        resultDict[date]=gameList

    return resultDict
