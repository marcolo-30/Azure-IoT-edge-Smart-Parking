import random  
import time  
import threading  
import RPi.GPIO as GPIO  
from datetime import datetime  
 
# Using the Python Device SDK for IoT Hub:  
# The sample connects to a device-specific MQTT endpoint on your IoT Hub.  

from azure.iot.device import IoTHubDeviceClient, Message, MethodResponse  


# The device connection string to authenticate the device with your IoT hub. 
# Using the Azure CLI:  
# az iot hub device-identity show-connection-string --hub-name {YourIoTHubName} --device-id MyNodeDevice --output table  

CONNECTION_STRING = "AzureConnectionString"  

# Define the JSON message to send to IoT Hub.  
 

MSG_TXT = '{{"parking:" {id} ,"tiempo:" {tiempo} ,"estado:" {estado},"temperatura:" {temperatura}}}'  
 

port = 1  
id="Parqueadero1"  
GPIO.setwarnings(False)  
GPIO.setmode(GPIO.BOARD)  
GPIO.setup(11, GPIO.IN) #Read output from PIR motion sensor  
GPIO.setup(13, GPIO.OUT) #LED output pin  
TEMPERATURE = 20.0  
HUMIDITY = 60  
Accion = 0  

   

 

def iothub_client_init():  

    # Create an IoT Hub client  
    client = IoTHubDeviceClient.create_from_connection_string(CONNECTION_STRING)  
    return client  

def iothub_client_telemetry_sample_run():  

    try:  
        client = iothub_client_init()  
        print( "IoT Hub device sending periodic messages, press Ctrl-C to exit" )  
        while True:  
 
            i=GPIO.input(11)  
            if i==0:  

                estado="evaluando"  
                print(estado)  
                GPIO.output(13,0)  
                time.sleep(1)  

            elif i==1:  

                estado="ocupado"  
                print(estado)  
                GPIO.output(13,1)  
                now = datetime.now()  
                hora_ingreso = now.strftime("%Y%m%d:%H:%M:%S")  
                tiempo=hora_ingreso  
                print("Hora de deteccion", hora_ingreso)  
                temperatura = TEMPERATURE + (random.random() * 15)  
                msg_txt_formatted = MSG_TXT.format(id=id,tiempo=tiempo,estado=estado,temperatura=temperatura)  
                message = Message(msg_txt_formatted)  
                print( "Sending message: {}".format(message) )  
                client.send_message(message)  
                print ( "Message successfully sent" )  

                time.sleep(5)  

                estado="disponible"  
                GPIO.output(13,0)  
                now = datetime.now()  
                hora_salida = now.strftime("%Y%m%d:%H:%M:%S")  
                tiempo=hora_salida  
                temperatura = TEMPERATURE + (random.random() * 15)  
                print("Hora de salida", hora_salida)  
                print("temperatura salida",temperatura)  
                msg_txt_formatted = MSG_TXT.format(id=id,tiempo=tiempo,estado=estado,temperatura=temperatura)  
                message = Message(msg_txt_formatted)  
                print( "Sending message: {}".format(message) )  
                client.send_message(message)  
                print ( "Message successfully sent") 

    except KeyboardInterrupt:  

        print ( "IoTHubClient sample stopped" )  


if __name__ == '__main__':  


    print ( "IoT Hub Quickstart #2 - Simulated device" )  
    print ( "Press Ctrl-C to exit" )  
    iothub_client_telemetry_sample_run()  