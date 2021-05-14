import mysql.connector

class Database:
	def __init__(self,username,password,database):
		self.username = username
		self.password = password
		self.database = database
		self.mydb,status = self.checkIfAllright(username,password)
		if status:
			self.mycursor = self.mydb.cursor(buffered=True)

			try:
				sql =f"use {database};"
				self.mycursor.execute(sql)

			except :
				print("Database is Missing So Creating One")
				sql = f"create database {database};"
				self.mycursor.execute(sql)
				self.mydb.commit()
				
				sql =f"use {database};"
				self.mycursor.execute(sql)


			sql = "create table IF NOT EXISTS customers(user_id varchar(70) NOT NULL, name varchar(30) NOT NULL, family_members int NOT NULL, PRIMARY KEY (user_id));" 
			print(sql)
			self.mycursor.execute(sql)
			self.mydb.commit()

			sql = "create table IF NOT EXISTS items(order_id INT(11) NOT NULL, alloted_rice float NOT NULL, remaining_amount float NOT NULL, user_id varchar(70), PRIMARY KEY (order_id), FOREIGN KEY (user_id) REFERENCES customers(user_id) ON DELETE CASCADE ON UPDATE CASCADE);" 
			print(sql)
			self.mycursor.execute(sql)
			self.mydb.commit()
		else:
			print("something went wrong")

	def getRemainingRice(self,user_id):
		sql = f"select remaining_amount from items where user_id = '{user_id}';"
		self.mycursor.execute(sql)

	def add_customer(self,name,family_members,user_id):
		sql = f"insert into customers(name,family_members,user_id) values('{name}','{family_members}','{user_id}');"
		try:
			self.mycursor.execute(sql)
			self.mydb.commit()
			print("Insertion successfull")
		except :
			print("Already Exists")

	def deduct(self,user_id,remaining_amount):
		sql = f"update items set remaining_amount = '{remaining_amount}' where user_id = '{user_id}';"
		self.mycursor.execute(sql)
		self.mydb.commit()
		print("Deduction successful")

	def add_items(self,alloted_rice,remaining_amount,user_id,position):
		sql = f"insert into items(alloted_rice,remaining_amount,user_id,order_id) values('{alloted_rice}','{remaining_amount}','{user_id}','{position}');"
		try:
			self.mycursor.execute(sql)
			self.mydb.commit()
			print("Insertion successfull")
		except :
			print("Already Exists")


	def checkIfAllright(self,username,password):
		try:
			mydb = mysql.connector.connect(
			  host="localhost",
			  user=username,
			  password=password
			)
			return mydb,True
		except Exception as e:
			print("username or password is wrong")
			print(e)
			return [],False

	def update(self,user_id,alloted_rice,remaining_amount):
		sql = f"update items set alloted_rice = '{alloted_rice}',remaining_amount = '{remaining_amount}' where user_id = '{user_id}';"
		self.mycursor.execute(sql)
		self.mydb.commit()
		print("Updated successfully")

	def delete(self,user_id):
		sql = f"delete from customers where user_id = '{user_id}';"
		self.mycursor.execute(sql)
		self.mydb.commit()
		print("Deleted successfully")

	def getAllotment(self,user_id):
		sql = f"select alloted_rice from items where user_id = '{user_id}';"
		self.mycursor.execute(sql)
		val = (self.mycursor.fetchone())
		return val[0] if val else 0

	def getRemaining(self,user_id):
		sql = f"select remaining_amount from items where user_id = '{user_id}';"
		self.mycursor.execute(sql)
		val = (self.mycursor.fetchone())
		return val[0] if val else 0

	def isPresent(self,user_id):
		sql = f"select * from items where user_id = '{user_id}';"
		self.mycursor.execute(sql)
		val = (self.mycursor.fetchone())
		return True if val else False

	def getPosition(self,user_id):
		sql = f"select order_id from items where user_id = '{user_id}';"
		self.mycursor.execute(sql)
		val = (self.mycursor.fetchone())
		return int(val[0]) if val else None

	def getFamilyMem(self,user_id):
		sql = f"select family_members from customers where user_id = '{user_id}';"
		self.mycursor.execute(sql)
		val = (self.mycursor.fetchone())
		return int(val[0]) if val else None


	def getName(self,user_id):
		sql = f"select name from customers where user_id = '{user_id}';"
		self.mycursor.execute(sql)
		val = (self.mycursor.fetchone())
		return (val[0]) if val else None


if __name__ == "__main__":
	username = input()
	password = input()
	database = input()
	obj = Database(username,password,database)
	key = "[Enter key here]"
	obj.add_customer(name = "Yugandhar",family_members=4,user_id=key)
	obj.add_customer(name = "Hemant",family_members=4,user_id=5)
	obj.add_customer(name = "Vandana",family_members=4,user_id=6)

	# obj.add_items(alloted_rice = 5,remaining_amount=30,user_id=3)
	# obj.add_items(alloted_rice = 6,remaining_amount=60,user_id=6)
	# obj.add_items(alloted_rice = 5,remaining_amount=50,user_id=5)


	obj.update(5,333,52)
	obj.delete(5)
	print(obj.getAllotment(5))
	print(obj.isPresent(99))
	print(obj.isPresent(9))
	print(obj.isPresent(3))
	print(obj.isPresent(4))
	print(obj.getRemaining(99))