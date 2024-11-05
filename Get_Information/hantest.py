from pysnmp.entity.rfc3413.oneliner import cmdgen
from datetime import datetime 
today = datetime.now()
date = today.strftime("%Y-%m-%d %H:%M:%S")
# Tham số đưa vào
community_string = 'hcmbras-125hbt'  # Chuỗi cộng đồng SNMP
IP_Address = '172.16.253.222'  # Địa chỉ IP của thiết bị SNMP
OID_TX = ['1.3.6.1.4.1.2636.3.60.1.2.1.1.8.734.0',      #OID công suất  đầu ra
       '1.3.6.1.4.1.2636.3.60.1.2.1.1.8.734.1',
       '1.3.6.1.4.1.2636.3.60.1.2.1.1.8.734.2',
       '1.3.6.1.4.1.2636.3.60.1.2.1.1.8.734.3']
OID_RX = ['1.3.6.1.4.1.2636.3.60.1.2.1.1.6.734.0',      #OID công suất đầu vào
          '1.3.6.1.4.1.2636.3.60.1.2.1.1.6.734.1',
          '1.3.6.1.4.1.2636.3.60.1.2.1.1.6.734.2',
          '1.3.6.1.4.1.2636.3.60.1.2.1.1.6.734.3']
OID_INT = ['1.3.6.1.2.1.31.1.1.1.1.734']                #OID cổng thiết bị

cmd_gen = cmdgen.CommandGenerator()                     #cung cấp các phương thức để phục vụ getCmd, setCmd, nextCmd, Bulk
device = "MX960"
def get_rx(OID_RX):                                     #tạo hàm lấy công xuất đầu vào
    var_rx = []
    for oid_RX in OID_RX:                               #hàm get snmp
        error_indication, error_status, error_index, var_binds_RX = cmd_gen.getCmd(     #trả về giá trị var_binds_rx
            cmdgen.CommunityData(community_string),
            cmdgen.UdpTransportTarget((IP_Address, 161)),  # 161 là cổng SNMP mặc định
            oid_RX
    )
        for name, var in var_binds_RX:
            var = var/100
            var = str(var)
            var_rx.append(var)
    return var_rx
def get_tx(OID_TX):                                     #tạo hàm lấy công xuất đầu ra
    var_tx = []
    for oid_tx in OID_TX:
        error_indication, error_status, error_index, var_binds_TX = cmd_gen.getCmd(
            cmdgen.CommunityData(community_string),
            cmdgen.UdpTransportTarget((IP_Address, 161)),
            oid_tx
        )   
        for name, var in var_binds_TX:
            var = var/100
            var = str(var)
            var_tx.append(var)
    return var_tx     
def get_int(OID_INT):                                    #tạo hàm lấy tên cổng
    var_int = []
    for oid_INT in OID_INT:
        error_indication, error_status, error_index, var_binds_INT = cmd_gen.getCmd(
            cmdgen.CommunityData(community_string),
            cmdgen.UdpTransportTarget((IP_Address, 161)),  # 161 là cổng SNMP mặc định
            oid_INT
    )  
        for name, var in var_binds_INT:
            var = str(var)
            var_int.append(var)
    return var_int
interface_list = get_int(OID_INT)
for interface in interface_list:
    var_tx = get_tx(OID_TX)
    var_rx = get_rx(OID_RX)
    print(f"{date},{device},{interface},{var_tx},{var_rx} dBm")






