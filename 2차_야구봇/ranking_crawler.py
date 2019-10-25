# -*- coding: utf-8 -*-
"""
Created on Wed Sep 18 17:08:37 2019

@author: Onedas
"""

##
from selenium import webdriver
from bs4 import BeautifulSoup
import time

import IPython.display as dp
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os


## webdriver options
options = webdriver.ChromeOptions()
options.add_argument('--headless') # 인터페이스 없는
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
options.add_argument('--window-size=1920x1080')
chromedriver = 'chromedriver.exe'

def url2soup(url='https://sports.news.naver.com/kbaseball/record/index.nhn?category=kbo'):
#     url = 'https://sports.news.naver.com/kbaseball/record/index.nhn?category=kbo'
    
    driver = webdriver.Chrome(chromedriver,options=options)
    
    driver.implicitly_wait(3)
    driver.get(url)
    
    time.sleep(3)
    html = driver.page_source
    soup = BeautifulSoup(html,'html.parser')
    ##
    return soup

def recordSoup2teamrank(soup):
    teamrank = soup.find('div',{'class':'tbl_box'}).text.replace('최근 10경기','최근10경기').split()
    teamrank.pop(0) #'팀별순위'
    teamrank.pop(0) #'테이블'
    
    ranks=[]
    start = 0
    step  = 12
    for i in range(11):
        start= start
        end = start+step
        rank=teamrank[start:end]
        ranks.append(rank)
        start = end
        
    data=pd.DataFrame(ranks)
    
    del data[0]
    data.columns=data.loc[0]
    data = data.drop(0)
    
    return data

def recordSoup2mainrank(soup):
    personalrank=soup.find('div',{'class':'tbl_box p_head'})
    
    d = {}
    categorys = list(map(lambda x:x.text.replace(' ','').split(), personalrank.find_all('thead')))
    categorys = np.array(categorys).reshape(-1)
    
    people = list(map(lambda x:x.text.replace(' ','').split(), personalrank.find_all('tbody')))
    people = np.array(people).reshape(-1)
    
    for cate_idx,cate in enumerate(categorys):        

        start=0+cate_idx*20
        step=4
        new_table=pd.DataFrame()
        for rank_idx in range(5):
            value = list(people[start:start+step])

            new_table[rank_idx+1]=value[1:]
            start=start+step
        new_table.index=['이름','팀','값']
        d[cate] = new_table.transpose()
    return d

def recordSoup2pitcherrank(soup):
    pitcherRecord_table=soup.find('div',{'id':'_pitcherRecord'})
    pitcherRecords_list=pitcherRecord_table.text.replace(' ','').split()
    pitcherRecords_list.pop(0) #다음기록
    pitcherRecords_list.pop(0) #이전기록

    categorys = pitcherRecords_list[1:17]
    start,step = 17,16
    
    pitcherRank = pd.DataFrame()
    for i in range(20):
        pitcherRank[i+1] = pitcherRecords_list[start:start+step]
        start=start+step
    pitcherRank.index=categorys
    pitcherRank=pitcherRank.transpose()
    del pitcherRank['순위']
    
    start,step = start,10

    categorys2 = pitcherRecords_list[start+1:start+step+1]
    start=start+step+1
    pitcherRank2 = pd.DataFrame()
    for i in range(20):
        pitcherRank2[i+1] = pitcherRecords_list[start:start+step]
        start=start+step
    pitcherRank2.index=categorys2
    pitcherRank2=pitcherRank2.transpose()
    del pitcherRank2['순위']
    
    
    return pitcherRank, pitcherRank2

def recordSoup2batterrank(soup):
    batterRecord_table=soup.find('div',{'id':'_batterRecord'})
    batterRecords_list=batterRecord_table.text.replace(' ','').split()
    batterRecords_list.pop(0) #타자순위
    batterRecords_list.pop(0) #순위
    
    categorys = batterRecords_list[1:17]
    start,step = 17,16
    batterRank = pd.DataFrame()
    for i in range(20):
        batterRank[i+1] = batterRecords_list[start:start+step]
        start=start+step
    batterRank.index=categorys
    batterRank=batterRank.transpose()
    del batterRank['순위']
    
    start,step = start,9
    
    categorys2 = batterRecords_list[start+1:start+step+1]
    start=start+step+1
    batterRank2 = pd.DataFrame()
    for i in range(20):
        batterRank2[i+1] = batterRecords_list[start:start+step]
        start=start+step
    batterRank2.index=categorys2
    batterRank2=batterRank2.transpose()
    del batterRank2['순위']
    
    return batterRank, batterRank2

def RankRecord(years=2019):
    # 년도 입력 필요 default = 최근(2019)
    url = 'https://sports.news.naver.com/kbaseball/record/index.nhn?category=kbo'
    years = 2019
    
    soup1 = url2soup(url+'&'+str(years))
    soup2 = url2soup(url+'&'+str(years)+'&type=batter&playerOrder=hra')
    
    
    d={} #각각의 데이터는 pd.DataFrame
    d['팀별순위']=recordSoup2teamrank(soup1)
    d['주요부문선두']=recordSoup2mainrank(soup1) 
                    # {다승순위,평균자책순위,탈삼진순위,세이브순위,
                    #  타율순위,타점순위,홈런순위,도루순위,
                    #   WHIP순위,OPS순위,투수WAR순위,타자War순위}
    d['투수순위']=list(recordSoup2pitcherrank(soup1)) #[DataFrame, DataFrame]
    d['타자순위']=list(recordSoup2batterrank(soup2)) #[DataFrame, DataFrame]
    
    return d

def save_as_txt(years):
    d=RankRecord(years)
    root = os.getcwd()
    if not(os.path.exists(root+'/Ranking')):
        os.mkdir(root+'/Ranking/')
    
    # 팀별순위
    if not(os.path.exists(root+'/Ranking/Team')):
        os.mkdir(root+'/Ranking/Team/')
        
    with open(root+'/Ranking/Team/'+str(years)+'.txt','w',encoding='utf-8') as f:
        f.write(str(d['팀별순위']))
    
    # 주요부문선두
    if not(os.path.exists(root+'/Ranking/Main')):
        os.mkdir(root+'/Ranking/Main/')
        
    with open(root+'/Ranking/Main/'+str(years)+'.txt','w',encoding='utf-8') as f:
        for d_ in d['주요부문선두']:
            f.write(str(d_)+'\n')                
            f.write(str(d['주요부문선두'][d_])+'\n\n')
        
    #투수순위
    if not(os.path.exists(root+'/Ranking/Pitcher')):
        os.mkdir(root+'/Ranking/Pitcher/')
        
    with open(root+'/Ranking/Pitcher/'+str(years)+'.txt','w',encoding='utf-8') as f:
        for d_ in d['투수순위']:
            f.write(str(d_)+'\n\n')
        
    #타자순위
    if not(os.path.exists(root+'/Ranking/Batter')):
        os.mkdir(root+'/Ranking/Batter/')
        
    with open(root+'/Ranking/Batter/'+str(years)+'.txt','w',encoding='utf-8') as f:
        for d_ in d['타자순위']:
            f.write(str(d_)+'\n\n')
    
    print(years,'years Done')
    
def load_Ranking(years=2019,keys=['Team','Main','Batter','Pitcher']):
    root=os.getcwd()
    text = ''
    # 하나만 올경우
    if not(type(keys)==list):
        keys=[keys]
    
        
    for key in keys:
        path = '/Ranking/{}/{}.txt'.format(key,years)
        #있는지 없는지 체크
        if not(os.path.exists(root+path)):
            raise 'data가 없습니다'
        # 있으면 열기
        with open(root+path, 'r', encoding='utf-8') as f:
            for line in f:
                text+=line
        text += '\n'
    
    return text

if __name__ =='__main__':
#    for i in range(2015,2020):    
#        save_as_txt(i)
    
    print(load_Ranking())




    pass
