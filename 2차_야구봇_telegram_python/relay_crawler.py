# -*- coding: utf-8 -*-
"""
Created on Wed Sep 18 16:12:16 2019

@author: 찬우
"""

from selenium import webdriver
from bs4 import BeautifulSoup
import re
import time
import input_filter



chromedriver = 'chromedriver.exe'
#options = webdriver.ChromeOptions()
#options.add_argument('--headless') # 인터페이스 없는
#options.add_argument('--no-sandbox')
#options.add_argument('--disable-dev-shm-usage')
#options.add_argument('--window-size=1920x1080')
#chromedriver = 'chromedriver.exe'


driver = webdriver.Chrome(chromedriver)#,options = options)
driver.implicitly_wait(3)


def pattern_maker_player(player_list):

    str = ""
    for player in player_list:
        str += player + '|'
    str = str[0:len(str)-1]

    pattern = re.compile(str)

    return pattern


#def team_member_crawler(url,selector):
#    driver.get(url)
#    (driver.find_element_by_class_name('mnu')).click()
#    css_selector = '#'+selector+'_lineup_btn'
#    (driver.find_element_by_css_selector(css_selector)).click()
#
#    html = driver.page_source
#    soup = BeautifulSoup(html,'html.parser')
#
#
#    if selector=="away":
#        lineup_popup_page = soup.find('div', {'class': 'lft_lineup'})
#    else:
#        lineup_popup_page = soup.find('div', {'class': 'rgt_lineup'})
#
#    table = lineup_popup_page.find_all('tbody')[1]
#
#    team_info_dict = {}
#    players = table.find_all('tr')
#    for player in players:
#        player_dict = {}
#        datas = player.find_all('td')
#        player_name = datas[1].find('dt').text
#        player_dict['playerInfo'] = datas[1].find('dd').text.strip().replace("\t","").split("\n")
#        player_dict['position'] = datas[2].text
#        player_dict['seasonBA'] = datas[12].text
#        player_dict['vsBA'] = datas[13].text
#        team_info_dict[player_name] = player_dict
#
#    return team_info_dict

def find_team(hitter_name, away_player_list,away_team,home_team):
    if hitter_name in away_player_list:
        return away_team
    else:
        return home_team

def get_result_index(history):
    print(history)
    pattern = re.compile("[가-힣]{1,6}\s:|[가-힣]{1,6}\s[가-힣]{1,6}\s:")
    index = pattern.search(history).end()
    return index

def relay_parser(soup):
    # 문자중계창 안에 있는 html 소스만 뽑아낸다
    relay_text = soup.find(id='relay_text').decode_contents()

    # 뽑아낸 relay_text를 파싱하여 soup에 담는다
    soup_relay = BeautifulSoup(relay_text, 'html.parser')

    # 타자이름에 관한 정보를 얻는다
    hitters = soup_relay.find_all('h5')

    # 각 타자에 대하여
    inningDict = {}
    player_info_dict = input_filter.file2dict()
    for hitter in hitters:

        hitter_name = find_name_by_regularExpression(hitter.text)
        #team_name = find_team(hitter_name,away_player_list,away_team,home_team)
        team_name = player_info_dict[hitter_name]['team']
        history = hitter.find_next_sibling()

        historyList = []

        while history.name == 'p':

            if is_history_of_hitter(hitter_name, history.text):
                historyList.insert(0, history.text)
                # if find_ballcount_by_regularExpression(history.text):
                #     historyList.insert(0, history.text)
                # else:
                #     index = get_result_index(history.text)
                #     historyList.insert(0,history.text[index+1:])
                #     #historyList.insert(0,(history.text.split(':'))[1][1:])
            if not history.find_next_sibling():
                break
            history = history.find_next_sibling()

        historyList.insert(0,team_name)

        inningDict[hitter_name] = historyList

    return inningDict


def is_history_of_hitter(hitter,history):
    if hitter in history:
        return True
    elif find_ballcount_by_regularExpression(history):
        return True
    else:
        return False

def find_name_by_regularExpression(hitter_history):


    p = re.compile('[0-9가-힣]{1,5}\s[가-힣]{1,6}\s:\s[가-힣]{1,5}\s[가-힣]{1,6}\s\(으\)로\s교체')
    result =p.match(hitter_history)

    if result != None:
        hitter_name = result.group().split()[4] #교체된 선수

    else:
        hitter_name = hitter_history.split()[1]

    return hitter_name

def find_ballcount_by_regularExpression(hitter_history):

    p = re.compile('-\s\d{1,2}구\s[가-힣]{1,10}')
    result = p.match(hitter_history)
    if result != None:
        return True
    else:
        return False

def print_all(relay_list,):

    for idx, relay in enumerate(relay_list):

        print("="*30, "{}이닝 기록".format(idx+1), "="*30)
        for player, historys in relay.items():
            print("[", player, "]")
            for history in historys:
                print(history)
            print()


def print_playerHistory(player, relay_list):
    for i,relay in enumerate(relay_list):
        if player in relay.keys():
            print("="*30,i+1,"이닝","="*30)
            print()
            for idx, history in enumerate(relay[player]):
                if find_ballcount_by_regularExpression(history):
                    print(history)
                elif idx > 0 and not find_ballcount_by_regularExpression(history):
                    print(history)
            print()

def print_teamHistory(team, url):
    relay_list = crawler(url)
    text=""

    for i,relay in enumerate(relay_list):
        #print("=" * 30, i + 1, "이닝", "=" * 30)
        #print()
        text += "="*10 + str(i+1) +"이닝" +"="*10 +'\n'
        for player,historys in relay.items():
            if historys[0] == team:
                #print('[',player,']')
                text += '[' + player + ']' + '\n'
                for i,history in enumerate(historys):
                    if i>0:
                        #print(history)
                        text+=history+'\n'
                #print()
                text+="\n"
        #print()
        text+="\n"
    return text


def crawler(url):
    print("Test3")
    driver.get(url)
    (driver.find_element_by_class_name('mnu')).click()

    resultList = []

    for i in range(1, 10):

        #1~9이닝까지
        driver.find_element_by_id('inning_tab_' + str(i)).click()
        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')

        inningDict = relay_parser(soup)

        resultList.append(inningDict)

    driver.quit()
    return resultList


def RelayScenario(url,away_team,home_team):
    print("테스트5")
    #각팀의 선수별 정보 가져오기 => 사용자가 선수이름 고르면 먼저 보여주기

    away_player_info = team_member_crawler(url,selector='away')
    home_player_info = team_member_crawler(url,selector='home')


    away_player_list = list(away_player_info.keys())
    home_player_list = list(home_player_info.keys())

    player_pattern = pattern_maker_player(away_player_list+home_player_list)
    relay_list = crawler(url, away_player_list,away_team,home_team)


    event_pattern = re.compile("안타|홈런|타율")
    summary_pattern = re.compile("경기|요약|정리|분석")



    #팀명 확인
    #선수 포함? => 선수 물어보는 의도 => 해당 선수 정보 보여주기 / 해당 선수에 대한 문자기록 보여주기 / 오늘 기록 분석(준기형)
    #선수 포함x => 팀의 성적을 물어보는 의도 => 팀의 모든 선수 문자기록 보여주기 / 팀 scoreboard(준기형)

    print("{} VS {}경기에 대해서 알려드릴께요!".format(away_team,home_team))

    while(True):
        request = input("=> ")
        #사용자 요청에 away 선수들 이름이없다면
        # away팀 이름만 쳤거나 home팀

        # 타자의 정보를 궁금해하는 의도
        request_players = player_pattern.findall(request)
        if request_players:
            if event_pattern.search(request):
                # "김찬우 안타쳤어?" 에 대한 답변
                # 준기형 데이터에서 선수이름 찾고 이벤트에 대한 데이터 출력 / 다른 선수와의 비교
                # for player in request_players:
                #     print_playerHistory(player, relay_list)
                pass
            else:
                for player in request_players:
                    print_playerHistory(player, relay_list)
                    # 준기형 데이터에서 선수이름 찾고 모든 이벤트 데이터 출력

        else:
            if home_team in request:
                print_teamHistory(home_team, relay_list)
            elif away_team in request:
                print_teamHistory(away_team, relay_list)
            else:
                if event_pattern.search(request):
                    #준기형 안타/타율/홈런 데이터 검색 => 이벤트에 해당하는 데이터들 출력 및 최대 데이터 출력(max함수)
                    pass

                else:
                    if summary_pattern.search(request):
                        print_all(relay_list)
                        #준기형 경기 정리 데이터 출력
                    else:
                        print("제가 멍청해서 잘 못 알아들었어요ㅜㅜ 다시 입력해주세요")



if __name__ == '__main__':
    RelayScenario('https://sports.news.naver.com/gameCenter/gameResult.nhn?category=kbo&gameId=20190901KTHH02019','KT','한화')

    result_list = crawler('https://sports.news.naver.com/gameCenter/gameResult.nhn?category=kbo&gameId=20190901KTHH02019')
    t = (print_teamHistory('KT',result_list))