from netmiko import ConnectHandler
from datetime import datetime
import threading

date = datetime.now()
today = date.strftime('%Y-%m-%d')

def backup(device):
    connection = ConnectHandler(**device)
    prompt = connection.find_prompt()           #xem chế độ đang ở
    if '<' in prompt:
        connection.enable()
    output = connection.send_command('show run')

    prompt = connection.find_prompt()
    hostname = prompt[0:-1]


    filename = f'{hostname}_{today}_Backup.txt'
    with open(filename, 'w') as backup:
        backup.write(output)
        print(f'Backup of {hostname} complete seccessfull')
        print('#'*30)
    print('Close connection')
    connection.disconnect()

with open('device.txt') as f:
    devices = f.read().splitlines()

threads = list()
for ip in devices:
    device = {'device_type': 'cisco_ios',
              'host': ip,
              'username': 'cisco',
              'password': 'cisco',
              'port':'22',
              'secret': 'cisco',
              'verbose':True}
    th = threading.Thread(target= backup, args= (device,))
    threads.append(th)
for th in threads:
    th.start()
for th in threads:
    th.join()
