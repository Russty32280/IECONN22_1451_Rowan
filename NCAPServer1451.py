#!/usr/bin/env python

'''
TODO: Implement Random Number Generation for Sensor data
Confirm sending sensor data to multiple clients.
Get Sensor Alerts Working
Make into executable
Begin Conversion to 1451.0 Byte Strings

'''
import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish
import time
import _thread
import sys
from random import randint, randrange
import socket

# Determine the IP Address of the machine running the code.
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(("8.8.8.8", 80))
Address = s.getsockname()[0]
print(Address)
s.close()

mqttBroker = "broker.emqx.io"

AddressType = "1"
#Address = "172.24.125.154" # TODO: Make this a function which will obtain current IP Address
NCAPS_ID = str(randint(1, 9999))
NCAPS_Name = "Process" + NCAPS_ID
NumTIM = "1"
TIM_ID = "1"
NumChan = "3"
XDCR_ChanID_Array = "(1;2;3)"
XDCR_ChanNameArray = "(\"Temp000001\";\"Valve00001\";\"PresSw0001\")"
ResponseTopic = "RUSMARTLAB/NCAPC001"
AlertEnable = False

# MQTT Callback Functions
def on_connect(mqttc, obj, flags, rc):
    print("rc: " + str(rc))

def on_message(mqttc, obj, msg):
    print(msg.topic + " " + str(msg.qos) + " " + msg.payload.decode('UTF-8'))
    MsgDict = MessageParse(msg.payload.decode('UTF-8'))
    print(MsgDict)
    if MsgDict["NetSvcType"] == '1':
        if MsgDict["NetSvcID"] == '3':
            _thread.start_new_thread(Thread132, (tuple(MsgDict.items()), ('ResponseTopic', ResponseTopic)))
        elif MsgDict["NetSvcID"] == '5':
            _thread.start_new_thread(Thread152, (tuple(MsgDict.items()), ('ResponseTopic', ResponseTopic)))
        elif MsgDict["NetSvcID"] == '6':
            _thread.start_new_thread(Thread162, (tuple(MsgDict.items()), ('ResponseTopic', ResponseTopic)))
    elif MsgDict["NetSvcType"] == '2':
        if MsgDict["NetSvcID"] == '1':
            _thread.start_new_thread(Thread212, (tuple(MsgDict.items()), ('ResponseTopic', ResponseTopic)))
        elif MsgDict["NetSvcID"] == '7':
            _thread.start_new_thread(Thread272, (tuple(MsgDict.items()), ('ResponseTopic', ResponseTopic)))
    elif MsgDict["NetSvcType"] == '4':
        if MsgDict["NetSvcID"] == '1':
            _thread.start_new_thread(Thread412, (tuple(MsgDict.items()), ('ResponseTopic', ResponseTopic)))
        elif MsgDict["NetSvcID"] == '2':
            _thread.start_new_thread(Thread422, (tuple(MsgDict.items()), ('ResponseTopic', ResponseTopic)))

def on_publish(mqttc, obj, mid):
    print("mid: " + str(mid))

def on_subscribe(mqttc, obj, mid, granted_qos):
    print("Subscribed: " + str(mid) + " " + str(granted_qos))

def on_log(mqttc, obj, level, string):
    print(string)

# Parsing Engine
def MessageParse(msg):
    parse = msg.split(",")
    NetSvcType = parse[0]
    NetSvcID =  parse[1]
    MsgType =  parse[2]
    MsgLength =  parse[3]
    if NetSvcType == '1': # It is a discovery service
        if NetSvcID == '3': # NCAP Discovery Request Note -> should be 4
            NCAPC_ID = parse[4]
            Timeout = parse[5]
            return{'NetSvcType':NetSvcType, 'NetSvcID':NetSvcID, 'MsgType':MsgType, 'MsgLength':MsgLength, 'NCAPC_ID':NCAPC_ID, 'Timeout':Timeout}
        elif NetSvcID == "5":
            NCAPC_ID = parse[4]
            NCAPS_ID = parse[5]
            Timeout = parse[6]
            return{'NetSvcType':NetSvcType, 'NetSvcID':NetSvcID, 'MsgType':MsgType, 'MsgLength':MsgLength, 'NCAPC_ID':NCAPC_ID, 'NCAPS_ID':NCAPS_ID, 'Timeout':Timeout}
        elif NetSvcID == "6":
            NCAPC_ID = parse[4]
            NCAPS_ID = parse[5]
            TIM_ID = parse[6]
            Timeout = parse[7]
            return{'NetSvcType':NetSvcType, 'NetSvcID':NetSvcID, 'MsgType':MsgType, 'MsgLength':MsgLength, 'NCAPC_ID':NCAPC_ID, 'NCAPS_ID':NCAPS_ID,  'TIM_ID':TIM_ID, 'Timeout':Timeout}
        elif NetSvcID == "7":
            NCAPC_ID = parse[4]
            NCAPS_ID = parse[5]
            TIM_ID = parse[6]
            NumChan = parse[7]
            XDCR_ChanID_Array = parse[8]
            return{'NetSvcType':NetSvcType, 'NetSvcID':NetSvcID, 'MsgType':MsgType, 'MsgLength':MsgLength, 'NCAPC_ID':NCAPC_ID, 'NCAPS_ID':NCAPS_ID, 'TIM_ID':TIM_ID, 'NumChan':NumChan, 'XDCR_ChanID_Array':XDCR_ChanID_Array}
    elif NetSvcType == '2':
        if NetSvcID == '1':
            NCAPC_ID = parse[4]
            NCAPS_ID = parse[5]
            TIM_ID = parse[6]
            XDCR_ChanID = parse[7]
            Timeout = parse[8]
            Mode = parse[9]
            return{'NetSvcType':NetSvcType, 'NetSvcID':NetSvcID, 'MsgType':MsgType, 'MsgLength':MsgLength, 'NCAPC_ID':NCAPC_ID, 'NCAPS_ID':NCAPS_ID, 'TIM_ID':TIM_ID, 'XDCR_ChanID':XDCR_ChanID, 'Timeout':Timeout, 'Mode':Mode}
        elif NetSvcID == '7':
            NCAPC_ID = parse[4]
            NCAPS_ID = parse[5]
            TIM_ID = parse[6]
            XDCR_ChanID = parse[7]
            WriteActuatorData = parse[8]
            Timeout = parse[9]
            Mode = parse[10]
            return{'NetSvcType':NetSvcType, 'NetSvcID':NetSvcID, 'MsgType':MsgType, 'MsgLength':MsgLength, 'NCAPC_ID':NCAPC_ID, 'NCAPS_ID':NCAPS_ID, 'TIM_ID':TIM_ID, 'XDCR_ChanID':XDCR_ChanID, 'WriteActuatorData':WriteActuatorData, 'Timeout':Timeout, 'Mode':Mode}
    elif NetSvcType == '4':
        if NetSvcID == '1':
            NCAPC_ID = parse[4]
            NCAPS_ID = parse[5]
            TIM_ID = parse[6]
            NumChan = parse[7]
            XDCR_ChanID = parse[8]
            AlertMinMaxArray = parse[9]
            return{'NetSvcType':NetSvcType, 'NetSvcID':NetSvcID, 'MsgType':MsgType, 'MsgLength':MsgLength, 'NCAPC_ID':NCAPC_ID, 'NCAPS_ID':NCAPS_ID, 'TIM_ID':TIM_ID, 'NumChan':NumChan, 'XDCR_ChanID':XDCR_ChanID, 'AlertMinMaxArray':AlertMinMaxArray}
        elif NetSvcID == '2': #THIS IS 100% WRONG
            NCAPC_ID = parse[4]
            NCAPS_ID = parse[5]
            TIM_ID = parse[6]
            NumChan = parse[7]
            XDCR_ChanID = parse[8]
            AlertMinMaxArray = parse[9]
            return{'NetSvcType':NetSvcType, 'NetSvcID':NetSvcID, 'MsgType':MsgType, 'MsgLength':MsgLength, 'NCAPC_ID':NCAPC_ID, 'NCAPS_ID':NCAPS_ID, 'TIM_ID':TIM_ID, 'NumChan':NumChan, 'XDCR_ChanID':XDCR_ChanID, 'AlertMinMaxArray':AlertMinMaxArray}

# Use this comment structure for service threads
'''
X.X.X Service_Name (XX XX) - X

 - Description

Network Service type (NetSvcType) = _ ()
Network Service ID   (NetSvcId)   = _ ()
Message Type         (MsgType)    = _ ()
'''

# Service threads

'''
10.1.4 NCAP discovery (01 04) - Reply

 - The APP uses this service to discover active NCAPs

Network Service type (NetSvcType) = 1 (Discovery service)
Network Service ID   (NetSvcId)   = 4 (NCAPDiscovery)
Message Type         (MsgType)    = 2 (Reply)

Notes
- should be called Thread142
'''
def Thread132(MSG_Tuple, SenderInfo):
    # NCAP Server Discover Response
    #print(MSG_Tuple)
    #print(SenderInfo)
    MSG = dict(MSG_Tuple)
    #print(MSG)
    response = '1,3,2,25,0' + MSG["NCAPC_ID"] + ',' + NCAPS_ID + ',' + NCAPS_Name + AddressType + ',' + Address
    #mqtt_send(str(SenderInfo[1]), response)
    LocalResponseTopic = "RUSMARTLAB/"+MSG["NCAPC_ID"]
    print("Local Reponse Topic: " + LocalResponseTopic + "\n")
    publish.single(LocalResponseTopic, response, hostname=mqttBroker)

'''
10.1.5 NCAP TIM discovery (01 05) - Reply

 - The APP uses this service to discover TIMs connected to active NCAPs

Network Service type (NetSvcType) = 1 (Discovery service)
Network Service ID   (NetSvcId)   = 5 (NCAPTIMDiscovery)
Message Type         (MsgType)    = 2 (Reply)
'''
def Thread152(MSG_Tuple, SenderInfo):
    #MSG = dict(map(None, MSG_Tuple))
    # TODO: Add the TIM Discovery Function
    MSG = dict(MSG_Tuple)
    response = '1,5,2,39,' + '0,' + NCAPS_ID + ',' + NumTIM + ',' + '1' + ','+ "BatchRx001"
    #publish.single(ResponseTopic, response, hostname=mqttBroker)
    LocalResponseTopic = "RUSMARTLAB/"+MSG["NCAPC_ID"]
    print("Local Reponse Topic: " + LocalResponseTopic + "\n")
    publish.single(LocalResponseTopic, response, hostname=mqttBroker)

'''
10.1.6 NCAP TIM transducer discovery (01 06) - Reply

 - The APP uses this service to discover TransducerChannels on TIMS connected to active NCAPS

Network Service type (NetSvcType) = 1 (Discovery service)
Network Service ID   (NetSvcId)   = 6 (NCAPTIMTransducerDiscovery)
Message Type         (MsgType)    = 2 (Reply)
'''
def Thread162(MSG_Tuple, SenderInfo):
    #MSG = dict(map(None, MSG_Tuple))
    MSG = dict(MSG_Tuple)
    response = '1,6,2,55,' + '0,' + NCAPS_ID + ',' + TIM_ID + ',' + NumChan + ',' + XDCR_ChanID_Array + ',' + XDCR_ChanNameArray
    #publish.single(ResponseTopic, response, hostname=mqttBroker)
    LocalResponseTopic = "RUSMARTLAB/"+MSG["NCAPC_ID"]
    print("Local Reponse Topic: " + LocalResponseTopic + "\n")
    publish.single(LocalResponseTopic, response, hostname=mqttBroker)

'''
10.2.1 Synchronous read transducer sample data from a channel of a TIM (02 01) - Reply

 - This service is used to read transducer sample data from a TIM Channel

Network Service type (NetSvcType) = 2 (Transducer access service)
Network Service ID   (NetSvcId)   = 1 (SyncReadTransducerSampleDataFromAChannelOfATIM)
Message Type         (MsgType)    = 2 (Reply)
'''
def Thread212(MSG_Tuple, SenderInfo):
    print("In Thread212")
    MSG = dict(MSG_Tuple)
    ReadSensorData = "0"
    if MSG["TIM_ID"] == '1':
        if MSG["XDCR_ChanID"] == '1':
            #ReadSensorData = str(round(sensor.temperature,2))
            ReadSensorData = str(20 + randint(0,10))
    response = '2,1,1,N,0,' + NCAPS_ID + ',' + TIM_ID + ',' + MSG["XDCR_ChanID"] + ',' + ReadSensorData + ',' + time.strftime("%H:%M:%S", time.localtime())
    print(response)
    #publish.single(ResponseTopic, response, hostname=mqttBroker)
    LocalResponseTopic = "RUSMARTLAB/"+MSG["NCAPC_ID"]
    print("Local Reponse Topic: " + LocalResponseTopic + "\n")
    publish.single(LocalResponseTopic, response, hostname=mqttBroker)

'''
10.2.7 Synchronous write transducer sample data to a channel of a TIM service (02 07) - Reply

 - This service is used to write a single transducer setting to a specific channel of a 
   specific TIM of a specific active NCAP

Network Service type (NetSvcType) = 2 (Transducer access service)
Network Service ID   (NetSvcId)   = 7 (SyncWriteTransducerSampleDataFromAChannelOfATIM)
Message Type         (MsgType)    = 2 (Reply)
'''
def Thread272(MSG_Tuple, SenderInfo):
    MSG = dict(MSG_Tuple)
    if MSG["TIM_ID"] == '1':
        if MSG["XDCR_ChanID"] == '2':
            print(str(MSG["WriteActuatorData"]))
            display.show(MSG["WriteActuatorData"])
    response = '2,7,2,19,0,' + NCAPS_ID + ',' + TIM_ID + ',' + MSG["XDCR_ChanID"]
    #publish.single(ResponseTopic, response, hostname=mqttBroker)
    LocalResponseTopic = "RUSMARTLAB/"+MSG["NCAPC_ID"]
    print("Local Reponse Topic: " + LocalResponseTopic + "\n")
    publish.single(LocalResponseTopic, response, hostname=mqttBroker)

'''
10.4.1 Subscribe new TIM from NCAP (04 01) - Reply

 - When a new TIM is plugged in, the TIM sends a TIM notification to the NCAP, and the NCAP
   should report this new TIM to the APP. The APP should subscribe a new TIM plug-in service

Network Service type (NetSvcType) = 4 (Event notification service)
Network Service ID   (NetSvcId)   = 1 (SubscribeNewTIMFromNCAP)
Message Type         (MsgType)    = 2 (Reply)
'''
def Thread412(MSG_Tuple, SenderInfo):
    MSG = dict(MSG_Tuple)
    if MSG["NCAPC_ID"] == "1":
        global AlertEnable
        AlertEnable = True
    response = '4,1,2,29,0,' + MSG["NCAPC_ID"] + ',' + "11" + ',' + NCAPS_ID + ',' + TIM_ID + ',' + '1,' + MSG["XDCR_ChanID"]
    #publish.single(ResponseTopic, response, hostname=mqttBroker)
    LocalResponseTopic = "RUSMARTLAB/"+MSG["NCAPC_ID"]
    print("Local Reponse Topic: " + LocalResponseTopic + "\n")
    publish.single(LocalResponseTopic, response, hostname=mqttBroker)

'''
X.X.X Service_Name (XX XX) - X

 - Description

Network Service type (NetSvcType) = _ ()
Network Service ID   (NetSvcId)   = _ ()
Message Type         (MsgType)    = _ ()

Notes
- What is this?
'''
def Thread422(MSG_Tuple, SenderInfo):
    MSG = dict(MSG_Tuple)
    if MSG["NCAPC_ID"] == "1":
        global AlertEnable
        AlertEnable = False
    response = '4,2,2,29,0,' + MSG["NCAPC_ID"] + ',' + "11" + ',' + NCAPS_ID + ',' + TIM_ID + ',' + '1,' + MSG["XDCR_ChanID"]
    #publish.single(ResponseTopic, response, hostname=mqttBroker)
    LocalResponseTopic = "RUSMARTLAB/"+MSG["NCAPC_ID"]
    print("Local Reponse Topic: " + LocalResponseTopic + "\n")
    publish.single(LocalResponseTopic, response, hostname=mqttBroker)

def SendAlert(SubscriptionID, Value):
    #TargetClients = CheckSubscriberList(SubscriptionID)
    if AlertEnable == True:
        TargetClients = ["NCAPC001"]
    else:
        TargetClients = None
    if TargetClients != None:
        for Clients in TargetClients:
            AlertString = "4,2,4,23," + NCAPS_ID + ',' + TIM_ID + ',' + '3' + ',' + SubscriptionID + ',' + Value
            publish.single(ResponseTopic, AlertString, hostname=mqttBroker)

'''
def CheckSubscriberList(SubscriptionID):
    #TODO Possibly add value to check against mins/max
    if

def AddSubscriber(NCAPC_ID, SubscriptionID):

'''

# MQTT Client Initialization
mqttc = mqtt.Client()
mqttc.on_message = on_message
mqttc.on_connect = on_connect
mqttc.on_publish = on_publish
mqttc.on_subscribe = on_subscribe
# Uncomment to enable debug messages
# mqttc.on_log = on_log
mqttc.connect(mqttBroker, 1883, 60)
mqttc.subscribe("RUSMARTLAB/"+NCAPS_ID, 0)

# Start the Client Loop
mqttc.loop_start()
while True:
    publish.single("RUSMARTLAB/Heartbeat", NCAPS_ID +",1", hostname=mqttBroker)
    print("Published Heartbeat")
    time.sleep(10)
mqttc.loop_stop()