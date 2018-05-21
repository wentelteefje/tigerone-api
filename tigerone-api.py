#!/usr/bin/env python

import mysql.connector as mariadb
import socket
import json

# establish mysql db connection
mariadb_connection = mariadb.connect(user='mgiapi', password='INV.api', database='MMU3')
cursor = mariadb_connection.cursor()

# Import IPs from hosts file
host = []
for line in open('/home/user/tigerone-api/hosts'):
#for line in open('hosts'):
    host.append(line)

# Set claymore API parameters
TCP_PORT = 3333
BUFFER_SIZE = 1024
msg = "{\"id\":0,\"jsonrpc\":\"2.0\",\"method\":\"miner_getstat1\"}"

for TCP_IP in host:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
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
        active = 1
        # write to db
        try:
            cursor.execute("REPLACE INTO stats (IP,NETHASH,HASHES,TEMPSFANS,ACTIVE) VALUES (%s,%s,%s,%s,%s)", (TCP_IP, nethash, hashes, tempsfans, active))
        except mariadb.Error as error:
            print("Error: {}".format(error))
        mariadb_connection.commit()
    except socket.error:
        # Catch error
        nethash = "0"
        hashes = "0"
        tempsfans = "0"
        active = 0
        #cursor.execute("UPDATE stats SET ACTIVE = "N" WHERE IP = %s", TCP_IP)
        try:
            cursor.execute("REPLACE INTO stats (IP,NETHASH,HASHES,TEMPSFANS,ACTIVE) VALUES (%s,%s,%s,%s,%s)", (TCP_IP, nethash, hashes, tempsfans, active))
        except mariadb.Error as error:
            print("Error: {}".format(error))
    finally:
        s.close()
