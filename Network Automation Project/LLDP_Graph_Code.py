#PYTHON APPLICATION THAT GATHERS NETWORK CONNECTIVITY INFORMATION AND DISPLAYS IT ON THE SCREEN IN A GRAPHICAL REPRESENTATION


#importing all the necessary libraries 
from jnpr.junos import Device
from jnpr.junos.utils.config import Config
from jnpr.junos.exception import ConnectError
from jnpr.junos.exception import CommitError
from lxml import etree as et
from graphviz import Graph

lldp_list = [] #this list collects the data about the routers, its interface, the neighbouring router interface and the neighboring router that it is connected to 
lldp_list_interfaces = [] # this lists collects the data from the lldp neighbor rpc and has the information about the router interfaces, and the neighbouring router and does not have local router data

#the block below defines the ip addresses of the six routers and its interfaces along with the interface address
routerlist = ['192.168.1.29', '192.168.1.30', '192.168.1.31', '192.168.1.32', '192.168.1.33', '192.168.1.34']
ifdata1 = {'ge-0/0/1': '72.114.96.1/24', 'ge-0/0/2': '72.114.96.2/24'}
ifdata2 = {'ge-0/0/1': '72.114.97.1/24', 'ge-0/0/2': '72.114.97.2/24'}
ifdata3 = {'ge-0/0/1': '72.114.98.1/24', 'ge-0/0/2': '72.114.98.2/24', 'ge-0/0/3': '72.114.98.3/24', 'ge-0/0/4': '72.114.98.4/24'}
ifdata4 = {'ge-0/0/1': '72.114.99.1/24', 'ge-0/0/3': '72.114.99.2/24'}
ifdata5 = {'ge-0/0/1': '72.114.100.1/24', 'ge-0/0/2': '72.114.100.2/24', 'ge-0/0/3': '72.114.100.3/24'}
ifdata6 = {'ge-0/0/2': '72.114.101.1/24'}
iflist = [ifdata1, ifdata2, ifdata3, ifdata4, ifdata5, ifdata6]
for i in range(len(routerlist)): #sets up a loop for the number of entries in the routerlist list
	device = Device(host=routerlist[i], user='labuser', password='Labuser') #connect to the router
	var_dict = {'ifdata': iflist[i]} #defines dictionary with variables to configure interfaces
	
	try:
		device.open() #setup NETCONF Session
		device.bind(conf=Config) #bind Candidate Configuration
		device.conf.load(template_path = 'projecttemplate.conf',template_vars = var_dict, merge = True) #load the candidate configuration
		success = device.conf.commit() #commit the candidate configuration
		print('success for router '+routerlist[i].format(success))

	except ConnectError as err:
		print('\nConnection Error:'+ repr(err)) #error handling
    
	finally:
		device.close() #close the NETCONF Session


#looping over each router in the routerlist
for i in range(len(routerlist)):
	device = Device(host=routerlist[i], user='labuser', password='Labuser')

	try:
		device.open()
		response_neighbor = device.rpc.get_lldp_neighbors_information(normalize = True) #getting the lldp neighbor information
		response_local=device.rpc.get_lldp_local_info(normalize = True) #getting the local lldp information 

		for i,value in enumerate(response_local): #looping over the response_local
			if i==1:
				lldp_list.append(value.text) #appending the value to the lldp_list
					
		for i,value in enumerate(response_neighbor): #looping over the response_neighbor
			for j,value2 in enumerate(value):
				lldp_list_interfaces=[]
				if j==0 and value2.text!='ge-0/0/0.0': #removing the interfaces ge-0/0/0
					lldp_list_interfaces.append(value2.text) #appending to another list which is lldp_list_interfaces

				#removing the interfaces which are other than what we require, if you have more interfaces than what are mentioned just add here
				if j==4 and (value2.text=='ge-0/0/1.0' or value2.text=='ge-0/0/2.0' or value2.text=='ge-0/0/3.0' or value2.text=='ge-0/0/4.0'):
					lldp_list_interfaces.append(value2.text) #appending to another list which is lldp_list_interfaces
				#extracting only the neighboring routers
				if j==5 and value2.text!='switch226':					
					lldp_list_interfaces.append(value2.text)
				if len(lldp_list_interfaces)>0: #if any element is blank do not consider it in the list 
					lldp_list.append(lldp_list_interfaces)
				
	except ConnectError as err: #Exception and error handling  
		print('\nConnection Error:'+ repr(err))
    
	finally: 
		device.close() #End the NETCONF Sesssion


print(lldp_list)		
dict1 = {}
for i in range(len(lldp_list)):
	if(isinstance(lldp_list[i],str)): #whichever element is string that is my local router, and remaining are the connections to the local router
		key = lldp_list[i] #set the key in the dictionary where key is equal to the local router name
		if key not in dict1: #creating a new entry in the dictionary
			dict1[key] = []
	else:
		dict1[key].append(lldp_list[i][0]) #populate the value list with all interfaces and neighbor router names and since our lldp_list is a list of single elements, we use lldp_list[i][0]
temporary_list = [] 
final_list_of_lists = []
for k,v in dict1.items(): #iterate over each local router
	for i in range(len(v)): #iterate over each element in the value list
		temporary_list.append(v[i])
		if 'router' in v[i]: #if we reach a neighbor router
			final_list_of_lists.append([k]+temporary_list) #append local router, interfaces, neighbor router in a single list to the final, which is a list of lists
			temporary_list = []
print("Final is ",final_list_of_lists) #get a list of list with all four values required to pass in the edge
graph = final_list_of_lists #assigning a variable to final_list_of_lists
dict2 = {} 
# print(graph)
# to remove the duplicate connections 
for i in range(len(graph)): 
	if str(sorted([int(graph[i][0][6:]),int(graph[i][-1][6:])])) not in dict2.keys(): #extracting router numbers and generating unique keys from them
		dict2[str(sorted([graph[i][0],graph[i][-1]]))] = graph[i]

g=Graph('G',filename='lldp.gv',strict=True)
for ele in dict2.values():
	#print("g.edge(",ele[0],",",ele[-1],",",ele[1],",",ele[2],")") ; to view the exact edges 
	g.edge(ele[0],ele[-1],headlabel=ele[2],taillabel=ele[1])
g.view() #to view the graph

