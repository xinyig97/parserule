from bs4 import BeautifulSoup as bs
import re 
fname = input('Enter xml filename: ')
infile = open(fname,'r') # change me to the actual xml file name 
contents = infile.read()
soup = bs(contents,'xml')

class per_rule:
	def __init__(self,src,dest,prot,port,des):
		self.source = src 
		self.destination = dest
		self.protocol = prot
		self.port = port
		self.description = des 
	def sowhat(self):
		print('from', self.source, 'to', self.destination,'as',self.protocol)

class per_alias:
	def __init__(self,name,address,descri,clast):
		self.name  = name
		self.address = address 
		self.description = descri 
		self.clast = clast
	def so(self):
		print('group',self.name,' with address: ', self.address, "do ", self.description)

rules = list()

for rule in soup.find_all('rule'):	
	# handle source information 
	# official_src has the official source name 
	source = rule.find_all('source')
	string_src = str(source[0])
	if 'address' in string_src:
		tmp_src = re.findall('(?<=<address>)(.*)(?=</address>)',string_src)
		official_src = tmp_src[0]
	elif 'network' in string_src:
		tmp_src = re.findall('(?<=<network>)(.*)(?=</network>)',string_src)
		official_src = tmp_src[0]
	elif 'any' in string_src:
		official_src = 'any'
	else:
		official_src = 'undefined'

	# handle destinarion information
	destination = rule.find_all('destination')
	string_dest = str(destination)
	if 'address' in string_dest:
		tmp_dest = re.findall('(?<=<address>)(.*)(?=</address>)',string_dest)
		official_dest = tmp_dest[0]
		if 'port' in string_dest:
			tmp_port = re.findall('(?<=<port>)(.*)(?=</port>)',string_dest)
			official_port = tmp_port[0]
		else:
			official_port = 'none'
	elif 'network' in string_dest:
		tmp_dest = re.findall('(?<=<network>)(.*)(?=</network>)',string_dest)
		official_dest = tmp_dest[0]
		if 'port' in string_dest:
			tmp_port = re.findall('(?<=<port>)(.*)(?=</port>)',string_dest)
			official_port = tmp_port[0]
		else:
			official_port = 'none'
	elif 'any' in string_dest:
		official_dest = 'any'
	else:
		official_dest = 'undefined'
		official_port = 'none'

	# handle protocol
	protocol = rule.find_all('protocol')
	string_prot = str(protocol)
	if len(string_prot) == 2:
		official_prot = 'none'
	else:
		tmp_prot = re.findall('(?<=<protocol>)(.*)(?=</protocol>)',string_prot)
		official_prot = tmp_prot[0]

	# handle comments 
	comment = rule.find_all('descr')
	string_descr = str(comment)
	if '<descr/>' in string_descr:
		official_comment = 'none'
	else:
		tmp_comm = re.findall('(?<=<descr>)(.*)(?=</descr>)',string_descr)
		official_comment = tmp_comm[0]

	tmp_rule = per_rule(official_src,official_dest,official_prot,official_port,official_comment)
	rules.append(tmp_rule)

file = open('ruletable.html','w')
file.write('<table class = "wrapped">')
file.write('<tbody>')
file.write('<tr><th colspan = "1">Protocol</th><th colspan="1">Source</th><th colspan="1">Destination</th><th colspan="1">Ports</th><th colspan="1">Comment</th></tr>')

ruleopening = '<tr>'
ruleclosing = '</tr>'
entryentering = '<td>'
entryclosing = '</td>'
for i in rules:
	instance = ''
	src = i.source
	dest = i.destination
	prot = i.protocol
	port = i.port
	description = i.description
	ticket = re.findall('(LSST-[0-9]+)',description)
	if ticket:
		ticketopening = '<a href="http://jira.ncsa.illinois.edu/browse/'
		ticketmid = '">'
		ticketclosing = '</a>'
		for per_ticket in ticket:
			tmp_t = ticketopening+per_ticket+ticketmid+per_ticket+ticketclosing
			description = description.replace(per_ticket,tmp_t)
	ticket = re.findall('(SECURITY-[0-9]+)',description)
	if ticket:
		ticketopening = '<a href="http://jira.ncsa.illinois.edu/browse/'
		ticketmid = '">'
		ticketclosing = '</a>'
		for per_ticket in ticket:
			tmp_t = ticketopening+per_ticket+ticketmid+per_ticket+ticketclosing
			description = description.replace(per_ticket,tmp_t)
	if port == 'none':
		port = ' '
	instance += ruleopening+entryentering+prot+entryclosing+entryentering+src+entryclosing+entryentering+dest+entryclosing+entryentering+port+entryclosing+entryentering+description+entryclosing+ruleclosing
	file.write(instance)
file.write('</tbody></table>')


aliaslist = list()
for alias in soup.find_all('alias'):
	name = alias.find_all('name')
	official_name = re.findall('(?<=<name>)(.*)(?=</name>)',str(name[0]))

	address = alias.find_all('address')
	official_address = re.findall('(?<=<address>)(.*)(?=</address>)',str(address[0]))

	description = alias.find_all('descr')
	official_description = re.findall('(?<=<descr>)(.*)(?=</descr>)',str(description[0]))

	clast = alias.find_all('type')
	official_type = re.findall('(?<=<type>)(.*)(?=</type>)',str(clast[0]))

	tmp_alias = per_alias(official_name,official_address,official_description,official_type)
	aliaslist.append(tmp_alias)

file.write(' ')
file.write('<table class = "wrapped">')
file.write('<tbody>')
file.write('<tr><th colspan = "1">Name</th><th colspan="1">Type</th><th colspan="1">Addresses</th><th colspan="1">Comments</th></tr>')
for a in aliaslist:
	instance = ''
	name = a.name[0]
	address = a.address
	if address:
		address = address[0]
	else:
		address = ''
	description = a.description
	if description:
		description = description[0]
	else:
		description = ''
	ticket = re.findall('(LSST-[0-9]+)',description)
	if ticket:
		ticketopening = '<a href="http://jira.ncsa.illinois.edu/browse/'
		ticketmid = '">'
		ticketclosing = '</a>'
		for per_ticket in ticket:
			tmp_t = ticketopening+per_ticket+ticketmid+per_ticket+ticketclosing
			description = description.replace(per_ticket,tmp_t)
	ticket = re.findall('(SECURITY-[0-9]+)',description)
	if ticket:
		ticketopening = '<a href="http://jira.ncsa.illinois.edu/browse/'
		ticketmid = '">'
		ticketclosing = '</a>'
		for per_ticket in ticket:
			tmp_t = ticketopening+per_ticket+ticketmid+per_ticket+ticketclosing
			description = description.replace(per_ticket,tmp_t)
	typ = a.clast[0]
	instance = ruleopening+entryentering+name+entryclosing+entryentering+typ+entryclosing+entryentering+address+entryclosing+entryentering+description+entryclosing+ruleclosing
	file.write(instance)
file.write('</tbody></table>')





