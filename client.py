import socket
import sys
import hashlib

#======================#
def md5sum(filename, blocksize=1024):
	hash = hashlib.md5()
	with open(filename, 'rb') as f:
		for block in iter(lambda: f.read(blocksize), b''):
			hash.update(block)
	return hash.hexdigest()
	
#=========================#

Multicast_Group = ('224.0.0.1', 33333)
Server_IP = (raw_input('Please enter the IP address of the server: '), 22222)
Buffer_Size = 1024

#=======================#

try:
	unicast = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	print ''
	print 'Unicast socket created'
except socket.error:
	print 'Failed to create unicast socket'
	sys.exit()

try:
	multicast = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	print 'Multicast socket created'
except socket.error:
	print 'Failed to create multicast socket'
	sys.exit()

try:
	multicast.bind(Multicast_Group)
	print 'Multicast bind complete'
except socket.error:
	print 'Failed to bind multicast'
	sys.exit()


#===========================#

print 'Waiting for servers acknowledgement'

Message = 'Awaiting to receive data...'

try:
	unicast.sendto(Message, Server_IP)
	d = unicast.recvfrom(Buffer_Size)
	reply = d[0]
	addr = d[1]
	
	print ''
	print 'Server reply: ' + reply
except socket.error, msg:
	print 'Server did not reply'
	sys.exit()

#================================#

size, Multicast_Group = multicast.recvfrom(Buffer_Size)
size = init(size)

print ''
print 'File size: ' + str(size)
print ''

file = open('C:\Users\Oliver\Documents\Universidad\2018-2\Infracom\Laboratorios\Lab4y5\ImageFile.jpg', 'w')
file_path = 'C:\Users\Oliver\Documents\Universidad\2018-2\Infracom\Laboratorios\Lab4y5\ImageFile.jpg'

total = 0
while True:
	piece, Multicast_Group_loop = multicast.recvfrom(Buffer_Size)
	file.write(piece)
	
	total += len(piece)
	print 'Current size received: ' +str(total)
	if total == size:
		break

file.close()

hashsum = md5sum(file_path)

print ''
print 'Hash verification value: ' + hashsum

print ''
print 'File transfer successfully'

#=====================================#

try:
	unicast.close()
	print ''
	print 'Unicast socked closed successfully'
except socket.error:
	print 'Failed to close unicast socket'
	sys.exit()

try:
	multicast.close()
	print ''
	print 'Multicast socked closed successfully'
except socket.error:
	print 'Failed to close multicast socket'
	sys.exit()
	

print ''
print 'Stopping communication'







