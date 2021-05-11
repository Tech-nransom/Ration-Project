import mysql.connector

class Database:
	def __init__(self,username,password,database):
		self.username = username
		self.password = password
		self.database = database
		self.mydb,status = self.checkIfAllright(username,password)
		if status:
			self.mycursor = self.mydb.cursor()

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


			sql = "create table IF NOT EXISTS customers(user_id int NOT NULL, name varchar(30) NOT NULL, family_members int NOT NULL, PRIMARY KEY (user_id));" 
			print(sql)
			self.mycursor.execute(sql)
			self.mydb.commit()

			sql = "create table IF NOT EXISTS items(order_id INT(11) NOT NULL AUTO_INCREMENT, alloted_rice float NOT NULL, remaining_amount float NOT NULL, user_id int, PRIMARY KEY (order_id), FOREIGN KEY (user_id) REFERENCES customers(user_id) ON DELETE CASCADE ON UPDATE CASCADE);" 
			print(sql)
			self.mycursor.execute(sql)
			self.mydb.commit()
		else:
			print("something went wrong")

	def getRemainingRice(self,user_id):
		sql = f"select remaining_amount from items where user_id = {user_id};"
		self.mycursor.execute(sql)

	def add_customer(self,name,family_members,user_id):
		sql = f"insert into customers(name,family_members,user_id) values('{name}','{family_members}','{user_id}');"
		self.mycursor.execute(sql)
		self.mydb.commit()
		print("Insertion successfull")

	def add_items(self,alloted_rice,remaining_amount,user_id):
		sql = f"insert into items(alloted_rice,remaining_amount,user_id) values('{alloted_rice}','{remaining_amount}','{user_id}');"
		self.mycursor.execute(sql)
		self.mydb.commit()
		print("Insertion successfull")



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
			return [],False


if __name__ == "__main__":
	username = input()
	password = input()
	database = input()
	obj = Database(username,password,database)
	obj.add_customer(name = "Yugandhar",family_members=4,user_id=3)
	obj.add_customer(name = "Hemant",family_members=4,user_id=5)
	obj.add_customer(name = "Vandana",family_members=4,user_id=6)

	obj.add_items(alloted_rice = 5,remaining_amount=30,user_id=3)
	obj.add_items(alloted_rice = 6,remaining_amount=60,user_id=6)
	obj.add_items(alloted_rice = 5,remaining_amount=50,user_id=5)