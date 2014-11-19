# -*- coding: utf-8 -*-
import sqlite3 # DB접속 라이브러리
import sys
from konlpy.tag import Kkma
from twitter import *


reload(sys)
sys.setdefaultencoding('utf-8')

# 인스턴스 <= 객체

t = Twitter(
    auth=OAuth( #트위터 계정인증
        "2901343172-xFtNRQc8SdbZY5WMCVJxVHcq6Y6nvIHshgOEgMQ",
        "tCVvdUav95DKOxRR6BI3zqxrqO2Hzpft54h7Phw4uOM1l",
        "goupuZ0pPcpgFyPDRK3q6qVDe",
        "3ZOmXF82V1pclqnuqN6rgkQ1WWURV1xLjLdkORsfWUb6vvhTw5"))

i = 1
kkma = Kkma()
conn = sqlite3.connect('yebi.db')
c = conn.cursor()

print '트위터 타임라인 탐색 중.'

for x in t.statuses.home_timeline(count=20):
    user_id = x['user']['id']

    print ''
    print '=' * 80
    print '... @%s: %s' % (x['user']['name'],  x['text'])

    t = (user_id, )
    c.execute('select count(*) from users where id=?', t)
    count_user = c.fetchone()[0]
    # print count_user

    if count_user == 0: #DB안에 User가 없으면 ( 0 )
        name = x['user']['name']
        screen_name = x['user']['screen_name']
        profile_image = x['user']['profile_image_url_https']
        t = (user_id, name, screen_name, profile_image)
        c.execute('insert into users values(?, ?, ?, ?)', t)
        conn.commit()
        print "... 유저 %s를 User 디비에 추가중" % x['user']['name']

    tweet_id = x['id']
    t = (tweet_id, )
    c.execute('select count(*) from tweets where id=?', t)
    count_tweets = c.fetchone()[0]

    print "... 트윗 디비를 검색중"

    if count_tweets == 0:
        print "... 아직 디비에 없어요."
        text = x['text']
        created_at = x['created_at']
        t = (tweet_id, text, created_at, user_id)
        c.execute('insert into tweets values(?, ?, ?, ?)', t)
        conn.commit()
        print '... %s 추가 중' % x['text']

        for n in kkma.nouns(x['text']):
            t = (user_id, n)
            c.execute('select count from user_nouns where user_id=? and noun=?', t)
            count_noun = c.fetchone()
            print count_noun

            print "... 명사 %s의 갯수는 %d" % (n, count_noun)

            if count_noun is None:
                #t = (user_id, n)
                c.execute('insert into user_nouns values(?, ?, 1)', t)
            else:
                c.execute('update user_nouns set count=count+1 where user_id=? and noun=?', t)
    else:
        print "... 이미 디비에 있어요. (그래도 명사를 분석하겠습니다.)"
        for n in kkma.nouns(x['text']):
            print "...... %s" % n

    i += 1
