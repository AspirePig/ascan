安装库
apt install masscan nmap -y
yum install masscan nmap -y
pip2 install python-nmap requests IPy

使用方法：
1.单行单个IP的文件
python2  ascan.py  [ip.txt]

2.子域名爆破域名，再做dns解析的结果文件  如  
baidu.com 39.156.69.79,220.181.38.148
python2  ascan.py -f [ip.txt]

result_scan.py   nmap结果复核脚本
domain2ip  批量域名解析IP



db-check.py 支持 mysql、mssql、oracle、postgresql、redis、mongodb、memcached、elasticsearch、zookeeper、ftp、CouchDB、docker、Hadoop

