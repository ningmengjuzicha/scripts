import socket
import sys
import datetime
from time import sleep
import threading
import platform





def ping(host, ips, timeout=3):
    # safe port:443, unsafe port:80
    ports = [623]
    for port in ports:
        try:
            socket.setdefaulttimeout(timeout)
            socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect((host, port))
        except Exception as e:
            return
    # print('host : ', host)
    ips.append(host)
    # return host


def parallel(action, host):
    hosts = [host+str(i) for i in range(1,256)]
    ips = []
    thread_list = []
    for host in hosts:
        t = threading.Thread(target=action, args=(host, ips))
        t.setDaemon(True)
        thread_list.append(t)
    for thread in thread_list:
        thread.start()
    for thread in thread_list:
        thread.join()
    return ips

def main(host):
    ips = parallel(ping, host)
    return ips

if __name__ == '__main__':
    ip_0 = '172.22.27.'
    if len(sys.argv) == 2:
        ip_0 = sys.argv[1]
    if not ip_0.endswith('.'):
        ip_0 = ip_0 + '.'
    start_time = datetime.datetime.now()
    ips = main(ip_0)
    end_time = datetime.datetime.now()
    diff_time = end_time - start_time    
    print(str(diff_time.seconds) + "s" + ' Found ' + str(len(ips)) + ' BMC IP ')
    [print(x) for x in ips]

