import types
from unittest import mock

class A(object):#but seems to work for old style objects too
    def funcx(self,x):
        print("x1=",x)
        print("called from", self)

    def method(self,x):
        print("xmethod=",x)
        print("called from", self)

def patch_me(target):
    def method(target,x):
        print("x=",x)
        print("called from", target)
        target.method = types.MethodType(method,target)

def method(self,x):
    print("x=",x)
    print("called from", self)

@mock.patch("__main__.A")
def funcx(self,x):
    print("new x=",x)
    print("called from", self)
        
A.method=method
#add more if needed
a = A()
print(A.__dict__)
print(a)
#out: <__main__.A object at 0x2b73ac88bfd0>  

@mock.patch("__main__.a")
def funcx(self,x):
    print("x=",x)
    print("called from", self)
 
a.funcx(3)
patch_me(a)    #patch instance
a.method=method
#a.method(5)
#out: x= 5
#out: called from <__main__.A object at 0x2b73ac88bfd0>
patch_me(A)

a.method(6)        #can patch class too
#out: x= 6
#out: called from <class '__main__.A'>
