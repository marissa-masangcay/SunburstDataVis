import csv
import json
import numpy as np


def get_median(self):
    med = 0
    i = 0
    medList = []
    for c in self.children:
        if c.rain is not None:
            medList.append(float(c.rain))
        if c.rainTotal is not None:
            medList.append(float(c.rainTotal))
    med = np.median(medList)
    return med


def get_max(self):
    tmp_max = 0
    for c in self.children:
        if c.max > tmp_max:
            tmp_max = c.max
    self.max = tmp_max
    return tmp_max

def get_average(self):
    ave = 0
    rainTotal = 0
    numVals = 0
    for c in self.children:
        if c.rain is not None:
            rainTotal += float(c.rain)
        if c.rainTotal is not None:
            rainTotal += float(c.rainTotal)
        numVals += 1
    ave = float(rainTotal/numVals)
    self.average = ave
    return ave


def get_total(self):
    rainTotal = 0
    for c in self.children:
        if c.rain is not None:
            rainTotal += float(c.rain)
        if c.rainTotal is not None:
            rainTotal += float(c.rainTotal)
    self.rainTotal = rainTotal
    return rainTotal


class Node(object):
    def __init__(self, name, rain=None):
        self.name = name
        self.children = []
        self.rain = rain
        self.max = rain
        self.average = rain
        self.rainTotal = 0
        self.median = 0

    def child(self, cname, rain=None):
        child_found = [c for c in self.children if c.name == cname]
        if not child_found:
            _child = Node(cname, rain)
            self.children.append(_child)
        else:
            _child = child_found[0]
        return _child

    def as_dict(self):
        res = {'name': self.name}
        if self.rain is None:
            res['children'] = [c.as_dict() for c in self.children]
            res['max'] = get_max(self)
            res['average'] = get_average(self)
            res['rainTotal'] = get_total(self)
            res['median'] = get_median(self)
        else:
            res['rain'] = self.rain
        return res

root = Node('Root')

with open('raindata_fullPICH.csv', 'r') as f:
    reader = csv.reader(f)
    reader.next()
    for row in reader:
        year, month, day, hour, minute, city = row
        root.child(year).child(month).child(day).child(hour).child(minute, city)

root.as_dict()

print json.dumps(root.as_dict(), indent=4)

with open('raindata_fullPICH.json', 'w') as writer:
    writer.write(json.dumps(root.as_dict()))
