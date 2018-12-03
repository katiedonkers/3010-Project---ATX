# Tuesday-5 
# This program acts as the database controller, it receives a packet 
# and based on the type field it executes different operations.

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

#stage 1
def parsePacket(data):
    # assuming no error on packet
    # get the packet type
    typeVar = chr(data[0])
    returnMessage = ""
    print("the typeVar is "+typeVar)

    if (typeVar == logIn):
        returnMessage = login(data)
    elif (typeVar == retryLogin):
        returnMessage = retryLogin(data)
    elif (typeVar ==str(2)):
        returnMessage = newUser(data)
    elif (typeVar == str(3)):   
        returnMessage = newMeasurement(data)
    else:
        returnMessage="didnt know what to return"
    print("parsePacket is returning "+ str(returnMessage))

    return returnMessage

#stage 2
def choice(choice):
    if choice == "more than  username exists":
        payload = 10 
    elif choice == "no user":
        payload = NOUSERTYPE
    elif choice == "max Logins":
        payload = MAXLOGINTYPE
    elif choice == "finishedNewMeasurement":
        payload = FINISHEDMEASUREMENT
    elif choice== "badUsername":
        payload = BADUSERNAME
    elif choice == "didnt know what to return":
        payload = BADPARSE
    elif choice=="badbytes":
        payload = BADBYTES

    else:
        payload = choice  # after successful login
        
    print("the choice function returned"+ str(payload)) #for debugging purposes

    return payload


#if the database finds that username, return it. If not, return an error message.
def login(data):
    print("entering log in ")
    badLogin = False
    if len(data) >11:
        badLogin = True
    sqlCommand = "Select * from usernamesAndMeasurements where username=?"
    username = data[1:11]
    print(username.decode('utf-8')) #for debugging

    cursor.execute(sqlCommand,(username.decode('utf-8'),))
    records = cursor.fetchall()
    print("the length of the records is "+ str(len(records)))
    
    if badLogin == True:
        return "badUsername"
    elif len(records) == 1:
        print("we are about to return username")
        return username.decode('utf-8')
    elif len(records)  > 1:
        return "more than  username exists"
    else:
        return newUser(data)
    
#Not implemented on client side
def retryLogin(data):
    global count
    count = count + 1  # this variable is not global
    if count <= 3:
        return login(data)
    else:
        count = 0
        return "max Logins"

#Adds a user to the database then logs in with that user
def newUser(data):
    print("getting ready to insert a new username") #debugging logs
    newUser = data[1:11].decode('utf-8')
    print(newUser)
    with sqlConnection:
        cursor.execute("INSERT INTO usernamesAndMeasurements(username,armLength,circum1,circum2) VALUES (?,?,?,?)", (newUser,0,0,0))
        
  
    sqlConnection.commit()
    return login(data)

#Deletes any old measurement attached to that username, then adds a new one. If the new measurement contains null return a bad bytes message
#Returns a success message 
def newMeasurement(data):
    print("entering new measurement")
    #delete old measurement
    sqlCommand = "DELETE FROM usernamesAndMeasurements WHERE username=? "
    sqlCommand2 = "INSERT INTO usernamesAndMeasurements (username,armLength,circum1,circum2) VALUES (?,?,?,?)"
    #print(data)
    for i in range(len(data)):
        #print(data[i])
        if data[i] is None:
            return "badbytes"
    username = data[1:11]
    armLength = data[11:13]
    circum1 =data[13:15]
    circum2 = data[15:17]#might be out of range
    cursor.execute(sqlCommand,(username.decode('utf'),))
    cursor.execute(sqlCommand2,(username.decode('utf'),int(armLength),int(circum1),int(circum2)))
    sqlConnection.commit()
    return "finishedNewMeasurement"



def sendBackAllMeasurements(username):
    sqlCommand = "Select * from usernamesAndMeasurements where username=?"
    print("the username is " + username) #debugging logs
    cursor.execute(sqlCommand, (username,))
    records = cursor.fetchall()
    #payload = "" + str(ALLMEASUREMENTTYPE) + "" + str(len(records))  #for multi measurement implementation
    payload = "" + str(ALLMEASUREMENTTYPE)+ username
    #print("checkpoint 2") #debugging logs
    print("payload is "+payload)
    print(records)
    for i in range(len(records)): #for multi-measurement implementation
        #payload += "xxxx" 
        armLength, circum1, circum2 = parseSQLRrow(records[i])
       # payload += ((armLength.length + "armLength".size) + "armLength" + armLength + (
              #      circum1.length + circum1.length) + "circum1" + circum1 + (
                           #     circum2.length + circum2.length) + "circum2" + circum2)
        payload +=  str(armLength)+str(circum1)+str(circum2)
        
    print("payload again is "+payload)
    return payload

#a method to get retrieve info from database record
def parseSQLRrow(parsePacketrecord):
    armlength = parsePacketrecord[1]
    circum1 = parsePacketrecord[2]
    circum2 = parsePacketrecord[3]

    return (armlength, circum1, circum2)


##############################################################################

#                          S T A R T  O F  M A I N                           #

##############################################################################

# get SQL initialized
sqlConnection = initializesql("/home/pi/eztables.db")
cursor = sqlConnection.cursor()
#sqlite3.autocommit(True)

while (True):
    
    print("start of loop")
    #counter = 0
    print("printing all the rows in the table")
    cursor.execute("Select * from usernamesAndMeasurements ")
    print(cursor.fetchall())
        
    # Receive packet
    data, address = sock.recvfrom(messageSize)# needs timeout
    time.sleep(1)     
    print(data)
    print(address)

    # parsePacket
    payload = choice(parsePacket(data))
    print("The payload is "+str(payload))
    time.sleep(2)

    # Send back a packet based on payload value, needs refactoring (unneeded if cases)
    try:  
        if payload == NOUSERTYPE or payload == MAXLOGINTYPE or payload == FINISHEDMEASUREMENT or payload == BADUSERNAME or payload==BADPARSE or payload == BADBYTES :   #not implemented in client                                        
            sock.sendto(bytes(str(payload), 'utf-8'), address)  
            
        else: #its a request to show measurements
            print("trying to send measurements")
            sock.sendto(bytes(sendBackAllMeasurements(payload), 'utf-8'), address)
            
    except Exception as e:
                print(e)
            
            
    #code for database quick access
    #cursor.execute("DELETE FROM usernamesAndMeasurements WHERE username=?",(bytes(str(tempDeleteme), 'utf-8'),))
    #sqlConnection.commit()
    #print("Inserting record")
    #cursor.execute("INSERT INTO usernamesAndMeasurements (username,armLength,circum1,circum2) VALUES (\"ababababka\",1,2,2)")
    #"INSERT INTO usernamesAndMeasurements (userNames,armLength,circum1,circum2) VALUES (\"ababababka\",1,2,2)"
    #sqlConnection.commit()
    #print("insert done")
    










