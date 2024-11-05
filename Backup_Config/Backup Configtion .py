from netmiko import ConnectHandler
from datetime import datetime, timedelta
import difflib

date = datetime.now()
today = date.strftime('%Y-%m-%d')

file_device = open("device.txt", "r")
ipdevice = file_device.read().split("\n")

deviceList = []
for ip in ipdevice:
    cisco_device = {
        "device_type":"cisco_ios",
        "host":ip,
        "username": "admin",
        "Password":"cisco",
        'port':'22'
    }
    deviceList.append(cisco_device)
for device in deviceList:
    try:
        connect = ConnectHandler(**cisco_device)
        prompt = connect.find_prompt()           #xem chế độ đang ở
        if '<' in prompt:
            connect.enable()
        output = connect.send_command('show run')
        #create filename
        prompt = connect.find_prompt()
        hostname = prompt[0:-1]
        filename = f'{hostname}_{today}_Backup.txt'
        #backup config
        with open(filename, 'w') as backup_config:
            backup_config.write(output)
            backup_config.close
            print(f'Backup of {hostname} complete seccessfull')
            print('#'*30)
        #backup log
        backup_log = open("backup_log", "a")
        backup_log.write("Successfully back up configuration of device" + filename)
        backup_log.close
        #Compare yesterday and today configuration
        yesterday = today() - timedelta(day = 1)
        filename_yes = f'{hostname}_{yesterday}_Backup.txt'

        yesterday_config = open(filename_yes)
        yesterday_config.read().split("\n")
        yesterday_config.close

        today_config = output.split("\n")
        diff = difflib.HtmlDiff().make_file(yesterday_config, today_config, "Yesterday Configuration", "Today Configuration")
        filenam_compare = f'{"Compare Configuration" + hostname}.html'
        compare_file =open(filenam_compare, "w")
        compare_file.write(diff)
        compare_file.close()

    except :
        backup_log = open("backup_log", "a")
        backup_log.write("There is a problem with device" + filename)
