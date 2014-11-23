# -*- coding: utf-8 -*-
import sqlite3
import sys


reload(sys)
sys.setdefaultencoding('utf-8')

conn = sqlite3.connect('yebi.db')
cursor = conn.cursor()

cursor.execute('select * from users')
users = cursor.fetchall()

for user in users:
    user_id = user[0]
    screen_name = user[1]
    tweet_id = user[2]
    url = user[3]
    print "%s(@%s)가 쓴 트윗입니다." % (screen_name, tweet_id)
    print "url: %s" % url
    print "=" * 60

    t = (user_id, )

    cursor.execute('select * from tweets where user_id=?', t)
    tweets = cursor.fetchall()

    for tweet in tweets:
        tweet_text = tweet[1]
        created_at = tweet[2]
        print "%s(@%s): %s\n작성일: %s\n" % (screen_name, tweet_id, tweet_text, created_at)

    cursor.execute("select * from user_nouns where user_id=?", t)
    user_nouns = cursor.fetchall()

    for user_noun in user_nouns:
        noun = user_noun[1]
        noun_count = user_noun[2]
        print "%s(@%s)님의 트윗에서 명사 \"%s\"가 %d회 나왔습니다." % (screen_name, tweet_id, noun, noun_count)

    print "=" * 60
    print "\n\n"
