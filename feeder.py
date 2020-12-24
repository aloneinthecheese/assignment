#!/usr/bin/env python

import time
import json
import requests
import pika
import sys
import os


class Feeder:
    API_RESULTS_URL = \
        'https://a831bqiv1d.execute-api.eu-west-1.amazonaws.com/dev/results'
    RABBITMQ_HOST = 'candidatemq.n2g-dev.net'
    RABBITMQ_USERNAME = 'cand_x54e'
    RABBITMQ_PASSWORD = ''
    RABBITMQ_EXCHANGE = 'cand_x54e'
    RABBITMQ_VHOST = '/'
    LOOP_RATE = 10

    def __init__(self):
        self._rabbit_conn = None
        self._rabbit_ch = None

        self._connect_rabbit()

    def _connect_rabbit(self):
        creds = pika.PlainCredentials(self.RABBITMQ_USERNAME,
                                      self.RABBITMQ_PASSWORD)
        self._rabbit_conn = pika.BlockingConnection(
            pika.ConnectionParameters(host=self.RABBITMQ_HOST,
                                      credentials=creds,
                                      virtual_host=self.RABBITMQ_VHOST)
        )
        self._rabbit_ch = self._rabbit_conn.channel()

    def _make_rkey(self, data):
        gateway_eui = int(data['gatewayEui'], 16)
        profile = int(data['profileId'], 0)
        endpoint = int(data['endpointId'], 0)
        cluster = int(data['clusterId'], 0)
        attribute = int(data['attributeId'], 0)

        rkey = f'{gateway_eui}.{profile}.{endpoint}.{cluster}.{attribute}'
        return rkey

    def _make_payload(self, data):
        payload = {
            'value': data['value'],
            'timestamp': data['timestamp']
        }
        return json.dumps(payload)

    def api_get(self):
        resp = requests.get(self.API_RESULTS_URL)
        res = json.loads(resp.content)
        print('[*] - Response from API Results:')
        # print(f'--> Status Code: {resp.status_code}')
        # print(f'--> Headers: {resp.headers}')
        print(f'--> Content: {res}')
        return res

    def send_to_excnahge(self, data):
        rkey = self._make_rkey(data)
        payload = self._make_payload(data)
        print(f'[*] - Sending data to topic <{rkey}>')
        self._rabbit_ch.basic_publish(exchange=self.RABBITMQ_EXCHANGE,
                                      routing_key=rkey,
                                      body=payload)

    def run_forever(self):
        while True:
            res = self.api_get()
            self.send_to_excnahge(res)
            time.sleep(1 / self.LOOP_RATE)


if __name__ == '__main__':
    try:
        feeder = Feeder()
        feeder.run_forever()
    except KeyboardInterrupt:
        print('\nInterrupted') 
    try:
        sys.exit(0)
    except SystemExit:
        os._exit(0)
