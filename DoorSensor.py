from machine import Pin
import time
import json
import network

from umqtt.simple import MQTTClient
from CourseWorkSecrets import ssid, password, device_token, hivemq_host, hivemq_name, hivemq_pw, hivemq_id  #imports the data from the secrets page, such as the login info, password, and ID

##### CONNECT TO THE WIFI ######
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(ssid, password)
while wlan.isconnected() == False:
    print('waiting for connection...') #the "waiting for connection..." message will display when the the device is attemptong to connect to the network
    time.sleep(1)
print("connected to wifi") #the "connected to wifi" message will disaply when the device has connected to the network sucessfully
print(wlan.ifconfig())

##### CREATE CONNECTION OBJECT #####
mqtt_client = MQTTClient(    #this paragraph is subscribing to the mqtt server
    server = hivemq_host,
    user = hivemq_name,
    password = hivemq_pw,
    client_id = hivemq_id,
    ssl = True,
    port = 0,
    ssl_params = {"server_hostname": hivemq_host})

mqtt_client.connect()
print("connected to cluster")
distance_data_topic = "DistanceData"
led_reset_topic = "led/reset"

############# SUBSCRIBE TO JACKY'S BUTTON PRESS ################
#mqtt_subscribe_topic = "button/pressed"   

redLed = Pin(14, Pin.OUT)

def message_recieved(topic, response):  #this paragraph shows what to do with the message when it is recieved
    global redLed
    print("message received!")
    print(f"message: {response}")
    print(f"topic: {topic.decode()}")
    if topic.decode() == "led/reset":
        redLed.value(0)
        
#    
mqtt_client.set_callback(message_recieved)
mqtt_client.subscribe(distance_data_topic)
mqtt_client.subscribe(led_reset_topic)

#
#while True:
#    mqtt_client.check_msg()
#################################################################    


Trig = Pin(19, Pin.OUT, 0)
Echo = Pin(18, Pin.IN, 0)
activeBuzzer = Pin(15,Pin.OUT)
activeBuzzer.value(0)

distance = 0
soundVelocity = 340



def getDistance():
    Trig.value(1)
    time.sleep_us(10)
    Trig.value(0)
    while not Echo.value():
        pass
    pingStart = time.ticks_us()
    while Echo.value():
        pass
    pingStop = time.ticks_us()
    distanceTime = time.ticks_diff(pingStop, pingStart) // 2
    distance = int(soundVelocity * distanceTime // 10000)
    return distance

while True:
    mqtt_client.check_msg()
    time.sleep_ms(500)
    distance = getDistance()
    print("Distance: ", distance, "cm")
    if distance <= 10:
        activeBuzzer.value(1)
        mqtt_client.publish(distance_data_topic, str(distance))
        print("published distance ", distance)
        redLed.value(1)
        time.sleep(1.0)
        redLed.value(1)
        #time.sleep(1.0)
        
    else:
        activeBuzzer.value(0)
    

