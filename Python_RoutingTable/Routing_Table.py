from jnpr.junos import Device
from jnpr.junos.exception import ConnectError
from lxml import etree as et

device = Device(host='192.168.1.1', user='labuser', \
                password='Labuser')
try:
    device.open()
    response = device.rpc.get_route_information(normalize='True', protocol='ospf')
    et.dump(response)
    
    ifstatus_path = 'rt-entry/nh/to'
    nexthop = response.xpath(ifstatus_path)[0]
    print('Next Hop Address is:{0}'.format(nexthop))
    
    ifstatus_path = 'rt-entry/nh/via'
    viaif = response.xpath(ifstatus_path)[0]
    print('Next Hop Interface is:{0}'.format(viaif))
    
    ifstatus_path = 'rt-entry/preference'
    routepref = response.xpath(ifstatus_path)[0]
    print('Route Preference is:{0}'.format(routepref))
    
except ConnectError as err:
    print('\nConnection Error:'+ repr(err))
    
finally:
    device.close()