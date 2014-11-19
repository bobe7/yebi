# -*- coding: utf-8 -*-
import os
import sys
import time

reload(sys)
sys.setdefaultencoding('utf-8')

while 1:
    print "크롤러를 수행합니다."
    for x in range(10):
        n1 = x + 1
        n2 = 11 - n1
        print "%s%s 크롤러를 준비합니다." % ("*" * n1, " " * n2)
        time.sleep(0.3)

    print "\n"
    os.system('python crawler.py')
    sec = 30 * 60.0

    if sec > 60:
        print "\n약 %d 분간 쉬겠습니다." % int(sec / 60)
    else:
        print "\n약 %d 초간 쉬겠습니다." % int(sec)

    homeplus = 0

    range_number = 50
    for x in range(range_number):
        tick = sec / range_number
        time.sleep(tick)
        n1 = x + 1
        n2 = range_number + 1 - n1
        homeplus = homeplus + tick
        print "%s%s 약 %d초" % ("*" * n2, " " * n1,  int(homeplus))