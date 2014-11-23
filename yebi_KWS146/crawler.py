# -*- coding: utf-8 -*-
import sqlite3 # DB접속 라이브러리
import sys
from konlpy.tag import Kkma
from fetcher import *


class Crawler:
    def __init__(self):
        self.kkma = Kkma()
        self.conn = sqlite3.connect('yebi.db')
        self.cursor = self.conn.cursor()
        self.count = 20

        reload(sys)
        sys.setdefaultencoding('utf-8')

    def do(self):
        print '트위터 타임라인 탐색 중.'

        for x in TwitterFetcher().get_time_line(self.count):
            user_id = x['user']['id']
            print ''
            print '=' * 80
            print '... @%s: %s' % (x['user']['name'],  x['text'])

            t = (user_id, )
            self.cursor.execute('select count(*) from users where id=?', t)
            count_user = self.cursor.fetchone()[0]

            if count_user == 0: #DB안에 User가 없으면 ( 0 )
                name = x['user']['name']
                screen_name = x['user']['screen_name']
                profile_image = x['user']['profile_image_url_https']
                t = (user_id, name, screen_name, profile_image)
                self.cursor.execute('insert into users values(?, ?, ?, ?)', t)
                self.conn.commit()
                print "... 유저 %s를 User 디비에 추가중" % x['user']['name']

            i = 1

            tweet_id = x['id']
            t = (tweet_id, )
            self.cursor.execute('select count(*) from tweets where id=?', t)
            count_tweets = self.cursor.fetchone()[0]

            print "... 트윗 디비를 검색중"

            if count_tweets == 0:
                print "... 아직 디비에 없어요."
                text = x['text']
                created_at = x['created_at']
                t = (tweet_id, text, created_at, user_id)
                self.cursor.execute('insert into tweets values(?, ?, ?, ?)', t)
                self.conn.commit()
                print '... %s 추가 중' % x['text']

                for n in self.kkma.nouns(x['text']):
                    t = (user_id, n)
                    self.cursor.execute('select count from user_nouns where user_id=? and noun=?', t)
                    count_noun = self.cursor.fetchone()

                    screen_name = x['user']['screen_name']
                    if count_noun is not None:
                        print "... %s가 명사 \"%s\"의 갯수는 %d회 사용하였습니다." % \
                              (screen_name, n, count_noun[0])

                    if count_noun is None:
                        print "... %s가 명사 \"%s\"를 처음 사용하였습니다." % (screen_name, n)
                        #t = (user_id, n)
                        self.cursor.execute('insert into user_nouns values(?, ?, 1)', t)
                    else:
                        self.cursor.execute('update user_nouns set count=count+1 where user_id=? and noun=?',
                                            t)
            else:
                print "... 이미 디비에 있어요. (그래도 명사를 분석하겠습니다.)"
                for n in self.kkma.nouns(x['text']):
                #     print "...... %s" % n
                    t = (user_id, n)
                    self.cursor.execute('select count from user_nouns where user_id=? and noun=?', t)
                    count_noun = self.cursor.fetchone()

                    screen_name = x['user']['screen_name']
                    if count_noun is not None:
                        print "... %s가 명사 \"%s\"의 갯수는 %d회 사용하였습니다." \
                              % (screen_name, n, count_noun[0])

            i += 1


if __name__ == "__main__":
    crawler = Crawler()
    crawler.do()
