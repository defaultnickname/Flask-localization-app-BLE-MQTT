import Target
import MQTT_READ
import sys
import math


def idxfor3smallest(list):
    lcopy = list.copy()
    tmp = []

    for _ in range(3):
        i_i = lcopy.index(min(lcopy))
        tmp.append(i_i)
        lcopy[i_i] = sys.maxsize

    return [x + 1 for x in tmp]


def letsgobaby(anchor, targetfromflask):
    host = 'localhost'
    port = 1883
    con = MQTT_READ.MQTT(broker_address=host, port=port, clientname='Dzungar1')

    anchorlist = []
    targetlist = targetfromflask

    for item in anchor:
        _anchor = Target.Beacon(item['x'], item['y'])
        anchorlist.append(_anchor)



    for target in targetlist:
        target.distanceTab = []
        for i, anchor in enumerate(anchorlist):
            topic = "test/" + str(target.targetID) + "/" + str(i + 1)
            print(f'Topic we read from for {target}',topic)
            v = con.read(topic)

            target.distanceTab.append(float(v.msg))

        l = idxfor3smallest(target.distanceTab)
        print(f'Indexes for trilateration of {target}',l)
        print(f'Target{target} distance tab',target.distanceTab)
        target.Update(l)

        print("Target XY ", target.x, target.y)
        t = 'test/front/' + str(target.targetID)
        print('Topic published to : ',t)
        con.publish(t, str(math.floor(target.x)) + " " + str(math.floor(target.y)) + " " + str(target.targetID), retain = False )

        print("Python calculated position and send it")

# Topic structure  test / *Target ID* / *Anchor ID*-,-
# pobierz dane o anchorach
# pobierz dane o targetach
# pobierz dane o dystansach
# policz pozycje
# wyślij dane o pozycji
