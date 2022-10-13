#Déclaration des bibliothèques
import paho.mqtt.client as mqtt
import pandas as pd
import sqlite3 as sqlite
import json


#Pour utiliser MQTT, nous avons besoin de définir: un TOKEN, l'URL d'un BROKER, un TOPIC ainsi qu'un intervalle de temps
#qui déclenchera les évènements

BROKER_URL = "192.168.1.97" # MQTT broker address
TOKEN = "dash" # Ubidots token
TOPIC = "smart/humi"
fix = 0

#Déclaration du ficher dans lequel la base de données sera insérée
dbFile = "capteurs.db"

#Initialisation de la variable data
data = ""


# Dès que nous sommes connectés, nous nous abonnons au topic pour recevoir les données et nous affichons que nous sommes
#connectés
def on_connect(client, userdata, flags, rc):

    client.subscribe(TOPIC)
    print("[INFO] Connected!")

#Fontion qui permet d'écrire dans la base de donnée une table nommée température
def writeToDb_temperature(theTime, temperature ):

    #Notre identifiant de connexion pointe sur le ficier de la base de donnée
    conn = sqlite.connect(dbFile)
    #Création d’un curseur. Le curseur permet d’exécuter une requête SQL et de récupérer un ensemble d’enregistrements.
    c = conn.cursor()
    #Création d'une table
    c.execute(""" CREATE TABLE IF NOT EXISTS temperature (id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, le_temps REAL, temperature REAL )""")
    #Ecriture dans la base de donnée
    c.execute("INSERT INTO temperature (letime, temperature)  VALUES (?,?)", (theTime, temperature))
    #Enregistrement des valeurs
    conn.commit()

    df_temperature = pd.read_sql("SELECT * FROM temperature", conn)
    #print(df_temperature)

#Même principe que la fonction température sauf que nous insérons les données provenant de l'humidité
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

#Même principe que pour la température sauf que nous insérons les données provenant des boutons
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

#Callback qui est appelé quand nous recevons une publication du serveur
def on_message(client, userdata, msg):
    #Nous affichons les valeurs pour voir si nous recevons les valeurs
    print("message received", str(msg.payload.decode("utf-8")))
    #Nous les décodons car nous avons utilisé un JSON.DUMPS pour publier et nous les insérons dans une variable
    data = msg.payload.decode("utf-8", "ignore")
    #Si cette variable contient une valeur alors nous exécutons le code suivant
    if (data != ""):
        # UNe fois décoder nous devons utiliser la fonction JSON.LOADS pour extraire les valeurs
        data = json.loads(data)
        # La température sera contenue dans la liste en [0]
        temp = data[0]
        #Et nous la passons en réel
        temp = float(temp)
        #Nous l'affichons pour vérification
        print(f"La température égale : {temp}")
        # L'humidité sera contenue dans la liste en [1]
        humi = data[1]
        # Et nous la passons en réel
        humi = float(humi)
        # Nous l'affichons pour vérification
        print(f"L'humidité' égale : {humi}")
        # La temps sera contenue dans la liste en [2]
        time = data[2]
        # Nous l'affichons pour vérification
        print(f"Le temps de réception égale : {time}")
        #Nous envoyons de base que 3 valeurs dans la liste (temps, humidité, température)
        # Cependant, quand nous appuyons sur les boutons, nous devons envoyer une 4ème valeurs
        #DOnc si la liste est supérieur à 3 valeurs alors
        if len(data) > 3 :
            #Le sentrées des boutons seront contenu dans liste en [3]
            panne1 = data[3]
            #Nous envoyons cette fois ci un texte donc on passe la variable en string
            panne1 = str(panne1)
            #Nous affichons pour vérification
            print(f"La panne1 : {panne1}")
            #Puis on écrit dans la base de données
            writeToDb_panne1(time, panne1)
        "Ecriture dans la base de données"
        #Si le data est différent de vide alors nous écrivons dans les bases de données respectives
        writeToDb_humidity(time, humi)
        writeToDb_temperature(time, temp)

#Définition de notre fonctio main qui va nous permettre de nous connecter au client MQTT
def main():
    mqttc = mqtt.Client()
    mqttc.username_pw_set(TOKEN, password="")
    mqttc.on_message = on_message
    mqttc.on_connect = on_connect
    mqttc.connect(BROKER_URL)
    try:
        mqttc.loop_forever()
    except KeyboardInterrupt:
        print('\nDisconnection')
        mqttc.disconnect()

if __name__ == '__main__':
    main()