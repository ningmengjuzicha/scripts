#!/usr/bin/python
#-*- coding:gb18030 -*-
'''

#�ж��ļ��е�ip�Ƿ���pingͨ�����ҽ�ͨ�벻ͨ��ip�ֱ�д�������ļ���
#�ļ��е�ipһ��һ��
'''
import time,os
import time
import subprocess
import threading
import datetime


ping_cmd = "ping -n 2 -w 1 {}"

#def exe_ping(count_True,count_False,ip_True,ip_False,ip):
def exe_ping(ip,thread_list):
    #print("enter")
    cmd = ping_cmd.format(ip)
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    stdout,stderr = p.communicate()
    if p.returncode == 0:
        print('ping %s is ok'%ip)
        #ip_True.write(ip)  #��pingͨ��ipд��ip_True.txt��
    else:
        print('ping %s is fail'%ip)
        #ip_False.write(ip)  #��ping��ͨ��д��ip_False.txt��

    return
    

def ping_Test():
    #ips=open('host.csv','r')
    data=['10.67.48.71','10.67.48.65','10.67.48.66','10.67.48.85']
    thread_list = []
    #ip_True = open('ip_True.csv','w')
    #ip_False = open('ip_False.csv','w')
    #count_True,count_False=0,0
    # for ip in ips.readlines():
        # data.append(ip.strip())
    for i in data:
            #t = threading.Thread(target=exe_ping, args=(count_True,count_False,ip_True,ip_False,i))
            t = threading.Thread(target=exe_ping, args=(i,thread_list))
            t.setDaemon(True)
            thread_list.append(t)
    #print("thread_list:",thread_list)
    for thread in thread_list:
        thread.start()
    for thread in thread_list:
        thread.join()
    # ip_True.close()
    # ip_False.close()
    # ips.close()
    
if __name__ == '__main__':  
    start_time = datetime.datetime.now()
    ping_Test()
    end_time = datetime.datetime.now()
    diff_time = end_time - start_time
    print('Total time : {}'. format(diff_time.seconds))    

