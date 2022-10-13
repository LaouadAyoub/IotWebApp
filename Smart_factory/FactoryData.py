import random
import paho.mqtt.client as mqtt
import pandas as pd
import sqlite3 as sqlite

import paho.mqtt.client as mqtt
import time
import json

class FactoryData(object):



    def __init__(self, process_names=None):

        if process_names is None:
            process_names = []

        self._process_names = process_names

    def get_data(self):
        return {
            pname: self._sample_data(pname) for pname in self._process_names
        }
    def send_data(self,data):
        TOKEN = "dash"
        BROKER_URL = "test.mosquitto.org"
        MQTT_TOPIC = "reception"  # topic name
        INTERVAL = 3  # delay in seconds
        def on_connect(client, userdata, flags, rc):
            print("Connection code: " + str(rc) + ", flags:" + str(flags))
        try:
            client = mqtt.Client()
            client.on_connect = on_connect
            client.username_pw_set(username=TOKEN, password='')  # token as username, empty password
            client.connect(host=BROKER_URL)
            client.loop_start()
            payload = [data]
            payload = json.dumps(payload)
            print(payload)
            client.publish(topic=MQTT_TOPIC, payload=payload)  # publish data
            time.sleep(INTERVAL)
        except KeyboardInterrupt:
            pass


    def _sample_data(self, process_name):

        #création de trois tableau Panda à partir de la base de donnés
        dbFile = "capteurs.db"
        conn = sqlite.connect(dbFile)

        df_humidity = pd.read_sql("SELECT * FROM humidity", conn)
        humi = df_humidity.iloc[-1, 2]

        df_temperature = pd.read_sql("SELECT * FROM temperature", conn)
        temp = df_temperature.iloc[-1, 2]

        temps = df_temperature.iloc[-1, 1]

        df_panne1 = pd.read_sql("SELECT * FROM panne1", conn)
        panne1 = df_panne1.iloc[-1, 2]

        base_value = random.random()
        data = {
            'indicateur_qualite': 6 + base_value,
            'indicateur_performance': 8 - base_value * 2,
            'materiels': 'red' if base_value < 0.01 else 'orange',
            'production': 'orange' if base_value < 0.1 else 'green',
            'conditionnement': 'yellow' if base_value < 0.05 else 'orange',
            'panne1': panne1,
            'manufacturing_temp': temp,
            'manufacturing_humi': humi,
            'production_levels': temps

        }
        return data[process_name]
