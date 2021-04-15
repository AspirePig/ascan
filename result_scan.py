#!/usr/bin/python
# coding=utf-8
# python ascan.py filename  /  python ascan.py -f filename [解析的IP]

import nmap
import datetime
import threading
import requests
import chardet
import re
import json
import os
requests.packages.urllib3.disable_warnings()
import Queue
from IPy import IP
import sys



final_domains = []
ports = []

class PortScan(threading.Thread):
    def __init__(self, queue):
        threading.Thread.__init__(self)
        self._queue = queue
        self.count_all = queue.qsize()

    def run(self):
        while not self._queue.empty():
            scan_ip = self._queue.get()
            try:
                masscan_ports = portscan(scan_ip)
                if len(masscan_ports) > 0:
                    print '当前扫描IP：{},扫描端口：{}'.format(scan_ip, ",".join(masscan_ports))
                    Scan(scan_ip,masscan_ports)
                else:
                    print '当前扫描IP：{},无端口，自动跳过'.format(scan_ip)
            except Exception as e:
                print e
                pass
            print '--***************** 剩余目标：{}个  总计：{}个 ***************--'.format(self._queue.qsize(),self.count_all)

#调用masscan
def portscan(scan_ip):
    temp_ports = []
    with open('{}.list'.format(scan_ip), 'r') as f:
        for line in f:
            if "open" in line:
                _ = line.split()
                temp_ports.append(str(_[2]))

    if len(temp_ports) > 60:
        return []       #如果端口数量大于50，说明可能存在防火墙，属于误报，清空列表
    else:
        return temp_ports #小于50则放到总端口列表里


#调用nmap识别服务
def Scan(scan_ip,masscan_ports):
    nm = nmap.PortScanner()
    try:
        scan_result = nm.scan(scan_ip, ",".join(masscan_ports), arguments='-Pn -sV --open')
        tcp_result = scan_result.get('scan').get(scan_ip).get('tcp')
        for port,portinfo in tcp_result.items():
            if portinfo.get('state') == "open":
                service_name = portinfo.get('name').strip()
                product = portinfo.get('product').strip()
                version = portinfo.get('version').strip()
                extrainfo = portinfo.get('extrainfo').strip()
                print '[*]主机 {} 的 {} 端口服务：{},产品：{},版本：{},额外信息：{}'.format( scan_ip, port, service_name, product, version, extrainfo)
                if 'http' in service_name  or service_name == 'sun-answerbook':
                    if service_name == 'https' or service_name == 'https-alt':
                        scan_url_port = 'https://' + scan_ip + ':' + str(port)
                    else:
                        scan_url_port = 'http://' + scan_ip + ':' + str(port)
                    final_domains.append(",".join([scan_url_port,service_name, product, version, extrainfo]))
                else:
                    final_domains.append(",".join([scan_ip+':'+str(port),service_name, product, version, extrainfo]))
    except Exception as e:
       print e
       pass

#启用多线程扫描
def main():
    queue = Queue.Queue()
    targets= []
    try:
        filelist = os.listdir(".")
        for filename in filelist:
            if "list" in filename:
                ip = filename.replace(".list","")
                targets.append(ip)
        for line in targets:
            queue.put(line)

        threads = []
        thread_count = 10
        for i in range(thread_count):
            threads.append(PortScan(queue))
        for t in threads:
            t.start()
        for t in threads:
            t.join()
    except Exception as e:
        print e
        pass


if __name__ =='__main__':
    start_time = datetime.datetime.now()
    main()
    final_domains = list(set(final_domains))
    with open(r'scan_url_port.csv', 'ab+') as ff:
        ff.write('\n'.join(final_domains))
    spend_time = (datetime.datetime.now() - start_time).seconds
    print '程序共运行了： ' + str(spend_time) + '秒'
