import mysql.connector

class Database:
	def __init__(self,username,password,database):

		try:
			mydb = mysql.connector.connect(
			  host="localhost",
			  user=username,
			  password=password,
			)
		except Exception as e:
			print("username or password is wrong")
			exit(1)

		mycursor = mydb.cursor()

		try:
			sql =f"use {database};"
			mycursor.execute(sql)

		except :
			print("Database is Missing So Creating One")
			sql = f"create database {database};"
			mycursor.execute(sql)
			mydb.commit()

			sql = "create table customers(user_id INT(11) NOT NULL AUTO_INCREMENT, name varchar(30), address varchar(50), age int, PRIMARY KEY (user_id));" 
			print(sql)
			mycursor.execute(sql)
			mydb.commit()

			sql = "create table items(user_id INT(11) NOT NULL AUTO_INCREMENT, name varchar(30), address varchar(50), age int, PRIMARY KEY (user_id));" 
			print(sql)
			mycursor.execute(sql)
			mydb.commit()

		