import Target
import time


Target.Beacon(x=20, y=40, id=1)
Target.Beacon(x=60, y=10, id=2)
Target.Beacon(x=5 , y=10, id=3)
Target.Beacon(x=20, y=20, id=4)


x = Target.Tar(1)

x.distanceTab = [30, 50, 6, 22, 0, 0]
x.Update((1, 2, 3))






