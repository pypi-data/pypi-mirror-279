####
#
# Debug communication
# sudo tcpdump -i en0 -A -nn dst 192.168.2.201 or src 192.168.2.201
#
# Script:
# python3 dzg_meter.py 192.168.178.109 8899 62371521
#
###

import warnings
import logging
import time
import sys
import json
sys.path.append("..")
from iec62056_21_dzg.client import Iec6205621Client


#print ('argument list', sys.argv)
ip_addr = sys.argv[1]
ip_port = int(sys.argv[2])
meter_address = sys.argv[3]


#logging.basicConfig(level="DEBUG")

#client = Iec6205621Client.with_tcp_transport(address=('192.168.178.109', 8899), device_address='62371521')
client = Iec6205621Client.with_tcp_transport(address=(ip_addr, ip_port), device_address=meter_address)

client.connect()
#print(client.standard_readout())

#client.send_password(password='9390')

password = client.access_programming_mode()
#print(password.data_set.value)
client.send_password(password.data_set.value)

#print(client.write_single_value(address='01-00:5E.31.01.0D', data = "12"))



#time.sleep(10)


#print(client.read_single_value(address='01-01:60.60.04.FF', additional_data = 0))

# Seriennummer
#print(client.read_single_value(address='01-00:00.00.05.FF', additional_data = 0))


#client.access_programming_mode()

#Spannung Phase L3
#print("Spannung L3:")
#dzg_spannung_l1 = int(client.read_single_value(address='01-00:48.07.00.FF', additional_data = 0).value, 16) / 100
#print(dzg_spannung_l1)

dzg_wirkleistung = int(client.read_single_value(address='01-00:10.07.00.FF', additional_data = 0).value, 16) / 100
#print(dzg_wirkleistung)

# Tarifkonfiguration
#print("Tarifkonfiguration Netzbezug: ")
#print(client.write_single_value(address='01-00:5E.31.01.0D', data = "10"))

#print("Tarifkonfiguration PV: ")
#dzg_tarifkonfiguration = client.write_single_value(address='01-00:5E.31.01.0D', data = "12")

#time.sleep(0.1)
#print("Tarifkonfiguration auslesen: ")
dzg_tarifkonfiguration = client.read_single_value(address='01-00:5E.31.01.0D', additional_data = 0).value
#print(dzg_tarifkonfiguration)

#time.sleep(0.1)
#print("Tarif 1.8.0 auslesen: ")
dzg_tarif_1_8_0 = int(client.read_single_value(address='01-00:01.08.00.FF', additional_data = 0).value, 16) / 10000
#print(dzg_tarif_1_8_0)

#time.sleep(0.1)
#print("Tarif 1.8.1 auslesen: ")
dzg_tarif_1_8_1 = int(client.read_single_value(address='01-00:01.08.01.FF', additional_data = 0).value, 16) / 10000
#print(dzg_tarif_1_8_1)

#time.sleep(0.1)
#print("Tarif 1.8.2 auslesen: ")
dzg_tarif_1_8_2 = int(client.read_single_value(address='01-00:01.08.02.FF', additional_data = 0).value, 16) / 10000
#print(dzg_tarif_1_8_2)

dzg_data = {
  "device_address": meter_address,
  "tarifkonfiguration": dzg_tarifkonfiguration,
  "tarif_1_8_0": {"value": dzg_tarif_1_8_0, "unit": "kWh"},
  "tarif_1_8_1": {"value": dzg_tarif_1_8_1, "unit": "kWh"},
  "tarif_1_8_2": {"value": dzg_tarif_1_8_2, "unit": "kWh"},
  "wirkleistung": {"value": dzg_wirkleistung, "unit": "W"},
}

dzg_data_json = json.dumps(dzg_data)
print(dzg_data_json)
