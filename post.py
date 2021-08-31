# import sqlite3
# from pytz import timezone
# from datetime import datetime
#
# conn = sqlite3.connect('test.db')
# cur = conn.cursor()
# format = "%Y-%m-%d %H:%M:%S %Z%z"
# now_utc = datetime.now(timezone('UTC'))
# now_asia = now_utc.astimezone(timezone('Asia/Kolkata'))
# mac_id = "asdfd"
# temperature= 10.1
# air_quality = 11.1
#
# cur = conn.cursor()
# sql = "INSERT INTO lorasensordata (mac_id, temperature, air_quality,addedDateTime) VALUES (?, ?, ?, ?)"
# val = (mac_id, temperature,air_quality,datetime.datetime.now())
#
#  # cur.execute("INSERT INTO lorasensordata (mac_id, temperature, air_quality,addedDateTime)VALUES ("10",11,12,2020-08-06 19:19:39.944839)");
# #
# cur.execute(sql,val)
#
# conn.commit()
# print ("Records created successfully)"
# conn.close()

import json
import paho.mqtt.client as mqtt
import sqlite3
from datetime import datetime
from pytz import timezone
import requests
import random

MQTT_SERVER = "broker.hivemq.com"
MQTT_PATH1 = "/lora/temp"
MQTT_PATH2 = "/zed/barcode"
MQTT_PATH3 = "/zed/validate/nfc"
MQTT_PATH4 = "/zed/validate/barcode"
# format = "%Y-%m-%dT%H:%M"
now_utc = datetime.now(timezone('UTC'))
now_asia = now_utc.astimezone(timezone('Us/Eastern'))
print(now_asia)
dateString = str(now_asia)
ada = dateString[:10]+"T"+dateString[11:]
datee = ada[:19]
print (datee)
# print (ada)
print(MQTT_SERVER)
# conn = psycopg2.connect(database = "karthik", user = "karthik", password = "karthikkaran", host = "127.0.0.1", port = "5432")
# # mydb = mysql.connector.connect(
# #   host="127.0.0.1",
# #   user="root",
# #   passwd="password",
# #   database="messages"
# # )
conn = sqlite3.connect('data.db')

token = "3Y1QwEDfikGni1PPouV7aw=="

def nfc():
    now_utc = datetime.now(timezone('UTC'))
    now_asia = now_utc.astimezone(timezone('Us/Eastern'))
    dateString = str(now_asia)
    ada = dateString[:10]+"T"+dateString[11:]
    datee = ada[:19]
    print (datee)
    print("inside transaction")
    random_number = random.randint(1000000000000000, 9999999999999999)
    print (random_number)

    data1  = {
            "Token": "ac23fb78-53f9-49c8-8d19-fc2b5efaf376",
            "FromAddress": "S 6th @ W Liberty",
            "DestinationAddress": "Iroquois Park Loop",
            "TransactionDate": datee,
            "currentlocation": "true",
            "departattime": datee,
            "TotalAmount": "1.50",
            "PlaceId": "123456",
            "Tickets": [
                {
                    "Amount": "1.50",
                    "RouteId": "Single Ride",
                    "TripId": "4",
                    "ProfileId": 0,
                    "FromAddress": "S 6th @ W Liberty ",
                    "DestinationAddress": "Iroquois Park Loop",
                    "Fareid": "9",
                    "Tickettype": 0
                }
            ],
            "Message": "Ticket Take in NFC App",
            "TransactionId": "2"+str(random_number),
            "Userid": 10504
    }
    json_data1 = json.dumps(data1,indent=2)
    print(json_data1)
    headers = {'Content-type': 'application/json'}
    r = requests.post(url = "https://closerlookdigitalsoftware.com/ZIGSTARCTEST/api/Tickets/Addnew", data = json_data1,headers=headers,timeout = 15)
    ticketDetails = r.json()
    #
    print(ticketDetails)
    print(r)

def nfcValidate(cardId,topic):
    print("inside function")
    nfcUrl = "https://closerlookdigitalsoftware.com/ZIGSTARCTest/api/Inspector/Purchaseticketfromwallet?TokenID=3Y1QwEDfikGni1PPouV7aw==&PhysicalID={}&wallettype=0".format(cardId)
    print(nfcUrl)
    r = requests.post(url = nfcUrl,timeout=5)
    print (r.text)
    if(r.text == "true"):
        ret= client.publish(topic,"1")
    else:
        ret= client.publish(topic,"3")


def getTicket(barcode,DeviceId):
    print(barcode)
    data = {
        "TicketId":barcode,
        "Token":token,
        "Blnvalidate":"true",
        "Whichdevice":2
    }

    r = requests.post(url = "https://closerlookdigitalsoftware.com/ZIGSTARCTEST/api/Firmware/Firmwareticketstatus", data = data,timeout = 5)
    ticketDetails = r.json()
    if(str(r) != "<Response [500]>"):
        print(ticketDetails)
        ticketStatus = ticketDetails['Result']['Status']
        print(ticketStatus)
        if(ticketStatus == 1):
            print("Ticket validated")
            return 1
        elif(ticketStatus == 3):
            print("Not a valid ticket")
            return 3
    else:
        print ("Invalid Ticket")
        return 0




def on_publish(client,userdata,result):             #create function for callback
    print("data published \n")
    pass
# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe(MQTT_PATH1)
    client.subscribe(MQTT_PATH2)
    client.subscribe(MQTT_PATH3)
    client.subscribe(MQTT_PATH4)

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    now_utc = datetime.now(timezone('UTC'))
    now_asia = now_utc.astimezone(timezone('Us/Eastern'))
    print(now_asia)
    dateString = str(now_asia)
    ada = dateString[:10]+"T"+dateString[11:]
    datee = ada[:19]


    #print(msg.topic+" "+str(msg.payload))

    print("success")
    topic = msg.topic
    print(type(topic))

    if (topic==MQTT_PATH1):
        y = json.loads(msg.payload)
        print(y["mac_id"])
        cur = conn.cursor()
        mac_id = y["mac_id"]
        temperature= y["temperature"]
        air_quality = y["air_quality"]

        # sql = "INSERT INTO lorasensordata (mac_id, temperature, air_quality, addedDateTime) VALUES (%s, %s, %s, %s)"
        # val = (y["mac_id"], y["temperature"],y["air_quality"],now_asia)
        sql = "INSERT INTO lorasensordata (mac_id, temperature, air_quality,addeDateTime) VALUES (?, ?, ?, ?)"
        val = (mac_id, temperature,air_quality,datetime.now())
        cur.execute(sql,val)
        conn.commit()
        print(cur.rowcount, "record inserted.")

    elif(msg.topic==MQTT_PATH2):
        print("inside")
        y = json.loads(msg.payload)
        DeviceId = y["DeviceId"]
        ticketId = y["ticketId"]
        topic = DeviceId+"/barcode"
        print(DeviceId)
        data = cur.fetchone()
        print(data[3])
        if(data[3]==0):
            print(topic)
            ret= client.publish(topic,"1")
            ticketStatus =1
            cur.execute("UPDATE barcodetickets SET ticketStatus=?,validateddatetime=? where ticketId=?",(ticketStatus,now_asia,ticketId))
            conn.commit()
        elif(data[3]==1):
            print("data received")
            ret= client.publish(topic,"0")

    elif(msg.topic==MQTT_PATH4):
        print("inside p4")
        y = json.loads(msg.payload)
        ticketId = y["ticketId"]
        DeviceId = y["DeviceId"]
        topic = "3C:71:BF:F9:D7:70/barcode"
        print(DeviceId)
        print(topic)
        print(ticketId)
        print("gng to api")
        data = getTicket(ticketId,DeviceId)
        print(data)
        if(data==1):
            print(topic)
            ret= client.publish(topic,"1")
        elif(data==3):
            ret= client.publish(topic,"3")
        elif(data==0):
            ret= client.publish(topic,"0")
    elif(msg.topic==MQTT_PATH3):
        print("inside p3")
        y = json.loads(msg.payload)
        cardId = y["cardId"]
        DeviceId = y["DeviceId"]
        topic = "3C:71:BF:F9:D7:70/nfc"
        print(DeviceId)
        print(cardId)


        if(cardId[2]!=":"):
            cardId="0"+cardId
            print(cardId)
            nfcValidate(cardId,topic)
        else:
            nfcValidate(cardId,topic)
        # nfc()
        # cur = conn.cursor()
        # # data = cur.fetchone()
        # cur.execute("SELECT * FROM nfcDetails where cardId =?",(cardId,))
        # data = cur.fetchone()
        # print("hi")
        # print (data)
        # print(data[4])
        # if(data[4]>1.50):
        #     balance = data[4]-1.50
        #     print(topic)
        #     # ret= client.publish(topic,"1")
        #     ticketStatus =1
        #     cur.execute("UPDATE nfcDetails SET balance=?,lastValidateddatetime=? where cardId=?",(balance,now_asia,cardId))
        #     conn.commit()
        #     ret= client.publish(topic,"1")
        #     nfc()
        # elif(data[4]<1.50):
        #     print("data received")
        #     ret= client.publish(topic,"3")
        # else:
        #     print("no data")
        #     ret= client.publish(topic,"3")
    # elif(msg.topic==MQTT_PATH4):
    #     print("inside p4")
    #     print(msg.payload)
    #     y = json.loads(msg.payload)
    #     print (y)
    #     DeviceId = y["DeviceId"]
    #     ticketId = y["ticketId"]
    #     topic = "3C:71:BF:F9:D7:70/barcode"
    #     print(DeviceId)
    #     print(topic)
    #     print(ticketId)
    #     data = getTicket(ticketId)
    #     print(data)
    #     if(data==1):
    #         print(topic)
    #         ret= client.publish(topic,"1")
    #
    #     elif(data==3):
    #         ret= client.publish(topic,"3")
    #     elif(data==0):
    #         ret= client.publish(topic,"0")













client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect(MQTT_SERVER, 1883, 60)


client.loop_forever()
