import socket, sys, time

measurementsPacketFlag = 5 

# function to collect and send measurements from headless Pi to database Pi
def sendMeasurements():

    host = '192.168.1.31'
    port = 1003
    server_address = (host, port)

    #create socket
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.bind(server_address)

    # send packet to database Pi
    s.sendto(data.encode('utf-8'), server_address)

def formatPacket(data):

    #format packet
    temp = "" + measurementsPacketFlag + "" + data[0] + "" + data[1] + "" + data[2] + ""
    byteArray = bytearray(temp)

    # call sendMeasurements() with proper packet format
    sendMeasurements(byteArray)


#MAIN

#measurements array [] will contain length, circumf1 (wrist) circumf2 (elbow) 
while len(measurements) < 3:
    #wait

formatPacket(measurements)







    buf, address = s.recvfrom(2048)
   
print ("Received %s bytes from %s %s: " % (len(buf), address, buf ))

s.shutdown(1)





