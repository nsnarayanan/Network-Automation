from jnpr.junos import Device
from jnpr.junos.exception import ConnectError
from lxml import etree as et
import time 

device = Device(host='192.168.1.10', user='labuser', \
	password='Labuser')
listmax = []
listmin = []

try:
	device.open()
	for ping in range(0,10):
		time.sleep(10)
		response = device.rpc.ping(normalize=True, count='3', host='192.168.1.139')
		et.dump(response)
		ifstatus_path = 'probe-result/rtt/text()'
		rtt1 = response.xpath(ifstatus_path)[0]
		print('RTT Ping 1: {0}'.format(rtt1))
		ifstatus_path = 'probe-result/rtt/text()'
		rtt2 = response.xpath(ifstatus_path)[1]
		print('RTT Ping 2: {0}'.format(rtt2))
		ifstatus_path = 'probe-result/rtt/text()'
		rtt3 = response.xpath(ifstatus_path)[2]
		print('RTT Ping 3: {0}'.format(rtt3))
	
		ifstatus_path = 'probe-results-summary/rtt-minimum/text()'
		rttmin = response.xpath(ifstatus_path)[0]
		print('Minimum RTT: {0}'.format(rttmin))
		ifstatus_path = 'probe-results-summary/rtt-maximum/text()'
		rttmax = response.xpath(ifstatus_path)[0]
		print('Maximum RTT: {0}'.format(rttmax))
		ifstatus_path = 'probe-results-summary/rtt-average/text()'
		rttavg = response.xpath(ifstatus_path)[0]
		print('Average RTT: {0}'.format(rttavg))	
		
		listmax.append(rttmax)
		rttmaxval = max(listmax)
		print("RTT Maximum Value for overall operation is:", rttmaxval)

		listmin.append(rttmin)
		rttminval = min(listmin)
		print("RTT Minimum Value for overall operation is:", rttminval)
		
	

except ConnectError as err:
	print('\nConnection error: '+ repr(err))

finally:
	device.close()

