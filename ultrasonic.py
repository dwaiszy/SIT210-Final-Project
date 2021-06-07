from gpiozero import DistanceSensor, Buzzer
import RPi.GPIO as GPIO
from time import sleep

# GPIO config
GPIO_TRIGGER = 27
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(GPIO_TRIGGER, GPIO.OUT)

# Setup buzzer
buzzer = GPIO.PWM(GPIO_TRIGGER, 1000)
buzzer.start(10)

ultrasonic = DistanceSensor(echo=17, trigger=4, threshold_distance=0.5)

def on():
  buzzer.ChangeDutyCycle(10)

def off():
  buzzer.ChangeDutyCycle(0)

try:
  while True:
    ultrasonic.when_in_range = on
    ultrasonic.when_out_of_range = off
    sleep(0.5)
except KeyboardInterrupt:
  GPIO.cleanup()
