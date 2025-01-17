import paho.mqtt.client as mqtt
import time


class MQTT:
    class ReceivedMessage:
        def __init__(self, msg, topic, msgQoS, retain_flag):
            self.msg = str(msg)
            self.topic = topic
            self.msgQos = msgQoS
            self.retain_flag = retain_flag

        def __str__(self):
            return self.msg + f" and retan lfag {self.retain_flag}"

    def on_message(self, client, userdata, message):
        msg = message.payload.decode("utf-8")
        topic = message.topic
        msgQoS = message.qos
        retain_flag = message.retain

        self.msg = MQTT.ReceivedMessage(msg, topic, msgQoS, retain_flag)

    def __init__(self, broker_address, clientname, port):
        self.client = mqtt.Client(clientname)  # create new instance
        self.client.connect(broker_address, port)
        self.brokerAddress = broker_address
        self.client.on_message = self.on_message
        self.msg = None

    def publish(self, topic, msg,qos = 0,retain=True):
        self.client.loop_start()
        self.client.publish(topic, msg, retain=retain,qos= qos)
        self.client.loop_stop()

    # time.sleep(1)

    def read(self, topic):
        self.client.subscribe(topic)
        self.client.loop_start()
        time.sleep(0.05)
        self.client.loop_start()
        return self.msg


if __name__ == "__main__":

    con = MQTT(broker_address='localhost', port=1883, clientname='P1')



    con.publish('test/1/2', '270')  # Anchor 2 publishes distance to Target 1


        # Topic structure  test / *Target ID* / *Anchor ID*
