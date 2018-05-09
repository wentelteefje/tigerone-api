#!/usr/bin/env python

import mysql.connector as mariadb
import socket
import json

# establish mysql db connection
mariadb_connection = mariadb.connect(user='mgiapi', password='INV.api', database='MMU3')
cursor = mariadb_connection.cursor()

# Import IPs from hosts file
host = []
for line in open('hosts'):
    host.append(line)

# Set claymore API parameters
TCP_PORT = 3333
BUFFER_SIZE = 1024
msg = "{\"id\":0,\"jsonrpc\":\"2.0\",\"method\":\"miner_getstat1\"}"

for TCP_IP in host:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((TCP_IP, TCP_PORT))
    s.sendall(msg.encode('utf-8'))
    data = s.recv(BUFFER_SIZE).decode('utf-8')
    jdata = json.loads(data)

    nethash = str(data).split()[7]
    hashes = str(data).split()[8]
    tempsfans = str(data).split()[11]

    nethash = nethash.replace(";", " ")
    hashes = hashes.replace(";", " ")
    tempsfans = tempsfans.replace(";", " ")
    s.close()

    # write to db
    cursor.execute("REPLACE INTO stats (IP,NETHASH,HASHES,TEMPSFANS) VALUES (%s,%s,%s,%s)", (TCP_IP, nethash, hashes, tempsfans))

    mariadb_connection.commit()

#print(nethash, hashes, tempsfans)
