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

			self.enter = ttk.Button(self.admin,text = "Enter",command = self.add_rec)
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
			self.adminWindow()
		else:
			print("Invalid Password")
			self.msg["text"] = "Invalid Password"
			self.msg.config(foreground = "red")

			self.password.delete(0,END)

class User:
	def __init__(self):
		pass
		

	def userWindow(self):
		self.user = Toplevel(self.master)
		self.user.title("User")
		self.user.minsize(width=300,height=100)
		self.user.register(False,False)

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

	def add_rec(self):
		# TODO: Add record by admin

		# 		from diff file
		# pass
		obj = Operations()
		key = (obj.add())
		temp = Database()
		# name,family_members,user_id
		temp.add_customer()
 		

	def delete_rec(self):
		# TODO: Delete record by admin
		obj = Operations()
		obj.delete()
		# pass

	def update_rec(self):
		# TODO: update the existing record by admin 
		#		Give appropriate msg if rec not present
		obj = Operations()
		key = (obj.search())
		# pass

def main():
	root = Tk()
	app = Application(root)
	root.mainloop()


if __name__ == "__main__":
	main()