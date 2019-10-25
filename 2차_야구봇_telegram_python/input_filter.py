# -*- coding: utf-8 -*-
"""
Created on Tue Sep 17 16:41:59 2019

@author: 찬
"""

import re


import datefinder



def file2dict():

    f = open("playerlist.txt","r",encoding='utf-8')
    player_dict = {}
    while True:

        player_info={}
        line = f.readline()

        if not line:
            break
        player_name = line.split()[0]
        player_info['position'] = line.split()[1]
        player_info['team'] = line.split()[2]

        player_dict[player_name]= player_info

    f.close()
    return player_dict


def date_filter(input_text):
    except_pattern = re.compile(
        '\s*[0-9]{1,4}\s*년\s*([0-9]{1,2}\s*월\s*[0-9]{1,2}\s*일)\s*|\s*([0-9]{1,2}\s*월\s*[0-9]{1,2}\s*일)\s*|\s*([0-9]{1,2}\.[0-9]{1,2})\s*')
    result = except_pattern.search(input_text)

    if result:
        # print('except_process')
        for i in range(1, 4):
            md = result.group(i)
            if md != None:
                input_text = md.replace(" ", "")
                if "월" in input_text:
                    input_text = "2019-" + input_text.replace("월", "-")
                else:
                    input_text = "2019-" + input_text.replace(".", "-")
                break

    matches = list(datefinder.find_dates(input_text))
    if len(matches) == 1:
        return matches[0].strftime('%Y%m%d')  # "#"을 사용하면 앞에 붙는 0제거 가능

    else:
        return -1

def dtp_filter(input_text):
    player_dict = file2dict()
    team_list = ['SK','두산','한화','키움','KIA','삼성','롯데','LG','KT','NC']
    date=None; team=None; player=None

    key_word_state = False

    #날짜추출
    if date_filter(input_text) != -1:
        date = date_filter(input_text)
        key_word_state = True



    for player_name in player_dict.keys():
        if player_name in input_text:
            key_word_state = True
            player = player_name
            break

    for team_name in team_list:
        if team_name in input_text:
            key_word_state = True
            team = team_name
            break


    return date,team,player, key_word_state


if __name__ == "__main__":
    input_text = " 11.8 김찬우 NC 알려줘"
    date, team, player = filter(input_text)
    print(date, team, player)