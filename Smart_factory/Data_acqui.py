import dash
import dash_daq as daq
import dash_core_components as dcc
import dash_html_components as html
import paho.mqtt.client as mqtt
import pandas as pd
from time import gmtime, strftime
import sqlite3 as sqlite
from time import gmtime, strftime
import sqlite3 as sqlite
import json

PORT = 1883
BROKER_URL = "test.mosquitto.org" # MQTT broker address
TOKEN = "dash" # Ubidots token
TOPIC = "smart/humi"
fix = 0


dbFile = "capteurs.db"

data = ""


# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):

    client.subscribe(TOPIC)
    print("[INFO] Connected!")

def writeToDb_temperature(theTime, temperature ):

    conn = sqlite.connect(dbFile)
    c = conn.cursor()
    "Création d'une table"
    c.execute(""" CREATE TABLE IF NOT EXISTS temperature (id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, le_temps REAL, temperature REAL )""")
    "Writing to db"
    c.execute("INSERT INTO temperature (letime, temperature)  VALUES (?,?)", (theTime, temperature))
    conn.commit()

    df_temperature = pd.read_sql("SELECT * FROM temperature", conn)
    #print(df_temperature)

def writeToDb_humidity(theTime, humidity ):

    conn = sqlite.connect(dbFile)
    c = conn.cursor()
    "Création d'une table"
    c.execute(""" CREATE TABLE IF NOT EXISTS humidity (id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, le_temps REAL, humidity REAL )""")
    "Writing to db"
    c.execute("INSERT INTO humidity (letime, humidity)  VALUES (?,?)", (theTime, humidity))
    conn.commit()

    df_humidity = pd.read_sql("SELECT * FROM humidity", conn)
    print(df_humidity)

def writeToDb_panne1(theTime, panne1 ):

    conn = sqlite.connect(dbFile)
    c = conn.cursor()
    "Création d'une table"
    c.execute(""" CREATE TABLE IF NOT EXISTS panne1 (id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, le_temps REAL, panne1 REAL )""")
    "Writing to db"
    c.execute("INSERT INTO panne1 (le_temps, panne1)  VALUES (?,?)", (theTime, panne1))
    conn.commit()

    df_panne1 = pd.read_sql("SELECT * FROM panne1", conn)
    print(df_panne1)
# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    print("message received", str(msg.payload.decode("utf-8")))
    data = msg.payload.decode("utf-8", "ignore")
    if (data != ""):

        data = json.loads(data)
        temp = data[0]
        temp = float(temp)
        print(f"La température égale : {temp}")
        humi = data[1]
        humi = float(humi)
        print(f"L'humidité' égale : {humi}")
        time = data[2]
        print(f"Le temps de réception égale : {time}")
        theTime = strftime("%Y-%m-%d %H:%M:%S", gmtime())
        result = (theTime + "\t" + str(msg.payload))
        print("aloooo",len(data))
        if len(data) > 3 :
            panne1 = data[3]
            panne1 = str(panne1)
            print(f"La panne1 : {panne1}")
            writeToDb_panne1(time, panne1)
        "Ecriture dans la base de données"
        writeToDb_humidity(time, humi)
        writeToDb_temperature(time, temp)


def main():
    # Setup MQTT client

    mqttc = mqtt.Client()
    mqttc.username_pw_set(TOKEN, password="")
    mqttc.on_message = on_message
    mqttc.on_connect = on_connect
    mqttc.connect(BROKER_URL, PORT, 60)
    try:
        mqttc.loop_forever()
    except KeyboardInterrupt:
        print('\nDisconnection')
        mqttc.disconnect()

if __name__ == '__main__':
    main()