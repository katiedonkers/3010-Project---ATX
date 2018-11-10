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
from sqlite3 import Error

messageSize = 1024  # 1kb

# stage 1 constants
logIn = 0
retryLogin = 1
newUser = 2
newMeasurement = 3
easterEgg = 4

# stage 2 constants
NOUSERTYPE = 5
RETRYLOGINTYPE = 6
MAXLOGINTYPE = 7
FINISHEDMEASUREMENT = 8
ALLMEASUREMENTTYPE = 9

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# making a socket
sock.bind(('localhost', 1050))  # this takes ipAddr and port


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
    typeVar = data[2]
    returnMessage = ""

    if (typeVar == logIn):
        returnMessage = login(data)
    elif (typeVar == retryLogin):
        returnMessage = retryLogin(data)
    elif (typeVar == newUser):
        returnMessage = newUser(data)
    elif (typeVar == newMeasurement):
        returnMessage = newMeasurement(data)
    elif (typeVar == easterEgg):
        returnMessage = easterEgg()

    return returnMessage


def choice(choice):
    if choice == "more than  username exists":
        payload = 9 # this is an enumeration
    elif choice == "no user":
        payload = NOUSERTYPE
    elif choice == "max Logins":
        payload = MAXLOGINTYPE
    elif choice == "finishedNewMeasurement":
        payload = FINISHEDMEASUREMENT
    elif choice == "easterEgg":
        payload = easterEgg

    else:
        payload = choice  # after successful login

    return payload


def login(data):
    sqlCommand = "Select * from usernamesAndMeasurements where Username="
    username = ""
    if data.substring(userIs.size) == "userIS":
        username = data
    else:
       # usernamestart = findStartandEnd(data, username)
        username = data[2:13]

    sqlCommand += username

    cursor.execute(sqlCommand)
    records = cursor.fetchall()

    if records.size == 1:
        return username
    elif records.size > 1:
        return "more than  username exists"
    else:
        return "no user"


def retryLogin(data):
    count = count + 1  # this variable is not global
    if count <= 3:
        return login(data)
    else:
        return "max Logins"


def newUser(data):
    sqlCommand = "INSERT INTO usernamesAndMeasurements(userNames) VALUES (?"
    newUser = data.substring(findStartAndEnd(data, "newUser"))
    sqlCommand += newUser + "\")"
    cursor.execute(sqlCommand)
    # return "successFul newUserCreation"
    login("userIs" + newUser)


def newMeasurement(data):
    sqlCommand = "INSERT INTO usernamesAndMeasurements (userNames,armLength,circum1,circum2) VALUES (\""
    username = data.substring(findStartandEnd(data, "userName"))
    armLength = data.substring(findStartandEnd(data, "armLength"))
    circum1 = data.substring(findStartandEnd(data, "circum1"))
    circum2 = data.substring(findStartandEnd(data, "circum2"))
    sqlCommands += "\"" + armLength + ",\"" + circum1 + ",\"" + circum2 + ")"
    cursor.execute(sqlCommands)
    return "finishedNewMeasurement"


def easterEgg():
    return "easterEgg"


def sendBackAllMeasurements(username):
    sqlCommand = "Select * from usernamesAndMeasurements where Username=?"
    cursor = sqlConnection.cursor()
    cursor.execute(sqlCommand, (username,))
    records = cursor.fetchall()
    payload = "" + str(ALLMEASUREMENTTYPE) + "" + str(len(records))  # make sure they are strings
    for i in range(len(records)):
        payload += "xxxx"
        armLength, circum1, circum2 = parseSQLrow(records[i])
        payload += ((armLength.length + "armLength".size) + "armLength" + armLength + (
                    circum1.length + circum1.length) + "circum1" + circum1 + (
                                circum2.length + circum2.length) + "circum2" + circum2)
    return payload


def parseSQLRrow(record):
    armlength = record[1]
    circum1 = record[2]
    circum2 = record[3]

    return (armlength, circum1, circum2)


# python is stupid
# get SQL initialized
sqlConnection = initializesql("/home/pi/eztables.db")
cursor = sqlConnection.cursor()
while (True):
    counter = 0
    # Receive packet
    # data, address = sock.recvfrom(messageSize)  # needs timeouts

    # forTEsting
    data = "123"
    address = ("127.0.0.1", 1234)

    # parsePacket
    payload = choice(parsePacket(data))

    # do things based on payload

    if payload == NOUSERTYPE:
        sock.sendto(payload, address)  ##might need try catch block for sending
    elif payload == MAXLOGINTYPE:
        sock.sendto(payload, address)
    elif payload == FINISHEDMEASUREMENT:
        sock.sendto(payload, address)
    elif payload == easterEgg:
        sock.sendto(payload, address)
    else:
        sock.sendto(bytes(sendBackAllMeasurements(payload), 'utf-8'), address)






