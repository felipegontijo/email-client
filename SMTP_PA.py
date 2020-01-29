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

'''
@pre   secureClientSocket created. secure connection established
    Same as sendToServer, but through a secure connection instead
@param   secureClientSocket
@param   info - the message/data to be sent to the Server
@param   expectedReplyMessage - the reply message expected for 'info'
'''
def sendSecure(secureClientSocket, info, expectedReplyMessage):
    secureClientSocket.send(info.encode())
    recv = secureClientSocket.read(1024).decode()
    print(recv)
    if recv[:3] != expectedReplyMessage :
        print('%s reply not received from server.'%(expectedReplyMessage))

'''
@pre    secure connection stablished, and second HELO message sent
@post   authentication completed. MAIL FROM and RCPT TO requests sent.
    Goes through the authentication process, requesting the user's username and password.
    Sends MAIL FROM and RCPT TO requests.
@param  secureClientSocket
'''
def authenticate(secureClientSocket):

    sendSecure(secureClientSocket, 'AUTH LOGIN\r\n', '334')

    username = input('Enter your Outlook email address: ')
    secureClientSocket.send(base64.b64encode(username.encode()) + '\r\n'.encode())
    recv5 = secureClientSocket.read(1024).decode()
    print(recv5)
    if recv5[:3] != '334':
        print('334 reply not received from server.')


    password = input('Enter your Outlook password: ')
    secureClientSocket.send(base64.b64encode(password.encode()) + '\r\n'.encode())
    recv6 = secureClientSocket.read(1024).decode()
    print(recv6)
    if recv6[:3] != '235':
        print('235 reply not received from server.')

    #username put as the username previously asked to the user
    mailFrom = 'MAIL FROM: <' + username + '>\r\n'
    sendSecure(secureClientSocket, mailFrom, '250')

    recipient = input('Enter the destination email address: ')
    rcpt = 'RCPT TO: <' + recipient + '>\r\n'
    sendSecure(secureClientSocket, rcpt, '250')

'''
@pre    user authentication successfully complete
@post   complete email message acquired
    Function to begin building the email itself. Sends DATA message request
    to server, creates a MIME object, fills the headers and the body of the email.
@param  secureClientSocket
@return msgString the message converted into a string
'''
def writeMail(secureClientSocket):

    sendSecure(secureClientSocket, 'DATA\r\n', '354')

    msg = MIMEMultipart()

    msg['From'] = input('From: ')
    msg['To'] = input('To: ')
    msg['Subject'] = input('Subject: ')

    body = input('Type your mail: ')
    message = MIMEText(body, 'plain')
    msg.attach(message)

    #converts msg into string as send() function requires it to be a string
    msgString = msg.as_string()
    return msgString

'''
@pre   complete email message acquired. message converted into a string.
@post  message sent
    Sends the email message
@param secureClientSocket
@param msgString  the email message as a string
'''
def sendMail(secureClientSocket, msgString):

    secureClientSocket.send(msgString.encode() + '\r\n'.encode() + '.\r\n'.encode())
    recv10 = secureClientSocket.read(1024).decode()
    print(recv10)
    if recv10[:3] != '250':
        print('250 reply not received from server')

'''
@pre    secureClientSocket created. secure connection established.
    Ends the current secure connection by sending the QUIT message to the server.
@param  secureClientSocket
'''
def endSecureConnection(secureClientSocket):

    secureClientSocket.send('QUIT\r\n'.encode())
    recv11 = secureClientSocket.read(1024).decode()
    print(recv11)
    if recv11[:3] != '221':
        print('221 reply not received from server')

'''
    The function main
'''
def main():

    #defines the mailserver here for easier maintenance
    mailserver = 'outlook.com'

    #creates the socket
    clientSocket = socket(AF_INET, SOCK_STREAM)

    #calls openSocket with the two previously created 'variables'
    openSocket(clientSocket, mailserver)

    #closes the socket
    clientSocket.close()