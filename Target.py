from datetime import datetime
import math
import scipy.optimize
from scipy.spatial import distance
import numpy as np
import sys

def great_circle_distance(ax, ay, bx, by, radius):
    a = (ax, ay)
    b = (bx, by)
    d = distance.euclidean(a, b)

    print("value for arcsin", (d / (2 * radius)))

    while d / (2 * radius) > 1:
        d -= 0.1

    phi = math.asin(d / (2 * radius))  # math.asin(x)  -1<x<1!!!!

    return 2 * phi * radius


class Beacon:
    NoAnchor = 0  # number of class objects/anchors
    BeaconList = []  # list of references to class instances

    def __init__(self, x=None, y=None, anchorId=None):
        self.x = x
        self.y = y
        if anchorId is None:
            self.anchorId = Beacon.NoAnchor + 1
        else:
            self.anchorId = anchorId

        self.distanceTab = []  # distance from self to each target
        self.tag = 'anchor'

        Beacon.NoAnchor += 1
        Beacon.BeaconList.append(self)

    def __str__(self):
        return f'X,Y:{self.x, self.y} ID {self.anchorId}'

    # to do : find better way to do that
    @classmethod
    def FindWithID(cls, anchorId):  # given ID of Anchor, return the anchor
        for v in Beacon.BeaconList:
            if v.anchorId == anchorId:
                return v


class Tar:
    NoTarget = 0
    TargetList = []

    def __init__(self, tarid):
        self.targetID = tarid
        self.x = 0
        self.y = 0
        self.tag = 'target'
        self.distanceTab = []

        Tar.NoTarget += 1
        Tar.TargetList.append(self)

    @staticmethod
    def mse(x, locations, distances):
        mse = 0.0

        for location, dist in zip(locations, distances):
            print("anchor (x,y) , dist to target")
            print("     ", location, dist)
            print()
            distance_calculated = great_circle_distance(x[0], x[1], location[0], location[1], dist)

            mse += math.pow(distance_calculated - dist, 2.0)
        return mse / 3

    def Update(self,id):


        A1 = Beacon.FindWithID(id[0])  # strongest signal lvl
        A2 = Beacon.FindWithID(id[1])  # 2 nd
        A3 = Beacon.FindWithID(id[2])  # 3 rd

        locations = [(A1.x, A1.y), (A2.x, A2.y), (A3.x, A3.y)]

        distances = (self.distanceTab[id[0] - 1], self.distanceTab[id[1] - 1], self.distanceTab[id[2] - 1])

        initial_location = np.array([self.x, self.y])

        # mse= self.mse((self.x, self.y), locations, distances)

        # (x - a1.x)^2  + (y - a1.y)^2  = distanceTab[id[0]]

        result = scipy.optimize.minimize(
            self.mse,  # The error function
            initial_location,  # The initial guess
            args=(locations, distances),  # Additional parameters for mse
            method='L-BFGS-B',  # The optimisation algorithm
            options={
                'ftol': 1e-5,  # Tolerance
                'maxiter': 1e+7  # Maximum iterations
            })
        location = result.x
        print(f"ID{self.targetID}","P coordinates", location)
        self.x = location[0]
        self.y = location[1]

    def checkstate(self, lastseen):

        lastseen = datetime.strptime(lastseen, '%d/%m/%Y %H:%M:%S')

        delta = datetime.now() - lastseen
        print(delta.total_seconds())
        if delta.total_seconds() > 28800:
            return 'expired'
        if delta.total_seconds() > 180:
            return 'criticallost'
        if delta.total_seconds() > 30:
            return 'lost'
        else:
            return 'good'
