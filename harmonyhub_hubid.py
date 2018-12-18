# -*- coding: utf-8 -*-

import requests
import json

hub_ip = '192.168.5.20'
hub_port = '8088'


# POST capture via Wireshark.
# This is from manually connecting to hub via iOS app
# ie, manually enter hub IP Address
#
#
#POST / HTTP/1.1
#Host: 192.168.5.20:8088
#Origin: http//:localhost.nebula.myharmony.com
#Accept-Charset: utf-8
#Content-Type: application/json
#Content-Length: 56
#Connection: keep-alive
#Accept: application/json
#User-Agent: Harmony_iOS_5.5_16
#Referer: http//:localhost.nebula.myharmony.com/mobile-fat.html
#Accept-Language: en-us
#Accept-Encoding: gzip, deflate

headers = {'Content-type': 'application/json', 'Accept': 'text/plain', 'Origin': 'http//:localhost.nebula.myharmony.com'}
r = requests.post('http://' + hub_ip + ':' + hub_port, json={"id": 124, "cmd": "connect.discoveryinfo?get", "params": {}}, headers=headers)

hub_data = json.loads(r.text)

hub_id = hub_data['data']['remoteId']
account_id = hub_data['data']['accountId']
print('Harmony Hub ID: ' + hub_id)
#print('Harmony Account ID: ' + account_id)
