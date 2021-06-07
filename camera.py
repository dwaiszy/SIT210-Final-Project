from picamera import PiCamera
from time import sleep

import RPi.GPIO as GPIO
import numpy as np
import face_recognition
import requests

# GPIO config
GPIO_TRIGGER_GREEN = 21
GPIO_TRIGGER_RED = 20
GPIO.setmode(GPIO.BCM)
GPIO.setup(GPIO_TRIGGER_GREEN, GPIO.OUT)
GPIO.setup(GPIO_TRIGGER_RED, GPIO.OUT)

# Camera config
camera = PiCamera()
camera.resolution = (320, 240)
output = np.empty((240, 320, 3), dtype=np.uint8)

# Load owner's picture so Pi can recognize
print('Loading known face image(s)')
owner_image = face_recognition.load_image_file('lynguyen.jpg')
owner_face_encoding = face_recognition.face_encodings(owner_image)[0]

face_locations = []
face_encodings = []

try:
  camera.start_recording('/home/pi/Desktop/test.h264')
  while True:
    print('Capturing image.')
    # Capture a single frame as a numpy array
    camera.capture(output, format='rgb')

    # Find all faces and face encodings in current frame
    face_locations = face_recognition.face_locations(output)
    print('Found {} faces in image.'.format(len(face_locations)))
    face_encodings = face_recognition.face_encodings(output, face_locations)

    # Loop over all faces to authorize
    for face_encoding in face_encodings:
      match = face_recognition.compare_faces([owner_face_encoding], face_encoding)
    
      if match[0]:
        print('Hello Nhi')
        GPIO.output(GPIO_TRIGGER_GREEN, GPIO.HIGH)
        GPIO.output(GPIO_TRIGGER_RED, GPIO.LOW)
      else:
        print('ALERT, FOUND A UNKNOWN PERSON!')
        GPIO.output(GPIO_TRIGGER_RED, GPIO.HIGH)
        GPIO.output(GPIO_TRIGGER_GREEN, GPIO.LOW)

        # Send a notification to owner's phone
        r= requests.post('https://maker.ifttt.com/trigger/rpicamera/with/key/djogjsv9Tw1xPNTs0TBmf')

except KeyboardInterrupt:
  camera.stop_recording()
  GPIO.cleanup()

