import paho.mqtt.client as mqtt
import time


class MQTT:

    def on_message(self, client, userdata, message):
        class MesG:
            def __init__(self, msg, topic, msgQoS, retain_flag):
                self.msg = str(msg)
                self.topic = topic
                self.msgQos = msgQoS
                self.retain_flag = retain_flag

            def __str__(self):
                return self.msg

        msg = message.payload.decode("utf-8")
        topic = message.topic
        msgQoS = message.qos
        retain_flag = message.retain

        self.MG = MesG(msg, topic, msgQoS, retain_flag)
        print("on msg", self.MG.msg)

    def __init__(self, broker_address, clientname):
        self.client = mqtt.Client(clientname)  # create new instance
        self.client.connect(broker_address)
        self.brokerAddress = broker_address
        self.client.on_message = self.on_message
        self.MG = None



    def write(self,topic,msg):
            time.sleep(1)
            self.client.publish(topic, msg,retain=True)




con = MQTT(broker_address='127.0.0.1', clientname='P1')



for _ in range(30):
    con.write('test/target1/5', 'el3')









