#!/usr/bin/env python

import time
import json
import requests
import pika
import sys
import os

class Reciever:
	RABBITMQ_HOST = 'candidatemq.n2g-dev.net'
    RABBITMQ_USERNAME = 'cand_x54e'
    RABBITMQ_PASSWORD = 'yoVFkPewBfu2Mmgf'
    RABBITMQ_EXCHANGE = 'cand_x54e'
    RABBITMQ_VHOST = '/'
    RABBITMQ_QUEUE = 'cand_x54e_results'
    LOOP_RATE = 10

    def __init__(self):
	    self._rabbit_conn = None
	    self._rabbit_ch = None
	    self._connect_rabbit()

	def _connect_rabbit(self):
		creds=pika.PlainCredentials(self.RABBITMQ_USERNAME,
									self.RABBITMQ_PASSWORD)
		self._rabbit_conn=pika.BlockingConnection(
			pika.ConnectionParameters(host=RABBITMQ_HOST,
									  credentials=creds,
									  virtual_host=self.RABBITMQ_VHOST)
		)
		self._rabbit_ch = self._rabbit_conn.channel()
