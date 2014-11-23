# -*- coding: utf-8 -*-
import sys
import time
import crawler


reload(sys)
sys.setdefaultencoding('utf-8')

c = crawler.Crawler()

while 1:
    print "크롤러를 수행합니다."
    for x in range(10):
        n1 = x + 1
        n2 = 11 - n1
        print "%s%s 크롤러를 준비합니다." % ("*" * n1, " " * n2)
        time.sleep(0.3)

    print "\n"
    c.do()

    sec = 30 * 60.0

    if sec > 60:
        print "\n약 %d 분간 쉬겠습니다." % int(sec / 60)
    else:
        print "\n약 %d 초간 쉬겠습니다." % int(sec)

    total_tick = 0
    range_number = 50
    for x in range(range_number):
        tick = sec / range_number
        time.sleep(tick)
        n1 = x + 1
        n2 = range_number + 1 - n1
        total_tick = total_tick + tick
        print "%s%s 약 %d초" % ("*" * n2, " " * n1,  int(total_tick))