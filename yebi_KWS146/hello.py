# -*- coding: utf-8 -*-
import sqlite3 # db접속 라이브러리
from twitter import *
from konlpy.tag import Kkma
from konlpy.utils import pprint

#인스턴스 <= 객체
t = Twitter(
    auth=OAuth( #인증/증명
        "2901343172-xFtNRQc8SdbZY5WMCVJxVHcq6Y6nvIHshgOEgMQ",
        "tCVvdUav95DKOxRR6BI3zqxrqO2Hzpft54h7Phw4uOM1l",
        "goupuZ0pPcpgFyPDRK3q6qVDe",
        "3ZOmXF82V1pclqnuqN6rgkQ1WWURV1xLjLdkORsfWUb6vvhTw5"))

i = 1
kkma = Kkma()
conn = sqlite3.connect('yebi.db')
c = conn.cursor()

for x in t.statuses.home_timeline(count=199):
    user_id = x['user']['id']

    t = (user_id, )
    c.execute('select count(*) from users where id=?', t)
    count_user = c.fetchone()[0]
    # print count_user

    if count_user == 0: #db안에 user가 없으면 ( 0 )
        name = x['user']['name']
        screen_name = x['user']['screen_name']
        profile_image = x['user']['profile_image_url_https']
        t = (user_id, name, screen_name, profile_image)
        c.execute('insert into users values(?, ?, ?, ?)', t)
        conn.commit()

    tweet_id = x['id']
    t = (tweet_id, )
    c.execute('select count(*) from tweets where id=?', t)
    count_tweets = c.fetchone()[0]
    # print count_tweets

    if count_tweets == 0:
        text = x['text']
        created_at = x['created_at']
        t = (tweet_id, text, created_at, user_id)
        c.execute('insert into tweets values(?, ?, ?, ?)', t)
        conn.commit()

        for n in kkma.nouns(x['text']):
            t = (user_id, n)
            c.execute('select count from user_nouns where user_id=? and noun=?', t)
            count_noun = c.fetchone()
            print count_noun

            if count_noun is None:
                #t = (user_id, n)
                c.execute('insert into user_nouns values(?, ?, 1)', t)
            else:
                c.execute('update user_nouns set count=count+1 where user_id=? and noun=?', t)

    #print "[" + str(i) + "]" + x['user']['screen_name'] + ": " + x['text']
    #print "==============================================="
    #pprint(kkma.nouns(x['text']))
    i += 1
