# code to mock inputs from Android app to database: user login, user creation, display measurements
import socket, sys, time

# Android send packets
loginPacketType = 0
retryLoginPacketType = 1
newUserCreationPacketype = 2
newMeasurementPacketType = 3

# Android receive packets
noUserPacketType = 5
addedMeasurementSuccessfulPacketType = 8
measurementPacketType = 9

temp = 99
packetLoad = None
username = None


def sendAndReceive(data):
    global temp 
    global packetLoad

    host = '192.168.43.231'
    port = 1050
    server_address = (host, port)
    host_address = ('192.168.43.128', 53477)

    #create socket
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.bind(host_address)

    # send packet to database Pi
    s.sendto(data, server_address)
    print('sent packet')
    #time.sleep(10)

    buf, address = s.recvfrom(2048)
    print ("Received %s bytes from %s %s: " % (len(buf), address, buf ))

    temp = chr(buf[0])
    print('temp in func is: ' + temp)
    packetLoad = buf
    print('packetload in func is: ' + str(packetLoad))

def formatPacket(type, value):

    #format packet
    if len(value) == 10:
        temp = "" + str(type) + "" + str(value) + ""
    else:
        print('passed an array to the format packet function')
        temp = "" + str(type) + "" + str(value[0]) + str(value[1]) + str(value[2]) + ""

    byteArray = bytearray(temp, 'utf8')

    # call sendMeasurements() with proper packet format
    sendAndReceive(byteArray)
    

def displayMeasurements():
    print('hi')
    # display payload of packet  

def handlePackets():
    
     #Check return packet type - handle cases 
    print('printing receive packet type: ' + temp)   
    if temp == str(5):
        print('No user found, creating new user')
        formatPacket(newUserCreationPacketype, username)
    if temp == str(8): 
        print('Added measurement successfully')
        print(str(packetLoad))
        packetLoadFinal = packetLoad.decode('utf-8')
        length = packetLoadFinal[1]
        c1 = packetLoadFinal[2]
        c2 = packetLoadFinal[3]
        print("The measurements entered are: Length: %s, Circumference 1: %s, Circumference 2: %s" % (length, c1, c2))
    elif temp == str(9):
        print('Hi: ' + username + "! \n")
        #Parse packet
        print(str(packetLoad))
        packetLoadFinal = packetLoad.decode('utf-8')
        length = packetLoadFinal[1]
        c1 = packetLoadFinal[2]
        c2 = packetLoadFinal[3]
        print("Your measurements are: Length: %s, Circumference 1: %s, Circumference 2: %s" % (length, c1, c2))
    else:
        quit()



    
def main():

    measurements = [6,6,6]

    while True:

        #mocking a login
        #CHANGE TO ASK FOR USER INPUT
        global username
        username = 'ababababka'

        if username is not None:
            formatPacket(loginPacketType, username)
            handlePackets()
            


        #if measurements is not None:
        print('calling format packet with measurements array')
        formatPacket(newMeasurementPacketType, measurements)
        handlePackets()


   


main()

