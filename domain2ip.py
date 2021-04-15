import dns.resolver
import sys
from IPy import IP

def domain2ip(domain):
    #print(domain.strip(), end=" ")
    A = dns.resolver.query(qname=domain.strip(),rdtype='A',raise_on_no_answer=False,lifetime=3)
    result = []
    for i in A.response.answer:
        for j in i.items:
            print(str(j))
            result.append(str(j).strip("."))
    #print("/".join(result))


if __name__ == "__main__":
    if len(sys.argv) == 2:
        domain2ip(sys.argv[1])
    elif len(sys.argv) == 3 and sys.argv[1] == "-f":
        with open(sys.argv[2],"r") as f:
            for domain in f.readlines():
                try:
                    domain2ip(domain)
                except:
                    continue
    else:
        notice = """Usage: 
        1. python3 domain2ip.py baidu.com
        2. python3 domain2ip.py -f domain.txt"""
        print(notice)
