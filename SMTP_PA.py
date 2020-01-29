import ssl
import base64
from socket import *
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib

'''
@pre    clientSocket created.
@post   email sent and connection ended.
    Starts the connection with mailserver.
    Starts the secure connection with mailserver.
    Goes through the whole process of sending the email, from authenticating the user
    to ending the connection after the email has been sent.
@param  clientSocket - socket object
@param  mailserver - string
'''
def openSocket(clientSocket, mailserver):

    clientSocket.connect((mailserver, 587))
    recv = clientSocket.recv(1024).decode()
    print(recv)
    if recv[:3] != '250':
        print('250 reply not received from server.')

    sendToServer(clientSocket, 'HELO outlook.com\r\n', '250')

    sendToServer(clientSocket, 'starttls\r\n', '220')

    secureClientSocket = ssl.wrap_socket(clientSocket, ssl_version=ssl.PROTOCOL_SSLv23)

    sendSecure(secureClientSocket, 'HELO outlook.com\r\n', '250')

    authenticate(secureClientSocket)

    msgString = writeMail(secureClientSocket)

    sendMail(secureClientSocket, msgString)

    endSecureConnection(secureClientSocket)

'''
@pre     clientSocket created. connection established.
    Sends requests/information to the Server through a standard connection
@param   clientSocket
@param   info -  the message/data to be sent to the Server
@param   expectedReplyMessage - the reply message expected for 'info'
'''
def sendToServer(clientSocket, info, expectedReplyMessage):
    clientSocket.send(info.encode())
    recv = clientSocket.recv(1024).decode()
    print(recv)
    if recv[:3] != expectedReplyMessage :
        print('%s reply not received from server.'%(expectedReplyMessage))