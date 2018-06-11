#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import requests
import sys
import websocket
import time
from datetime import datetime
import dateutil.parser


class IntegrationClient(object):

    def __init__(self):
        self.data = None

    def fetch_data(self):
        payload = {}
        headers = {}

        r = requests.get('http://localhost:8000/books/book/', params=payload, headers=headers)
        if r.status_code == 200:
            self.res = r.json()
        else:
            print('Error has occured while fetching data from petasense cloud. Error code: %s' % r.status_code)
            sys.exit()

    def prepare_data_for_ufl(self):
        self.res = self.res['objects']
        self.data = ""
        for r in self.res:
            time = datetime.utcnow()
            d = "{tag_name}, {time}, {value}\n".format(
                    tag_name=r['title'],
                    time=time,
                    value=str(r['cost'])
                )
            self.data += d
        self.data.encode('UTF-8')

    def push_data_to_ufl(self):
        s = requests.session()
        s.auth = ('petasense', 'petasense')
        response = s.put("", data=self.data, verify=False)

        if response.status_code != 200:
            print('The following error(%s) has occured while pushing to UFL:' % response.status_code)
            sys.exit()
        else:
            print('The data sent to UFL successfully.')
            print('Check the "PI Connectors" event logs '
                        'for any other errors processing the sent data.')

    def get_predix_uaa_token(self):
        payload = {
            'grant_type': 'client_credentials',
            'client_id': 'test_client',
            'client_secret': 'Petarox14',
            'response_type': 'token'
        }
        r = requests.post("https://09365f33-e0f9-437d-b45d-8d234c3ca554.predix-uaa.run.aws-usw02-pr.ice.predix.io/oauth/token", data=payload)
        if r.status_code == 200:
            token = r.json()['access_token']
            self.predix_auth_head_token = 'Bearer ' + str(token)
        else:
            print('Error occured while generating Predix UAA token. Error code: ',
                  r.status_code)
            sys.exit()

    def create_ingest_body(self, sensor_id, ts, value):
        mid = "Petasense_" + str(int(round(1000*time.time())))
        datapoints = [[int(round(1000*ts)), value], ]
        return {
            'messageId': mid,
            'body': [{
                "name": str(sensor_id),
                "datapoints": datapoints,
                "attributes": {"test": True}
            }]
        }

    def push_data_to_predix(self):
        self.get_predix_uaa_token()
        headers = {
            'Predix-Zone-Id': "",  # 972f6020-1836-49cc-805f-8344bf998f53
            'Authorization': self.predix_auth_head_token,
            'Content-Type': 'application/json'
        }

        print("Connecting to wss://gateway-predix-data-services.run.aws-usw02-pr.ice.predix.io/v1/stream/messages")
        try:
            ws = websocket.create_connection("wss://gateway-predix-data-services.run.aws-usw02-pr.ice.predix.io/v1/stream/messages", header=headers)
        except websocket._exceptions.WebSocketBadStatusException as err:
            print('Error has occured while connecting to timeseries server. Error code: ',
                  err.status_code)
            sys.exit()

        print("Connected")
        utc_time = datetime.utcnow().replace(tzinfo=None)
        dt = datetime(1970, 1, 1).replace(tzinfo=None)
        epoch_time = (utc_time - dt).total_seconds()
        for r in self.res:
            ws.send(json.dumps(self.create_ingest_body(r['title'], epoch_time, r['cost'])))
        result = ws.recv()
        print (result)
        ws.close()

    def run(self):
        self.fetch_data()
        self.prepare_data_for_ufl()
        # self.push_data_to_ufl()
        self.push_data_to_predix()


if __name__ == "__main__":
    client = IntegrationClient()
    IntegrationClient.run(client)
