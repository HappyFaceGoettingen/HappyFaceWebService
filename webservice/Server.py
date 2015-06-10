import os
import sys
from EchoServer_services import *
from ZSI.twisted.wsgi import (SOAPApplication,
                              soapmethod,
                              SOAPHandlerChainFactory)

class EchoService(SOAPApplication):
    factory = SOAPHandlerChainFactory
    wsdl_content = dict(name='Echo', 
                        targetNamespace='urn:echo', 
                        imports=(), 
                        portType='',
                        )

    def __call__(self, env, start_response):
        self.env = env
        return SOAPApplication.__call__(self, env, start_response)

    @soapmethod(EchoRequest.typecode, 
                EchoResponse.typecode, 
                operation='Echo', 
                soapaction='Echo')
    def soap_Echo(self, request, response, **kw):
        # Just return what was sent
        response.Value = request.Value
        return request, response

def main():
    from wsgiref.simple_server import make_server
    from ZSI.twisted.wsgi import WSGIApplication

    application         = WSGIApplication()
    httpd               = make_server('', 7000, application)
    application['echo'] = EchoService()
    print "listening..."
    httpd.serve_forever()

if __name__ == '__main__':
    main()

