import paramiko

host = "we12s300.ugent.be"                    #hard-coded
port = 1048
transport = paramiko.Transport((host, port))

password = "Peikop11358"                #hard-coded
username = "samuel"                #hard-coded
transport.connect(username = username, password = password)

sftp = paramiko.SFTPClient.from_transport(transport)

import sys
path = 'D:\One Drive\Documenten\Samuel\PhD\Gent' + sys.argv[1]    #hard-coded
localpath = sys.argv[1]
sftp.put(localpath, path)

sftp.close()
transport.close()
print ('Upload done.')