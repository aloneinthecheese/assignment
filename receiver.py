#!/usr/bin/env python

import time
import json
import requests
import pika
import sys
import os
import MySQLdb
import mysql.connector
from mysql.connector import Error, errorcode

#DATABSE_URI='mysql+mysqlconnector://{user}:{password}@{server}/{database}'.format(user='root', password='1312', server='localhost', database='test_db')

#con=MySQLdb.connect(host='localhost', user='root', passwd='1312', db='test_db')


class Receiver:
    RABBITMQ_HOST = 'candidatemq.n2g-dev.net'
    RABBITMQ_USERNAME = 'cand_x54e'
    RABBITMQ_PASSWORD = ''
    RABBITMQ_EXCHANGE = 'cand_x54e'
    RABBITMQ_VHOST = '/'
    RABBITMQ_QUEUE = 'cand_x54e_results'
    LOOP_RATE = 10
    DB_HOST = 'candidaterds.n2g-dev.net'
    DB_USERNAME = 'cand_x54e'
    DB_PASSWORD = ''
    DB_NAME = 'cand_x54e'


    def __init__(self):
        """__init__.
        """
        self._rabbit_conn = None
        self._rabbit_ch = None
        self._connect_rabbit()

    def _connect_rabbit(self):
        """_connect_rabbit.
        """
        creds=pika.PlainCredentials(self.RABBITMQ_USERNAME, self.RABBITMQ_PASSWORD)
        self._rabbit_conn=pika.BlockingConnection(
            pika.ConnectionParameters(
                host=self.RABBITMQ_HOST,
                credentials=creds,
                virtual_host=self.RABBITMQ_VHOST)
        )
        self._rabbit_ch = self._rabbit_conn.channel()

    def callback(self, ch, method, properties, body):
        """callback.

        Args:
            ch:
            method:
            properties:
            body:
        """
        payload = body.decode()
        data = json.loads(payload)
        rkey = method.routing_key
        _t = rkey.split('.')
        store = {
            'gateway_eui': int(_t[0].replace('<', '').replace('>', '')),
            'profile_id': int(_t[1].replace('<', '').replace('>', '')),
            'endpoint_id': int(_t[2].replace('<', '').replace('>', '')),
            'cluster_id': int(_t[3].replace('<', '').replace('>', '')),
            'attribute_id': int(_t[4].replace('<', '').replace('>', '')),
            'value': data['value'],
            'timestamp': data['timestamp']
        }   #string manipulation to split data
        print(f"[x] Received data at the topic <{rkey}> : {data}") 
        # self.connect_db(store) #Connect to db to store data

    def run_forever(self):
        """run_forever.
        """
        self.receive_from_queue()

    def receive_from_queue(self):
        """receive data from queue
        """
        print(f'[*] - receiving data')
        # Receive messages from queue
        self._rabbit_ch.basic_consume(queue=self.RABBITMQ_QUEUE,
                                      on_message_callback=self.callback)
        self._rabbit_ch.start_consuming()

    def push_data_db(self, store):
        """insert data to db
        """
        query="INSERT INTO data(value, timestamp)"\
              "VALUES(%s, %s, %s, %s, %s, %s)"      #insert query
        try:
            cursor.execute(query, store)
            if cursor.lastrowid:
                print('last insert id', cursor.lastrowid)
            else:
                print('last insert id not found')
            conn.commit()
        except Error as error:
            print(error)

    def connect_db(self, store):
        """if self._db_con.is_connected():  #if connection already open, then dont attempt another connection
            print('\n Already connected, pushing to db...')
            self.push_data_db(data)
        else:"""
        try:
            self.db_con = mysql.connector.connect(host='candidaterds.n2g-dev.net', database='cand_x54e', user='cand_x54e', password='yoVFkPewBfu2Mmgf', ssl_disabled = True)
            if self._db_con.is_connected():
                print('[*] - Connected to MySQL database!')
            cursor=connection.cursor()
            push_data_db(store)
        except mysql.connector.Error as error:
            print("Failed to connect. {}".format(error))

if __name__ == '__main__':
    try:
        receiver = Receiver()
        receiver.run_forever()
    except KeyboardInterrupt:
        print('\nInterrupted')
        #cursor.close()  #close cursor
        #connection.close()    #close connection to db
        #print('\nConnection to db is closed :)')
    try:
        sys.exit(0)
    except SystemExit:
        os._exit(0)
