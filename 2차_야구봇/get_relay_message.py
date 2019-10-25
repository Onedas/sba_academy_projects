import os

def get_team_message(date,team):

    path = "data/" + date + "/" + team + "/" + team+".txt"

    if not os.path.exists(path):
        return team+"의 경기는" + date + "에 없습니다"


    else:
        f = open(path,"r",encoding="utf-8")
        message = f.read()
        f.close()

    return message

def get_player_message(date,team,player):

    path = "data/" + date + "/" + team + "/" + player +".txt"

    if not os.path.exists(path):
        return team+"의 경기는" + date + "에 없습니다"

    else:
        f = open(path,"r",encoding="utf-8")
        message = f.read()
        f.close()

    return message

def get_game_graph(date,team):

    path = "data/" + date + "/" + team + "/" + "graph.png"
    return path


if __name__ == '__main__':

    t = get_game_graph('20190901', '한화')
    print(t)