import paramiko
import json
import hmac, base64, struct, hashlib, time

def get_secrets(pwd_file):
    with open(pwd_file,'r') as file:
        for line in file:
            line = line.strip()
    dict = eval(line)
    dict = {k: base64.b64decode(v).decode("utf-8") for k, v in dict.items()}
    return dict
def get_hotp_token(secret, intervals_no):
    key = base64.b32decode(secret, True)
    msg = struct.pack(">Q", intervals_no)
    h = hmac.new(key, msg, hashlib.sha1).digest()
    o = h[19] & 15
    h = (struct.unpack(">I", h[o:o+4])[0] & 0x7fffffff) % 1000000
    return h

def get_totp_token(secret):
    return get_hotp_token(secret, intervals_no=int(time.time())//30)

def connect_sftp(hostname,username,password,port):
    transport = paramiko.Transport(hostname,port)

    #ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    transport.connect(username=username,password=password)

    ftp = paramiko.SFTPClient.from_transport(transport)
    files = ftp.listdir()

    ftp.close()
    transport.close()
    return files

if __name__ == '__main__':
    filename = 'sftp_password.txt'
    secrets_dict = get_secrets(filename)
    secret,username,password,hostname = secrets_dict['mfaAuthCode'],secrets_dict['username'],secrets_dict['password'],secrets_dict['hostname']
    token = get_totp_token(secret)
    password = password+str(token)
    files = connect_sftp(hostname,username,password,port=22)
    print(files)
