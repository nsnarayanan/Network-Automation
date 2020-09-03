from jnpr.junos import Device
from jnpr.junos.utils.config import Config
from jnpr.junos.exception import ConnectError
from jnpr.junos.exception import CommitError
from lxml import etree as et

device_1 = Device(host='192.168.1.19', user='labuser', password='Labuser')
if_config = {'ge-0/0/1':'42.7.1.1/24', 'lo0':'42.7.10.1/24'}
ifname = {'ge-0/0/1':'42.7.1.1/24'}
var_dict_1 = {'if_config': if_config, 'ifname':ifname}


device_2 = Device(host='192.168.1.20', user='labuser', password='Labuser')
if_config = {'ge-0/0/2':'42.7.1.2/24', 'lo0':'42.7.20.1/24'}
ifname = {'ge-0/0/2':'42.7.1.2/24'}
var_dict_2 = {'if_config': if_config, 'ifname':ifname}


try:
	device_1.open()
	device_1.bind(conf=Config)
	device_1.conf.load(template_path = 'templatehw4.conf', template_vars = var_dict_1, merge = True)
	success = device_1.conf.commit()
	print('success = {0}'.format(success))
	

	device_2.open()
	device_2.bind(conf=Config)
	device_2.conf.load(template_path = 'templatehw4.conf', template_vars = var_dict_2, merge = True)
	success = device_2.conf.commit()
	print('success = {0}'.format(success))
	
	device_1.open()
	device_1.bind(conf2=Config)
	device_1.conf2.load(template_path = 'templatehw4_fw.conf', merge = True)
	success = device_1.conf2.commit()
	print('success = {0}'.format(success))
	
	
	device_1.open()
	response = device_1.rpc.get_rip_neighbor_information(normalize=True)
	et.dump(response)
	
	device_1.open()
	response = device_1.rpc.get_route_information(protocol='rip', normalize=True)
	et.dump(response)
	
	device_1.open()
	response = device_1.rpc.ping(host='42.7.20.1', normalize=True, count='1')
	et.dump(response)
	
	

except ConnectError as err:
    print('\nConnection Error:'+ repr(err))
    
finally:
    device_1.close()
    device_2.close()

