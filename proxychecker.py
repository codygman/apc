import httplib2
from httplib2 import ServerNotFoundError
import socks
from httplib2.socks import GeneralProxyError
import threading
import Queue
import time
import os

#httplib2.debuglevel=4

queue = Queue.Queue()

class ThreadProxy(threading.Thread):
    """Threaded proxy checker"""
    def __init__(self, queue):
        threading.Thread.__init__(self)
        self.queue = queue

    def run(self):
        while True:
            proxy = self.queue.get()
            self.test_proxy(proxy)
            self.queue.task_done()

    def test_proxy(self, proxy):
        url = 'http://checker.samair.ru'
        server, port = proxy.split(':')   
        port = int(port)
        response = ""
        try:
            h = httplib2.Http(proxy_info = httplib2.ProxyInfo(socks.PROXY_TYPE_SOCKS5, server, port), timeout=5)
            r,c = h.request(url)
            html_page = c
        except AttributeError:
# HttpLib2 likes to throw an attribute error when you give it the wrong type of socks proxy or it just can't connect
            print proxy + " is bad (Couldn't connect)"
            return "bad"
        except GeneralProxyError:
            print "socks general proxy error"
        except ServerNotFoundError:
            print proxy + ' is bad (server not found)'
            return "bad"
        else: 
            if server in html_page:
                print proxy + " is good"
                good_proxies.append(proxy)
                pass
            else:
                print proxy + ' is not anonymous'
                pass

     


with open('untested-proxies/proxylist.txt', 'r') as f:
    file_contents = f.read()

proxies = file_contents.split()
good_proxies = []

print 'There are %i proxies' % len(proxies)

def main():
    for i in range(9):
        t = ThreadProxy(queue)
        t.setDaemon(True)
        t.start()

    for proxy in proxies:
        queue.put(proxy)

    queue.join()

main()

all_good_proxies = ""
print '\n\n\n\nGood Proxies:'

for proxy in good_proxies:
    print proxy
    all_good_proxies += proxy + os.linesep

with open('good-proxies/proxies.txt', 'a') as f:
    f.write(all_good_proxies)
    f.close()
