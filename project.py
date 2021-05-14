from tkinter import *
from tkinter import ttk
from modules import Operations
from database import *
import tkinter.font as tkFont
from motor import playMotor
from tkinter.messagebox import showerror

class Administrator:
	def __init__(self):
		self._flg = False

	def adminWindow(self):
		if self._flg:
			self.admin.destroy()
			self.admin = Toplevel(self.master)
			self.admin.resizable(False,False)
			self.admin.geometry("+300+300")
			self.msg = ttk.Label(self.admin,text = "Select the option:")
			self.msg.pack()

			self.admin.title("Admin")
			self.admin.minsize(width=300,height=300)

			self.enter = ttk.Button(self.admin,text = "Enter",command = self.createWindow)
			self.delete = ttk.Button(self.admin,text = "Delete",command = self.delete_rec)
			self.update = ttk.Button(self.admin,text = "Update",command = self.update_rec)
			self.enter.pack()
			self.delete.pack()
			self.update.pack()

			

		else:
			self.admin = Toplevel(self.master)

			self.admin.title("Admin")
			self.admin.minsize(width=300,height=300)
			self.admin.geometry("+300+300")
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
		self.user.resizable(False,False)
		self.user.geometry("300x300+300+300")
		# self.auth = ttk.Button(self.user,text = "Authenticate",command = lambda :self.displayInfo(key))
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
		print(key)
		self.infoPage(temp.getName(key),temp.getFamilyMem(key),temp.getAllotment(key),temp.getRemaining(key),key)
		# self.infoPage("yugandhar",4,10,15,key)
		print(temp.getName(key),temp.getFamilyMem(key),temp.getAllotment(key),temp.getRemaining(key))

	def infoPage(self,name,members,allotment,remaining,key):
		self.user.withdraw()
		fontStyle = tkFont.Font(family="Times", size=15)
		self.page = Toplevel(self.user)
		self.page.title("Information Page")
		self.page.minsize(width=300,height=300)
		self.page.resizable(False,False)
		self.page.geometry("+300+300")
		def on_closing():
			self.user.deiconify()
			self.page.destroy()
		self.page.protocol("WM_DELETE_WINDOW", on_closing)


		Label(self.page,text = f"Name: {name}",font = fontStyle, justify=LEFT,anchor="w").grid(sticky = W,row = 1,column = 0)
		# Label(self.page,tex)
		Label(self.page).grid(row = 2,column = 0)
		Label(self.page,text = f"Family Members: {members}",font = fontStyle, justify=LEFT,anchor="w").grid(sticky = W,row = 3,column = 0)
		Label(self.page).grid(row = 4,column = 1)
		Label(self.page,text = f"Alloted Rice: {allotment}",font = fontStyle, justify=LEFT,anchor="w").grid(sticky = W,row = 5,column = 0)
		Label(self.page).grid(row = 6,column = 0)
		Label(self.page,text = f"Remaining Amount: {remaining}",font = fontStyle, justify=LEFT,anchor="w").grid(sticky = W,row = 7,column = 0)

		self.amount = Entry(self.page)
		Label(self.page).grid(row = 8,column = 0)
		Label(self.page,text = "Enter the Amount To Withdraw:",font = fontStyle, justify=LEFT,anchor="w").grid(sticky = W,row = 9,column = 0)
		self.amount.grid(row = 9,column=1)

		self.ok= ttk.Button(self.page,text = "OK",command = lambda :self.motor(key,remaining))
		self.cancel = ttk.Button(self.page,text = "CANCEL",command = on_closing)

		self.ok.grid(row = 10,column=1,padx = 6)
		self.cancel.grid(row = 10,column=2)

	def isOk(self,key,remaining):
		try:
			if self.username == None:
				self.username = input("Username:")
				self.password = input("Password:")
				self.database = input("Database name:")

			temp = Database(self.username,self.password,self.database)
			deduct = int(self.amount.get())
			if deduct > int(remaining):
				return False
			else:
				temp.deduct(key,(int(remaining) - deduct))
			return True
		except :
			return False


	def motor(self,key,remaining):
		if self.isOk(key,remaining):
			playMotor() 
		else:
			showerror("Invalid Enter","Please Check the Amount Entered")
			self.page.destroy()



class Application(Administrator,User):
	def __init__(self,master):
		super().__init__()
		ttk.Label(master=master,text = "Select Your Choice").pack()

		# self.username = "root"
		# self.password = "root"
		# self.database = "sample2"


		self.PASSWORD = "admin"

		self.master = master
		self.master.geometry("+300+300")
		self.admin_b = ttk.Button(master,text = "Administrator",command = self.adminWindow)
		self.admin_b.pack()
		self.user_b = ttk.Button(master,text = "User",command = self.userWindow)
		self.user_b.pack()
		master.title("Fingerprint Management")
		master.minsize(width = 300,height = 300)
		master.resizable(False,False)

		self.username = None

	def createWindow(self):
		self.admin.withdraw()
		self.window = Toplevel(self.master)
		self.window.minsize(width=300,height=300)
		Label(self.window,text = "Enter Users Name:   ").grid(row = 0,column=0)
		self.name = ttk.Entry(self.window)
		self.name.grid(row = 0,column=1)
		self.window.geometry("+300+300")
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

		def on_closing():
			self.admin.deiconify()
			self.window.destroy()
		self.window.protocol("WM_DELETE_WINDOW", on_closing)

		self.back = ttk.Button(self.window,text = "Back",command = on_closing)
		self.back.grid(row = 5,column=0)



		

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