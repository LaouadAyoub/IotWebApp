import random
import pandas as pd
import sqlite3 as sqlite
import paho.mqtt.client as mqtt
import time
import json

# déclaration d'une classe FactoryData
class FactoryData(object):

    
    # si on rentre aucun paramétre en entrée de la fonction, on return une liste vide
    def __init__(self, process_names=None):
        if process_names is None:
            process_names = []
        self._process_names = process_names

    # Fonction get_dat
    def get_data(self):
        # retourne une liste des valeurs retourné dans la fonction sample_data, avec clé process names
        return {
            pname: self._sample_data(pname) for pname in self._process_names
        }
    # Fonction send_data envoie les données avec mqtt
    def send_data(self,data):
        TOKEN = "dash"
        BROKER_URL = "test.mosquitto.org"
        #BROKER_URL = "172.18.20.88"  # MQTT broker address

        MQTT_TOPIC = "reception"  # topic name
        INTERVAL = 3  # delay in seconds
        # fonction qui vérifie que la connexion avec broker et il retourne un message après la vérification
        def on_connect(client, userdata, flags, rc):
            print("Connection code: " + str(rc) + ", flags:" + str(flags))
        try:
            # déclaration d'un clien mqtt
            client = mqtt.Client()
            # se connecter avec ce client
            client.on_connect = on_connect
            # déclarer le nom d'utilisateur et le mot de passe
            client.username_pw_set(username=TOKEN, password='')
            # se connecter avec le broket
            client.connect(host=BROKER_URL)
            # créer une boucle d'envoie
            client.loop_start()
            # créer le message d'envoie
            payload = [data]
            # Mqtt à besoin de la forme json pour pouvoir lire les valeurs
            payload = json.dumps(payload)
            # Affichage du message avant l'envoie
            print(payload)
            # Publication du message dans le topic
            client.publish(topic=MQTT_TOPIC, payload=payload)
            # Attendre 3 seconde pour continuer
            time.sleep(INTERVAL)
        except KeyboardInterrupt:
            pass


    def _sample_data(self, process_name):

        #création de trois tableau Panda à partir de la base de donnés
        dbFile = "capteurs.db"
        conn = sqlite.connect(dbFile)

        #déclaration des variable panda contenant la base de données de température, d'humidité et de déclaration de panne
        df_humidity = pd.read_sql("SELECT * FROM humidity", conn)
        humi = df_humidity.iloc[-1, 2]

        df_temperature = pd.read_sql("SELECT * FROM temperature", conn)
        temp = df_temperature.iloc[-1, 2]

        temps = df_temperature.iloc[-1, 1]

        df_panne1 = pd.read_sql("SELECT * FROM panne1", conn)
        panne1 = df_panne1.iloc[-1, 2]

        base_value = random.random()
        # création d'un dictionnaire avec 9 variable
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
        #retourner une liste de donéées
        return data[process_name]
