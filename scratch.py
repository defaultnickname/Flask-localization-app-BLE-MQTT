import pickle

class A(object):
    def __init__(self,x):
        self.x = x
    pass

obj = A(6)
print(obj.x)
print(obj)
pickled = pickle.dumps(obj)

_A = A; del A # hide class



A = _A # unhide class
b=pickle.loads(pickled)
print(b)
print(b.x)
