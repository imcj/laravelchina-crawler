#!/usr/bin/env python

import os
import sys
import urllib
import base64
from time import sleep, time

i = 1
traffic = 0
monitor = time()
monitor_traffic = 0
M = 1024 * 1024
K = 1024
limit = 1024 * K
exceptionIndex = 0
# supervisord except exit code 0,2
# http://supervisord.org/configuration.html
os.mkdir('mkdir -p data/pages')
while True:
    url = "https://laravel-china.org/topics/%d" % i

    t1 = time()
    try:
        fd = urllib.urlopen(url)
        content = fd.read()
    except Exception, e:
        exceptionIndex += 1
        print e

    downloadDuration = time() - t1
    print "Download duration %s %.6f" % (url, downloadDuration)

    if fd.getcode() > 299 or fd.getcode() < 200:
        print "%d %s" % (fd.getcode(), url)
        exceptionIndex += 1

    wfd = open("data/pages/%s" % (base64.urlsafe_b64encode(url)), "w")
    wfd.write(content)
    wfd.close()

    traffic += len(content)
    monitor_traffic += len(content)
    monitor_duration = time() - monitor
    per_second = monitor_traffic / monitor_duration
    if monitor_duration > 2:
        excepted = monitor_duration * limit
        actual = monitor_traffic
        overflow = actual - excepted
        print "Excepted %.2f Actual %.2f Overflow %.2f Per second %.2f" %\
            (excepted / K, actual / K, overflow / K, per_second / K)
        if overflow > 0:
            sleepSecond = overflow / limit
            print "Per second over flow sleep %.2f" % sleepSecond
            sleep(sleepSecond)

        monitor_traffic = 0
        monitor = time()
    

    if exceptionIndex > 1000:
        sys.exit(1)
    i += 1