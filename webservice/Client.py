from EchoServer_services import *
import sys, time

loc  = EchoServerLocator()
port = loc.getEchoServer(url='http://happy3/webservice/Server.py')

print "Echo: ", 
msg = EchoRequest()
msg.Value = "Is there an echo in here?"
rsp = port.Echo(msg)
print rsp.Value
