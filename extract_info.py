import os, re, MySQLdb, time
from datetime import datetime
from random import randint

#Clase para los productos
class Product:
	def __init__(self, name, price):
		self.name = name
		self.price = price

	def __str__(self):
		return "Name: {}\nPrice: ${}".format(self.name, self.price)

#Clase para los tickets
class Ticket:

	def __init__(self, number, date, total):
		self.number = number
		self.products = []
		self.date = date
		self.total = total

	def __str__(self):
		string = ""
		for p in self.products:
			string += "\t{} ${}\n".format(p.name, p.price)
		return "Ticket no: {}\nDate: {}\nProducts:\n{}\nTotal: {}".format(self.number, self.date, string, self.total)


#python-pip
#python-mysqldb
#libmysqlclient-dev
#pip mysql
def testConnection():
	db = MySQLdb.connect(host="192.168.43.63", user="root", passwd="admin")
	c = db.cursor()
	c.execute("use mydb;")
	c.execute(""" INSERT INTO store(name) VALUES("La_Tiendita") """)
	db.commit()
	db.close()

def insertToDatabase(tickets):
	id_branch = randint(1,25)

	#db = MySQLdb.connect(host="192.168.43.63", user="root", passwd="admin")
	#c = db.cursor()
	#c.execute("use mydb;")

	for t in tickets:
		print("\n================================================")
		print(t)
		query = "INSERT INTO ticket ""(num_ticket, date, total, id_branch)"" VALUES ({}, '{}', {}, {});"\
		.format(t.number,t.date,t.total, id_branch)
		print(query)
		#c.execute(query)
		#db.commit(q)
		#id_ticket = c.lastrowid
		id_ticket = 12
		for p in t.products:
			print("\n------------------------------------")
			print(p)
			query2 = "INSERT INTO ticket_item ""(id_ticket, item_name, amount)"" VALUES ({},'{}',{});"\
        	.format(id_ticket, p.name, p.price) 
			print(query2)
			#c.execute(query2)
			#db.commit()
	#db.close()

#Procesa y hace la extraccion de informacion de cada uno de los tickets
def processData(data):
	regexDate = r"(([0-9]+[\/][\w]+[\/][0-9]+) ([\d]+:[\d]+:[\d]+) ([A|P][M]))"
	regexTotal = r"([\d+.?,\d+]+)"
	regexLinea = r"(([\w]+[\s[\w]+]*) (\$[\d+,?.+\d+]+) ([xX][\d+|l]))"
	products = []
	item_n = 0

	for line in data:
		if re.search(regexLinea, line):
			matchLinea = re.search(regexLinea, line)
			precio = matchLinea.group(3)
			ent, dec = precio.split(".") 
			ent = re.sub('[\,|\$]', '', ent)
			strPrecio = "{}.{}".format(ent, dec)	
			nombre = matchLinea.group(2)
			producto = Product(nombre, strPrecio)
			products.append(producto)
			
		if line.startswith("Date:"):
			date_ticket = ""
			time_ticket = ""
			if re.search(regexDate, line):
				matchDate = re.search(regexDate, line)
				date_ticket = matchDate.group(2)
				time_ticket = matchDate.group(3)
			day,month,year = date_ticket.split("/")
			hours,minutes,seconds = time_ticket.split(":")
			timeSql = datetime.strptime("{}/{}/{} {}:{}:{}".format(day,month,int(year)%100,hours,minutes,seconds), "%d/%m/%y %H:%M:%S")
			
		if line.startswith("Items count: "):
			_,item = line.split(":")
			item_n += int(item)
		
		if line.startswith("Receipt: "):
			_,tcktnum = line.split(":")
			num_ticket = int(tcktnum.strip())
			
		if line.startswith("Total "):
			if re.search(regexTotal, line):
				matchTotal = re.search(regexTotal, line)
			ent, dec = matchTotal.group(0).split(".") 
			ent = re.sub('[\,]', '', ent)
			strTotal = "{}.{}".format(ent, dec)	
			total_ticket = float(strTotal)
	ticket = Ticket(num_ticket, timeSql, total_ticket)
	for p in products:
		ticket.products.append(p)
	return ticket

#Procesa y manda a extraer los datos de todos los tickets
def processFile(path):
	listTickets = []

	for file in os.listdir(path):
		c_file = os.path.join(path, file)
		data = open(c_file, "r")
		listTickets.append(processData(data))
		data.close()

	return listTickets

	
def parseTxt():
	path = "/home/narvaezv/Documents/ISC/Integrador/txt"

	tickets = processFile(path)
	insertToDatabase(tickets)

	print("\n\nNumero de tickets: {}".format(len(tickets)))

def main():
	parseTxt()

#testConnection()

main()