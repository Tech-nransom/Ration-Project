import RPi.GPIO as GPIO
import time

def playMotor():
	GPIO.setmode(GPIO.BOARD)
	GPIO.setwarnings(False)
	DC_Motor_Pin1 = 11
	DC_Motor_Pin2 = 13
	GPIO.setup(DC_Motor_Pin1,GPIO.OUT)
	GPIO.setup(DC_Motor_Pin2,GPIO.OUT)
	GPIO.output(DC_Motor_Pin1,GPIO.LOW)
	GPIO.output(DC_Motor_Pin2,GPIO.LOW)
	time.sleep(1)
	GPIO.output(DC_Motor_Pin1,GPIO.HIGH)
	GPIO.output(DC_Motor_Pin2,GPIO.LOW)
	time.sleep(2)
	GPIO.output(DC_Motor_Pin1,GPIO.LOW)
	GPIO.output(DC_Motor_Pin2,GPIO.LOW)
	time.sleep(10)