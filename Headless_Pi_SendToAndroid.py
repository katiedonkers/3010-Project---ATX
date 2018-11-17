import socket, sys, time

newMeasurementsPacketFlag = 3
temp = 99

# function to collect and send measurements from headless Pi to database Pi
def sendMeasurements(data):

    host = '192.168.43.231'
    port = 1050
    server_address = (host, port)
    host_address = ('192.168.43.128', 53477)

    #create socket
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    print('trying to bind')
    s.bind(host_address)
    print('bound')

    # send packet to database Pi
    s.sendto(data, server_address)
    print('sent packet')

    #time.sleep(10)
    print('waiting to receive...')
    buf, address = s.recvfrom(2048)
    print ("Received %s bytes from %s %s: " % (len(buf), address, buf ))

def formatPacket(data):

    # format packet
    temp = "" + str(newMeasurementsPacketFlag) + "" + str(data[0]) + "" + str(data[1]) + "" + str(data[2])
    byteArray = bytearray(temp, 'utf8')

    # call sendMeasurements() with proper packet format
    sendMeasurements(byteArray)
    
#MAIN
def main():

    #measurements array [] will contain length, circumf1 (wrist) circumf2 (elbow) 
    measurements = [7,8,9]
    formatPacket(measurements)


main()








