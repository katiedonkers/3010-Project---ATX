import socket

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
print('trying to bind')
s.bind('192.168.43.231',1050)

def _2_databaseErrorsReceiveLogInTimeout():
    data, address = s.recvfrom(1024)
    #waitSocketTimeout

def _x_dbReceiveLogInsendBadPacket():
    data,address = s.recvfrom(1024)

    s.sendto(bytes("7", 'utf-8'),address) #change flag with smth we dont check for

def _x_dbReceiveLogInSendLongUsername():
    data, address = s.recvfrom(1024)
    s.sendto(bytes("9xXxXxXxXxXx122", 'utf-8'), address)

def _5a_headlessPiReceiveNewMeasurementTimeout():
    data, address = s.recvfrom(1024)
    #waitSocketTimeout

def _5d_headlessPiReceiveNewMeasurementSendBackZeroMeasurements():
    data, address = s.recvfrom(1024)
    s.sendto(bytes("8000", 'utf-8'), address) #assuming 8 is the flag for headlessPi measurementPacket

######
#Construct your test here 
######
