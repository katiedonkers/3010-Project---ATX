#receive
#decide what packet it is/check error
# save username it came from
# if it is log in packet, query table for username
# ii) parse SQL return then if user found send a packet back and save the user in a variable here
# iii) if user not found then send a packet asking if u want new user creation
#
#if its a packet from the same username:
#return all packet: this should return a select * from table
#return latest : return the latest record with the username
#newUserPacket: insert new user record
#
#submitMeasurements packet: do a insert in the table with the username that we have
#

import sys
import socket
import sqlite3
from sqlite3 import Error

messageSize = 1024 #1kb

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

#making a socket
sock.bind('localhost',10000) #this takes ipAddr and port

#get SQL initialized
sqlConnection = initializesql(databaseName)
cursor=connection.cursor()
while(true):
    main()

        
def main():

    #Receive packet
    data, address = sock.recfrom(messageSize)#needs timeouts

    #parsePacket
    payload = choice(parsePacket(data))

    #do things based on payload
    if payload>TYPEENUMERATIONSLISTLENGTH :
        sock.sendTo(sendBackAllMeasurements(payload),address)
    else if payload==noUserpayloadtype:
        sock.sendTo(payload,address) ##might need try catch block for sending
    else if payload==maxLoginspayloadtype:
        sock.sendTo(payload,address)
    else if payload==finishedNewMeasurement:
        sock.sendTo(payload,address)
    else if payload==easterEggType:
        sock.sendTo(payload,address)
 
    
    
def intializeSql(sqlDB):
    try:
        conn = sqlite3.connect(sqlDB)
        return conn
    except Error as e:
        print(e)

        return None

def parsePacket(data):
    #assuming no error on packet
    #get the packet type
    typeVar = data[2]
    returnMessage=""

    if (typeVar == logIn) returnMessage=login(data)
    else if (typeVar == retryLogin) returnMessage=retryLogin(data)
    else if (typeVar== newUser) returnMessage=newUser(data)
    else if (typeVar == newMeasurement) returnMessage=newMeasurement(data)
    else if (typeVar == easterEgg) returnMessage=easterEgg()

    return returnMessage

def choice(choice):
    if choice=="more than  username exists":
        payload=THISTYPE #this is an enumeration
    else if choice == "no user":
        payload=THISTYPE
    else if choice=="max Logins":
        payload=THISTYPE
    else if choice=="finishedNewMeasurement":
        payload=THISTYPE
    else if choice == "easterEgg":
        payload=THISTYPE
                   
    else payload=choice#after successful login

    return payload



def login(data):
    message = ""
    if data.substring(userIs.size)=="userIS":
        sqlCommand+=data
    sqlCommand="Select * from ezTable where Username="
    usernamestart = findStartandEnd(data,username)
    username= data.substring(usernameStart[0],usernameStart[1])
    sqlCommand+= username
    
    cursor.execute(sqlCommand)
    records = cursor.fetchall()
    
    if records.size == 1:
        return username
    else if records.size>1:
        return "more than  username exists"
    else return "no user"

def retryLogin(data):
    count++
    if count<=3:
        return returnMessage=login(data)
    else:
        return returnMessage="max Logins"

def newUser(data):
    sqlCommand="INSERT INTO ezTable (userNames) VALUES (\""
    newUser=data.substring(findStartAndEnd(data,"newUser"))
    sqlCommand += newUser+"\")"
    cursor.execute(sqlCommand)
    #return "successFul newUserCreation"
    login("userIs"+newUser)

def newMeasurement(data):
    sqlCommand="INSERT INTO ezTable (userNames,armLength,circum1,circum2) VALUES (\""
    username=data.substring(findStartandEnd(data,"userName"))
    armLength=data.substring(findStartandEnd(data,"armLength"))
    circum1 = data.substring(findStartandEnd(data,"circum1"))
    circum2 = data.substring(findStartandEnd(data,"circum2"))
    sqlCommands += "\""+armLength+",\""+circum1+",\""+circum2+")"
    cursor.execute(sqlCommands)
    return "finishedNewMeasurement"

def easterEgg():
    return "easterEgg"


def getAllMeasurements(username):
    sqlCommand="Select * from ezTable where Username="+username
    cursor.execute(sqlCommand)
    records = cursor.fetchall()
    payload=ALLMEASUREMENTTYPE + records.length #make sure they are strings
    for (int i=0;i<records.length;i++):
        payload+="SPECIALCODETHATSPLITSTHeROWS"
        armLength,circum1,circum2 = parseSQLrow(records[i])
        payload +=  ((armLength.length+"armLength".size)+"armLength"+armLength+(circum1.length+circum1.length)+"circum1"+circum1+ (circum2.length+circum2.length)+"circum2"+circum2)
    return payload
        
    
    
    
    
    

    


