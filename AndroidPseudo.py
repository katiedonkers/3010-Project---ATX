# code to mock inputs from Android app to database: user login, user creation, display measurements

login = 0
newUserCreationPacketType = 2
noUserPacketType = 5
measurementsPacketType = 9
address
port

def sendAndReceiveDB():

    # get socket (Port, address) from database Pi
    # save and store in variable

    #send packet
    #delay
    #wait for receive packet
    #save packet in temp variable

def formatPacket():

    #call sendAndReceive() with proper packet format

def displayMeasurements():

    # display payload of packet    

def sendAndReceiveHeadlessPi():

    # MAIN

while true:

    # continuously check user input
    # if username, call formatPacket with Username
    # unpack temp packet
    # if packetType = noUser, call formatPacket with newUserCreation
    # else packetType = Measurements, call DisplayMeasurements()
    
    