import socket
import pymongo
import requests
import ftplib
from tqdm import tqdm
import MySQLdb
import cx_Oracle
import psycopg2
import binascii
import sys
from concurrent.futures import ThreadPoolExecutor


passwd = ['123456','admin','root','password','123123','123','1','','{user}',
          '{user}{user}','{user}1','{user}123','{user}2016','{user}2015',
          '{user}!','P@ssw0rd!!','qwa123','12345678','test','123qwe!@#',
          '123456789','123321','1314520','666666','woaini','fuckyou','000000',
          '1234567890','8888888','qwerty','1qaz2wsx','abc123','abc123456',
          '1q2w3e4r','123qwe','159357','p@ssw0rd','p@55w0rd','password!',
          'p@ssw0rd!','password1','r00t','system','111111','admin']


oracle_user = ['sys','system','sysman','scott','aqadm','Dbsnmp']
oracle_pass_default = ['','manager','oem_temp','tiger','aqadm','dbsnmp']

data = '0200020000000000123456789000000000000000000000000000000000000000000000000000ZZ5440000000000000000000000000000000000000000000000000000000000X3360000000000000000000000000000000000000000000000000000000000Y373933340000000000000000000000000000000000000000000000000000040301060a09010000000002000000000070796d7373716c000000000000000000000000000000000000000000000007123456789000000000000000000000000000000000000000000000000000ZZ3360000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000Y0402000044422d4c6962726172790a00000000000d1175735f656e676c69736800000000000000000000000000000201004c000000000000000000000a000000000000000000000000000069736f5f31000000000000000000000000000000000000000000000000000501353132000000030000000000000000'


def IsOpen(ip,port):
    s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    try:
        s.connect((ip,int(port)))
        s.shutdown(2)
        return True
    except:
        return False

def redis(ip, port = 6379):
    try:
        socket.setdefaulttimeout(5)
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((ip, int(port)))
        s.send(bytes("INFO\r\n", 'UTF-8'))
        result = s.recv(1024).decode()
        if "redis_version" in result:
            print(ip + ":6379 redis?????????")
        s.close()
    except Exception as e:
        pass
    finally:
        bar.update(1)

def mongodb(ip, port = 27017):
    try:
        conn = pymongo.MongoClient(ip, port, socketTimeoutMS=4000)
        dbname = conn.list_database_names()
        print(ip + ":27017 mongodb?????????")
        conn.close()
    except Exception as e:
        pass
    finally:
        bar.update(1)

def memcached(ip, port = 11211):
    try:
        socket.setdefaulttimeout(5)
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((ip, int(port)))
        s.send(bytes('stats\r\n', 'UTF-8'))
        if 'version' in s.recv(1024).decode():
            print(ip + ":11211 memcached?????????")
        s.close()
    except Exception as e:
        pass
    finally:
        bar.update(1)

def elasticsearch(ip, port = 11211):
    try:
        url = 'http://' + ip + ':9200/_cat'
        r = requests.get(url, timeout=5)
        if '/_cat/master' in r.content.decode():
            print(ip + ":9200 elasticsearch?????????")
    except Exception as e:
        pass
    finally:
        bar.update(1)

def zookeeper(ip, port = 2181):
    try:
        socket.setdefaulttimeout(5)
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((ip, int(port)))
        s.send(bytes('envi', 'UTF-8'))
        data = s.recv(1024).decode()
        s.close()
        if 'Environment' in data:
            print(ip + ":2181 zookeeper?????????")
    except:
        pass
    finally:
        bar.update(1)

def ftp(ip, port = 21):
    try:
        ftp = ftplib.FTP.connect(ip,port,timeout=5)
        ftp.login('anonymous', 'Aa@12345678')
        print(ip + ":21 FTP?????????")
    except Exception as e:
        pass
    finally:
        bar.update(1)

def CouchDB(ip, port = 5984):
    try:
        url = 'http://' + ip + ':5984'+'/_utils/'
        r = requests.get(url, timeout=5)
        if 'couchdb-logo' in r.content.decode():
            print(ip + ":5984 CouchDB?????????")
    except Exception as e:
        pass
    finally:
        bar.update(1)

def docker(ip, port = 2375):
    try:
        url = 'http://' + ip + ':2375'+'/version'
        r = requests.get(url, timeout=5)
        if 'ApiVersion' in r.content.decode():
            print(ip + ":2375 docker api?????????")
    except Exception as e:
        pass
    finally:
        bar.update(1)

def Hadoop(ip, port = 50070):
    try:
        url = 'http://' + ip + ':50070'+'/dfshealth.html'
        r = requests.get(url, timeout=5)
        if 'hadoop.css' in r.content.decode():
            print(ip + ":50070 Hadoop?????????")
    except Exception as e:
        pass
    finally:
        bar.update(1)

def mysql(ip, port = 3306):
    bar.update(1)
    if IsOpen(ip, port):
        for pwd in passwd:
            try:
                pwd = pwd.replace('{user}', 'root')
                conn = MySQLdb.connect(ip, port = port, user = 'root', passwd = pwd, db = 'mysql')
                print('{}:3306  Mysql???????????????: root  {}'.format( ip, pwd))
                conn.close()
                break
            except Exception as e:
                pass
                

def mssql(ip, port = 1433):
    bar.update(1)
    if IsOpen(ip, port):
        for pwd in passwd:
            try:
                pwd = pwd.replace('{user}', 'sa')
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.connect((ip, port))
                husername = binascii.b2a_hex('sa')
                lusername = len('sa')
                lpassword = len(pwd)
                hpwd = binascii.b2a_hex(pwd)
                address = binascii.b2a_hex(ip) +'3a'+ binascii.b2a_hex(str(port))
                data1 = data.replace(data[16:16+len(address)], address)
                data2 = data1.replace(data1[78:78+len(husername)], husername)
                data3 = data2.replace(data2[140:140+len(hpwd)], hpwd)
                if lusername >= 16:
                    data4 = data3.replace('0X', str(hex(lusername)).replace('0x', ''))
                else:
                    data4 = data3.replace('X', str(hex(lusername)).replace('0x', ''))
                if lpassword >= 16:
                    data5 = data4.replace('0Y', str(hex(lpassword)).replace('0x', ''))
                else:
                    data5 = data4.replace('Y', str(hex(lpassword)).replace('0x', ''))
                hladd = hex(len(ip) + len(str(port))+1).replace('0x', '')
                data6 = data5.replace('ZZ', str(hladd))
                data7 = binascii.a2b_hex(data6)
                s.send(data7)
                if 'master' in s.recv(1024):
                    print('{}:1433  SQLserver???????????????: sa  {}'.format(ip, pwd))
                    break
            except Exception as e:
                pass    

def oracle(ip, port = 1521):
    bar.update(1)
    if IsOpen(ip, port):
        for i in range(1, len(oracle_user)):
            try:
                user = oracle_user[i]
                pwd  = oracle_pass_default[i]
                conn = cx_Oracle.connect(user, pwd, ip+':{}/orcl'.format(port))
                print('{}:1521  Oracle???????????????: {} {}'.format(ip, user, pwd))
                conn.close()
            except Exception as e:
                pass
        for pwd in passwd:
            try:
                pwd = pwd.replace('{user}', 'sys')
                conn = cx_Oracle.connect('sys', pwd, ip+':1521/orcl')
                print('{}:1521  Oracle???????????????: sys {}{}'.format( ip, pwd))
                conn.close()
                break
            except Exception as e:
                pass

def postgresql(ip, port = 5432):
    bar.update(1)
    if IsOpen(ip, port):
        for pwd in passwd:
            try:
                pwd = pwd.replace('{user}', 'postgres')
                conn = psycopg2.connect(host=ip, port=port, user='postgres', password=pwd)
                print('{}:5432  Postgresql???????????????: postgres  {}'.format( ip, pwd))
                conn.close()
                break
            except Exception as e:
                pass



if __name__ == '__main__':
    if len(sys.argv) == 1:
        print("Usage:python3 unauthorized-check.py url.txt")
    file = sys.argv[1]
    with open(file, "r", encoding='UTF-8') as f:
        line = [i for i in f.readlines()]
        line = list(set(line))
    bar = tqdm(total=len(line)*13)
    with ThreadPoolExecutor(100) as pool:
        for target in line:
            target=target.strip()
            pool.submit(redis, target)
            pool.submit(Hadoop, target)
            pool.submit(docker, target)
            pool.submit(CouchDB, target)
            pool.submit(ftp, target)
            pool.submit(zookeeper, target)
            pool.submit(elasticsearch, target)
            pool.submit(memcached, target)
            pool.submit(mongodb, target)
            pool.submit(mysql, target)
            pool.submit(mssql, target)
            pool.submit(oracle, target)
            pool.submit(postgresql, target)