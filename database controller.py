# receive
# decide what packet it is/check error
# save username it came from
# if it is log in packet, query table for username
# ii) parse SQL return then if user found send a packet back and save the user in a variable here
# iii) if user not found then send a packet asking if u want new user creation
#
# if its a packet from the same username:
# return all packet: this should return a select * from table
# return latest : return the latest record with the username
# newUserPacket: insert new user record
#
# submitMeasurements packet: do a insert in the table with the username that we have
#

import sys
import socket
import sqlite3
import time
from sqlite3 import Error

messageSize = 1024  # 1kb

# stage 1 constants
logIn = str(0)
retryLogin = 12
newUser = 2
newMeasurement = str(3)
easterEgg = 15

# stage 2 constants
NOUSERTYPE = 5
RETRYLOGINTYPE = 6000
MAXLOGINTYPE = 7
FINISHEDMEASUREMENT = 8
ALLMEASUREMENTTYPE = 9
BADUSERNAME = 1
BADBYTES = 6
BADPARSE = 4


sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# making a socket
sock.bind(("192.168.43.231", 1050))  # this takes ipAddr and port


def initializesql(sqldb):
    try:
        conn = sqlite3.connect(sqldb)
        return conn
    except Error as e:
        print(e)

        return None


def parsePacket(data):
    # assuming no error on packet
    # get the packet type
    typeVar = chr(data[0])
    returnMessage = ""
    print("the typeVar is "+typeVar)
    #typeVar=2
    print(typeVar ==str(2))

    if (typeVar == logIn):
        returnMessage = login(data)
    elif (typeVar == retryLogin):
        returnMessage = retryLogin(data)
    elif (typeVar ==str(2)):
        print("executing this thing")
        returnMessage = newUser(data)
    elif (typeVar == str(3)):
    
        returnMessage = newMeasurement(data)
    elif (typeVar == easterEgg):
        returnMessage = easterEgg()
    else:
        returnMessage="didnt know what to return"

    return returnMessage


def choice(choice):
    if choice == "more than  username exists":
        payload = 10 # this is an enumeration
    elif choice == "no user":
        payload = NOUSERTYPE
    elif choice == "max Logins":
        payload = MAXLOGINTYPE
    elif choice == "finishedNewMeasurement":
        payload = FINISHEDMEASUREMENT
    elif choice == "easterEgg":
        payload = easterEgg
    elif choice== "badUsername":
        payload = BADUSERNAME
    elif choice == "didnt know what to return":
        payload = BADPARSE
    elif choice=="badbytes":
        payload = BADBYTES

    else:
        payload = choice  # after successful login
        
    print("the choice function returned"+ str(payload))

    return payload


def login(data):
    print("entering log in ")
    badLogin = False
    if len(data) >11:
        badLogin = True
        #send a bad usernamePacket then leave login function 
    sqlCommand = "Select * from usernamesAndMeasurements where username=?"
    username = data[1:11]
    print(username.decode('utf-8'))


    cursor.execute(sqlCommand,(username.decode('utf-8'),))
    records = cursor.fetchall()
    
    if badLogin == True:
        return "badUsername"
    elif len(records) == 1:
        return username.decode('utf-8')
    elif len(records)  > 1:
        return "more than  username exists"
    else:
        return "no user"
    



def retryLogin(data):
    global count
    count = count + 1  # this variable is not global
    if count <= 3:
        return login(data)
    else:
        count = 0
        return "max Logins"


def newUser(data):
    print("getting ready to insert a nwe username")
    sqlCommand = "INSERT INTO usernamesAndMeasurements(username) VALUES (\"?\")"
    newUser = data[1:11]
    newUser2 = newUser.decode('utf-8')
    print(newUser2)
    with sqlConnection:
        cursor.execute("INSERT INTO usernamesAndMeasurements(username) VALUES (?)", (newUser2,))
        
  
    sqlConnection.commit()
    login(data)


def newMeasurement(data):
    #delete old measurement
    sqlCommand = "DELETE FROM usernamesAndMeasurements WHERE username=? "
    sqlCommand2 = "INSERT INTO usernamesAndMeasurements (userNames,armLength,circum1,circum2) VALUES (?,?,?,?)"
    print(data)
    for i in range(len(data)):
        print(data[i])
        if data[i] is None:
            return "badbytes"
    username = data[1:11]
    armLength = data[11]
    circum1 =data[12]
    circum2 = data[13]
    cursor.execute(sqlCommand,(username.decode('utf'),))
    cursor.execute(sqlCommand,(username.decode('utf'),armLength,circum1,circum2))
    return "finishedNewMeasurement"


def easterEgg():
    return "easterEgg"


def sendBackAllMeasurements(username):
    sqlCommand = "Select * from usernamesAndMeasurements where username=?"
    print("the username is " + username)
    #cursor = sqlConnection.cursor()
    cursor.execute(sqlCommand, (username,))
    records = cursor.fetchall()
    #payload = "" + str(ALLMEASUREMENTTYPE) + "" + str(len(records))  # make sure they are strings
    payload = "" + str(ALLMEASUREMENTTYPE)
    print("checkpoint 2")
    print("payload is "+payload)
    print(records)
    for i in range(len(records)):
        #payload += "xxxx"
        armLength, circum1, circum2 = parseSQLRrow(records[i])
       # payload += ((armLength.length + "armLength".size) + "armLength" + armLength + (
              #      circum1.length + circum1.length) + "circum1" + circum1 + (
                           #     circum2.length + circum2.length) + "circum2" + circum2)
        payload += str(armLength)+str(circum1)+str(circum2)
        
    print("payload again is "+payload)
    return payload


def parseSQLRrow(parsePacketrecord):
    armlength = parsePacketrecord[1]
    circum1 = parsePacketrecord[2]
    circum2 = parsePacketrecord[3]

    return (armlength, circum1, circum2)


# python is stupid
# get SQL initialized
sqlConnection = initializesql("/home/pi/eztables.db")
cursor = sqlConnection.cursor()
#sqlite3.autocommit(True)

while (True):
    
    print("start of loop")
    counter = 0
    print("printing all the rows in the table")
    tempDeleteme= "katiedonke"
    cursor.execute("Select * from usernamesAndMeasurements ")
    print(cursor.fetchall())
    cursor.execute("DELETE FROM usernamesAndMeasurements WHERE username=?",(bytes(str(tempDeleteme), 'utf-8'),))
    sqlConnection.commit()
    #print("trying to insert the thing")
    #cursor.execute("INSERT INTO usernamesAndMeasurements (username,armLength,circum1,circum2) VALUES (\"ababababka\",1,2,2)")
   # "INSERT INTO usernamesAndMeasurements (userNames,armLength,circum1,circum2) VALUES (\"ababababka\",1,2,2)"
   # sqlConnection.commit()
    #print("insert done")
    #cursor.execute("Select * from usernamesAndMeasurements ")
    #print(cursor.fetchall())
    
    
    
    # Receive packet
    data, address = sock.recvfrom(messageSize)# needs timeouts
    address2 = "192.168.43.128"
    port2 = 53477
    katie_address= (address2,port2)
    time.sleep(1)
    
   # try:
      #  sock.sendto(bytes("hi", 'utf-8'), katie_address)
     # sock.sendto(bytes(str(payload), 'utf-8'), katie_address) 
    #except Exception:
    #   print("failed test sending")
        
    print(data)
    print(address)

    # forTEsting
   # data = "123"
    #address = ("127.0.0.1", 1234)

    # parsePacket
    payload = choice(parsePacket(data))
    print("checkpoint 1")
    print(payload)
    time.sleep(2)

    # do things based on payload #tip for refactoring code: dont need all the elifs, just check if the payload length is more than 1
    try: 
  
        if payload == NOUSERTYPE:
                                          
            print("sending a no user type")
            sock.sendto(bytes(str(payload), 'utf-8'), katie_address)  ##might need try catch block for sending
            print("sent complete")
            
        elif payload == MAXLOGINTYPE:
            sock.sendto(payload, address)
        elif payload == FINISHEDMEASUREMENT:
            sock.sendto(payload, address)
        elif payload == easterEgg:
            sock.sendto(payload, address)
        elif payload == BADUSERNAME or payload==BADPARSE or payload == BADBYTES:
            sock.sendto(bytes(str(payload), 'utf-8'),katie_address)
            
        else:
            print("trying to send measurements")
            sock.sendto(bytes(sendBackAllMeasurements(payload), 'utf-8'), katie_address)
    except Exception as e:
                print(e)
    









