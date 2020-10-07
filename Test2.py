import paho.mqtt.client as mqtt
import time
import timeit

class MQTT:
    class ReceivedMessage:
        def __init__(self, msg, topic, msgQoS, retain_flag):
            self.msg = str(msg)
            self.topic = topic
            self.msgQos = msgQoS
            self.retain_flag = retain_flag

        def __str__(self):
            return self.msg + f" and retan lfag {self.retain_flag}"

    def on_message(self, client, userdata,message):


        msg = message.payload.decode("utf-8")
        topic = message.topic
        msgQoS= message.qos
        retain_flag= message.retain

        self.msg = MQTT.ReceivedMessage(msg,topic,msgQoS,retain_flag)



    def __init__(self,broker_address, clientname):
        self.client = mqtt.Client(clientname)  # create new instance
        self.client.connect(broker_address)
        self.brokerAddress = broker_address
        self.client.on_message = self.on_message
        self.msg = None




    def read(self):

        self.client.loop_start()
        time.sleep(0.01)
        self.client.loop_start()
        return self.msg




if __name__ == '__main__':

    con = MQTT(broker_address='127.0.0.1', clientname='P1')
    con.client.subscribe('test/target1/5')


    start = timeit.timeit()
    for _ in range(10):
        print(con.read())

    print('h')
    end = timeit.timeit()
    print(end - start)


