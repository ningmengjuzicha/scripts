import threading
import os
import platform
import subprocess
import sys
import datetime

error_info = 'Error: Unable to establish IPMI'
ipmi_cmd = 'ipmitool -H {} -U jdroot -P JCss%6!8 -I lanplus chassis power status'

# jdroot JCss%6!8

def power_status_parse(ip_0, ip_1, status_list):
    # print('into parse -------------------------------')
    ip = ip_0 + ip_1
    cmd = ipmi_cmd.format(ip)
    p = subprocess.Popen(cmd, stderr=subprocess.PIPE, stdout=subprocess.PIPE, shell=True)
    result = p.communicate()
    if result[1]:
        # status_list.append({ip: None})
        return
    elif error_info in result[0].decode('utf8'):
        # status_list.append({ip: None})
        return
    status_list.update({ip: result[0].decode('utf8').split(' ')[-1].strip()})
    return


def call_ipmi(ip_0):
    # print('into call ipmi------------------- ')
    power_status_dict = {}
    os_version = platform.system()
    thread_count = 1000
    if 'Windows' in os_version:
        thread_count = int(os.environ['NUMBER_OF_PROCESSORS'])*4

    # print(thread_count)
    for index in range(1, 256, thread_count):
        thread_list = []
        final_val = index+thread_count
        if final_val > 256:
            final_val = 256
        range_list = list(range(index, final_val))
        # print(range_list)
        for i in range_list:
            t = threading.Thread(target=power_status_parse, args=(ip_0, str(i), power_status_dict))
            t.setDaemon(True)
            thread_list.append(t)
        for thread in thread_list:
            thread.start()
        for thread in thread_list:
            thread.join()
    return power_status_dict


if __name__ == '__main__':
    ip_0 = '172.22.27.'
    if len(sys.argv) == 2:
        ip_0 = sys.argv[1]
    if not ip_0.endswith('.'):
        ip_0 = ip_0 + '.'
    start_time = datetime.datetime.now()
    power_status = call_ipmi(ip_0)
    end_time = datetime.datetime.now()
    diff_time = end_time - start_time
    print('Total time : {}'. format(diff_time.seconds))
    print('Got ' + str(len(power_status)) + ' bmc ip')
    # power_status = sorted(power_status, lambda x: x.values())
    after_sorted = sorted(power_status.items(), key=lambda v: v[1])
    [print(x) for x in after_sorted]

