import urllib2
import time

start_time = time.time()
for x in range(100):
    print time.time() - start_time, "seconds"
    print urllib2.urlopen("http://fa2png.io/generate?name=play&size=32%s&color=000000").read()
