import socket, sys, time

measurementsPacketFlag = 5 

# function to collect and send measurements from headless Pi to database Pi
def sendMeasurements(data):

    host = '192.168.43.231'
    port = 1050
    server_address = (host, port)

    #create socket
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # send packet to database Pi
    s.sendto(data, server_address)

def formatPacket(data):

    #format packet
    temp = "" + str(measurementsPacketFlag) + "" + str(data[0]) + "" + str(data[1]) + "" + str(data[2]) + ""
    byteArray = bytearray(temp, 'utf8')

    # call sendMeasurements() with proper packet format
    sendMeasurements(byteArray)
    
#MAIN
def main():

    count = 1
#measurements array [] will contain length, circumf1 (wrist) circumf2 (elbow) 
    measurements = [1,2,3]

    while (len(measurements) < 3):
        count+=1
   
    formatPacket(measurements)
    print('hi')


main()
#print ("Received %s bytes from %s %s: " % (len(buf), address, buf ))
#s.shutdown(1)










