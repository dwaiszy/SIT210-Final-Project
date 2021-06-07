import RPi.GPIO as GPIO
from time import sleep

import requests
import smbus
import logging
import os

import Adafruit_DHT

from flask import Flask
from flask_ask import Ask, request, session, question, statement

app = Flask(__name__)
ask = Ask(app, '/')
logging.getLogger('flask_ask').setLevel(logging.DEBUG)


@ask.launch
def launch():
  return question('Hi there, you have any task for me to do?').simple_card('Alexa and Pi are ready!')

@ask.intent('AskTempIntent')
def tempFunc():
  #sensor = Adafruit_DHT.DHT11
  #gpio = 26
  #humidity, temperature = Adafruit_DHT.read_retry(sensor, gpio)
  #if temperature is None:
  temperature = 13
  answer = 'Current temperature is ' + str(temperature) + ' Celsius degree'
  return statement(answer).simple_card(answer)

@ask.intent('StarterIntent')
def startFunc():
  lightLevel = readLight()
  question_text = 'Light control is ready. Current light level is ' + determineLightLevel(lightLevel) + '. Would you like to adjust?'
  reprompt_text = 'Make sure Echo can hear you'
  return question(question_text).reprompt(reprompt_text).simple_card(question_text)

@ask.intent('LightOnIntent')
def turnLightOn():
  GPIO_TRIGGER = 21
  GPIO.setwarnings(False)
  GPIO.setmode(GPIO.BCM)
  GPIO.setup(GPIO_TRIGGER, GPIO.OUT)

  GPIO.output(GPIO_TRIGGER, GPIO.HIGH)
  text = 'Your light has been turned on'
  return statement(text).simple_card(text)

@ask.intent('LightOffIntent')
def turnLightOff():
  GPIO_TRIGGER = 21
  GPIO.setwarnings(False)
  GPIO.setmode(GPIO.BCM)
  GPIO.setup(GPIO_TRIGGER, GPIO.OUT)

  GPIO.output(GPIO_TRIGGER, GPIO.LOW)
  text = 'Your light has been turned off'
  return statement(text).simple_card(text)

@ask.intent('AMAZON.HelpIntent')
def help():
  text = 'Please say hello to test out the system'
  return question(text).simple_card('Hello from Alexa and Pi')

@ask.session_ended
def sessionEnded():
  GPIO.cleanup()
  return '{}', 200

DEVICE = 0x23
ONE_TIME_HIGH_RES_MODE = 0x20

bus = smbus.SMBus(1)

def determineLightLevel(lightLevel):
  if lightLevel < 100:
    return 'Low'
  elif lightLevel > 300:
    return 'High'
  else:
    return 'Normal'

def convertToNumber(data):
  result = (data[1] + (256 * data[0])) / 1.2
  return result

def readLight():
  data = bus.read_i2c_block_data(DEVICE, ONE_TIME_HIGH_RES_MODE)
  return convertToNumber(data)


if __name__ == "__main__":
  app.run(debug=True)
