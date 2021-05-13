from tkinter import *
from tkinter import ttk
from modules import Operations
from database import *

class Administrator:
	def __init__(self):
		self._flg = False

	def adminWindow(self):
		if self._flg:
			self.admin.destroy()
			self.admin = Toplevel(self.master)

			self.admin.resizable(False,False)

			self.msg = ttk.Label(self.admin,text = "Select the option:")
			self.msg.pack()

			self.admin.title("Admin")
			self.admin.minsize(width=300,height=100)

			self.enter = ttk.Button(self.admin,text = "Enter",command = self.createWindow)
			self.delete = ttk.Button(self.admin,text = "Delete",command = self.delete_rec)
			self.update = ttk.Button(self.admin,text = "Update",command = self.update_rec)
			self.enter.pack()
			self.delete.pack()
			self.update.pack()

		else:
			self.admin = Toplevel(self.master)

			self.admin.title("Admin")
			self.admin.minsize(width=300,height=100)

			self.admin.resizable(False,False)

			Label(self.admin,text = "Enter Your Password").pack()

			self.password = ttk.Entry(self.admin,width = 30)
			self.password.pack()
			self.password.config(show = "*")


			self.submit = ttk.Button(self.admin,text = "Submit",command = self.checkPassword)
			self.submit.pack()

			self.msg = ttk.Label(self.admin,text = "")
			self.msg.pack()
			
		
	def checkPassword(self):
		if (self.password.get()) == self.PASSWORD:
			print("Password:", self.password.get())
			self.msg["text"] = "Successfull Login"
			self.msg.config(foreground = "green")
			self._flg = True
			if self.username == None:
				self.username = input("Username:")
				self.password = input("Password:")
				self.database = input("Database name:")
			self.adminWindow()
		else:
			print("Invalid Password")
			self.msg["text"] = "Invalid Password"
			self.msg.config(foreground = "red")

			self.password.delete(0,END)

	def RegisterUser(self,name,mem,q,key,position):

		temp = Database(self.username,self.password,self.database)
		temp.add_customer(name,mem,key)
		alloted_rice,remaining_amount,user_id,position = q*mem,q*mem,key,position
		temp.add_items(alloted_rice,remaining_amount,user_id,position)

class User:
	def __init__(self):
		pass
		

	def userWindow(self):
		self.user = Toplevel(self.master)
		self.user.title("User")
		self.user.minsize(width=300,height=100)
		self.user.register(False,False)

		self.auth = ttk.Button(self.user,text = "Authenticate",command = self.verify)
		self.auth.pack()

	def verify(self):
		obj = Operations()
		key,position = obj.search()
		if (key) == -1:
			print("Invalid key found")
		else:
			self.displayInfo(key)

	def displayInfo(self,key):
		temp = Database(self.username,self.password,self.database)
		print(temp.getName(key))
		print(temp.getFamilyMem(key))
		print(temp.getAllotment(key))
		print(temp.getRemaining(key))

class Application(Administrator,User):
	def __init__(self,master):
		super().__init__()
		ttk.Label(master=master,text = "Select Your Choice").pack()
		self.PASSWORD = "admin"
		self.master = master
		self.admin_b = ttk.Button(master,text = "Administrator",command = self.adminWindow)
		self.admin_b.pack()
		self.user_b = ttk.Button(master,text = "User",command = self.userWindow)
		self.user_b.pack()
		master.title("Fingerprint Management")
		master.minsize(width = 300,height = 100)
		master.resizable(False,False)
		self.username = None



	def createWindow(self):
		self.window = Toplevel(self.master)
		Label(self.window,text = "Enter Users Name:   ").grid(row = 0,column=0)
		self.name = ttk.Entry(self.window)
		self.name.grid(row = 0,column=1)

		Label(self.window,text="").grid(row=1,column=0)
		Label(self.window,text = "Enter Users Family Members:   ").grid(row = 2,column=0)
		self.family = ttk.Entry(self.window)
		self.family.grid(row = 2,column=1)

		Label(self.window,text="").grid(row=3,column=0)
		Label(self.window,text = "Rice PerPerson:").grid(row = 4,column=0)
		self.perPerson = StringVar()
		self.q = ttk.Spinbox(self.window, from_ = 0, to=20, textvariable = self.perPerson,state = "readonly")
		self.q.grid(row = 4,column=1)

		self.register = ttk.Button(self.window,text = "Register",command = self.add_rec)
		self.register.grid(row=5,column=1)


		

	def add_rec(self):
		if self.username == None:
			self.username = input("Username:")
			self.password = input("Password:")
			self.database = input("Database name:")

		# Validation remaining

		name = self.name.get()
		mem = self.family.get()
		quantity = self.perPerson.get()
		print(name,mem,quantity)
		self.window.destroy()
		obj = Operations()
		key,position = obj.add()
		print(key)
		print(position)
		if (key) == -1:
			print("Invalid Key Detected....Not inserting in the database")
		else: self.RegisterUser(name = name,mem = int(mem),q = int(quantity),key = key,position = position)
		
 		

	def delete_rec(self):
		# TODO: Delete record by admin
		if self.username == None:
			self.username = input("Username:")
			self.password = input("Password:")
			self.database = input("Database name:")
		obj = Operations()
		temp = Database(self.username,self.password,self.database)
		key,position = obj.search()
		if (key) == -1:
			print("Invalid key found")
		else:
			if position != None:
				obj.delete(temp.getPosition(key))
				temp.delete(key)
			else:
				print("Position not found")


	def update_rec(self):
		if self.username == None:
			self.username = input("Username:")
			self.password = input("Password:")
			self.database = input("Database name:")
		# TODO: update the existing record by admin 
		#		Give appropriate msg if rec not present
		obj = Operations()
		key,position = (obj.search())
		

def main():
	root = Tk()
	app = Application(root)
	root.mainloop()


if __name__ == "__main__":
	main()