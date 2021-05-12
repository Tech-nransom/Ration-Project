import time
import hashlib
from pyfingerprint.pyfingerprint import PyFingerprint

class Operations:
	def delete(self,position):
		try:
		    f = PyFingerprint('/dev/ttyUSB0', 57600, 0xFFFFFFFF, 0x00000000)

		    if ( f.verifyPassword() == False ):
		        raise ValueError('The given fingerprint sensor password is wrong!')

		except Exception as e:
		    print('The fingerprint sensor could not be initialized!')
		    print('Exception message: ' + str(e))
		    exit(1)

		## Gets some sensor information
		print('Currently used templates: ' + str(f.getTemplateCount()) +'/'+ str(f.getStorageCapacity()))

		## Tries to delete the template of the finger
		try:
		    positionNumber = position
		    positionNumber = int(positionNumber)

		    if ( f.deleteTemplate(positionNumber) == True ):
		        print('Template deleted!')

		except Exception as e:
		    print('Operation failed!')
		    print('Exception message: ' + str(e))
		    exit(1)

	def update(self):
		pass

	def add(self):

		try:
		    f = PyFingerprint('/dev/ttyUSB0', 57600, 0xFFFFFFFF, 0x00000000)

		    if ( f.verifyPassword() == False ):
		        raise ValueError('The given fingerprint sensor password is wrong!')

		except Exception as e:
		    print('The fingerprint sensor could not be initialized!')
		    print('Exception message: ' + str(e))
		    return -1,-1
		    exit(1)

		## Gets some sensor information
		print('Currently used templates: ' + str(f.getTemplateCount()) +'/'+ str(f.getStorageCapacity()))

		

		## Tries to enroll new finger
		try:
			print('Waiting for finger...')

			while (f.readImage() == False):
				pass

		    ## Converts read image to characteristics and stores it in charbuffer 1
			f.convertImage(0x01)

			## Checks if finger is already enrolled
			result = f.searchTemplate()
			positionNumber = result[0]

			if ( positionNumber >= 0 ):
			    print('Template already exists at position #' + str(positionNumber))
			    exit(0)

			print('Remove finger...')
			time.sleep(2)

			print('Waiting for same finger again...')

			## Wait that finger is read again
			while ( f.readImage() == False ):
			    pass

			## Converts read image to characteristics and stores it in charbuffer 2
			f.convertImage(0x02)

			## Compares the charbuffers
			if ( f.compareCharacteristics() == 0 ):
			    raise Exception('Fingers do not match')

			## Creates a template
			f.createTemplate()

			## Saves template at new position number
			positionNumber = f.storeTemplate()
			print('Finger enrolled successfully!')
			print('New template position #' + str(positionNumber))
			return self.getHash(f,positionNumber),int(positionNumber)

		except Exception as e:
		    print('Operation failed!')
		    print('Exception message: ' + str(e))
		    return -1,-1
		    exit(1)

	def search(self):
		try:
		    f = PyFingerprint('/dev/ttyUSB0', 57600, 0xFFFFFFFF, 0x00000000)

		    if ( f.verifyPassword() == False ):
		        raise ValueError('The given fingerprint sensor password is wrong!')

		except Exception as e:
		    print('The fingerprint sensor could not be initialized!')
		    print('Exception message: ' + str(e))
		  
		    exit(1)

		## Gets some sensor information
		print('Currently used templates: ' + str(f.getTemplateCount()) +'/'+ str(f.getStorageCapacity()))

		## Tries to search the finger and calculate hash
		try:
		    print('Waiting for finger...')

		    ## Wait that finger is read
		    while ( f.readImage() == False ):
		        pass

		    ## Converts read image to characteristics and stores it in charbuffer 1
		    f.convertImage(0x01)

		    ## Searchs template
		    result = f.searchTemplate()

		    positionNumber = result[0]
		    accuracyScore = result[1]

		    if ( positionNumber == -1 ):
		        print('No match found!')
		        return -1,-1
		        exit(0)
		    else:
		    	print('Found template at position #' + str(positionNumber))
		    	print('The accuracy score is: ' + str(accuracyScore))
		    	f.loadTemplate(positionNumber, 0x01)
		    	characterics = str(f.downloadCharacteristics(0x01)).encode('utf-8')
		    	return hashlib.sha256(characterics).hexdigest(),positionNumber
		except Exception as e:
		    print('Operation failed!')
		    print('Exception message: ' + str(e))
		    return -1,-1
		    exit(1)

	def getHash(self,fingerPrint,positionNumber):
		fingerPrint.convertImage(0x01)

		## Searchs template
		result = fingerPrint.searchTemplate()

		
		# accuracyScore = result[1]
		if positionNumber != -1:
			fingerPrint.loadTemplate(positionNumber, 0x01)

			## Downloads the characteristics of template loaded in charbuffer 1
			characterics = str(fingerPrint.downloadCharacteristics(0x01)).encode('utf-8')

			## Hashes characteristics of template
			return (hashlib.sha256(characterics).hexdigest())
		else:
			return -1

# # Program for delete

# from pyfingerprint.pyfingerprint import PyFingerprint


# ## Deletes a finger from sensor
# ##


# ## Tries to initialize the sensor





# # program for enroll

# import time
# from pyfingerprint.pyfingerprint import PyFingerprint


# ## Enrolls new finger
# ##

# ## Tries to initialize the sensor


# # program for search

# import hashlib
# from pyfingerprint.pyfingerprint import PyFingerprint


# ## Search for a finger
# ##

# ## Tries to initialize the sensor
