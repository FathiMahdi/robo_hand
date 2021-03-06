###############################################################################################################


# Robotic hand control using landmark detection
# hand landmark detector
# Fathi Mahdi Elsiddig
# 10/11/2021
# This code deyect the hand landmarks in real time and send the data to Arduino board through serial communication 


##############################################################################################################


import cv2
import mediapipe as mp
import serial
import time
import numpy as np
########################################################################################################

mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_hands = mp.solutions.hands

#######################################################################################################

# For static images:
IMAGE_FILES = []
with mp_hands.Hands(
    static_image_mode=True,
    max_num_hands=1,
    min_detection_confidence=0.5) as hands:
  for idx, file in enumerate(IMAGE_FILES):
    # Read an image, flip it around y-axis for correct handedness output (see
    # above).
    image = cv2.flip(cv2.imread(file), 1)
    # Convert the BGR image to RGB before processing.
    results = hands.process(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))

    # Print handedness and draw hand landmarks on the image.
    print('Handedness:', results.multi_handedness)
    if not results.multi_hand_landmarks:
      continue
    image_height, image_width, _ = image.shape
    annotated_image = image.copy()
    for hand_landmarks in results.multi_hand_landmarks:
      print('hand_landmarks:', hand_landmarks)
      print(
          f'Index finger tip coordinates: (',
          f'{hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].x * image_width}, '
          f'{hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].y * image_height})'
      )
      mp_drawing.draw_landmarks(
          annotated_image,
          hand_landmarks,
          mp_hands.HAND_CONNECTIONS,
          mp_drawing_styles.get_default_hand_landmarks_style(),
          mp_drawing_styles.get_default_hand_connections_style())
    cv2.imwrite(
        '/tmp/annotated_image' + str(idx) + '.png', cv2.flip(annotated_image, 1))
    # Draw hand world landmarks.
    if not results.multi_hand_world_landmarks:
      continue
    for hand_world_landmarks in results.multi_hand_world_landmarks:
      mp_drawing.plot_landmarks(
        hand_world_landmarks, mp_hands.HAND_CONNECTIONS, azimuth=5)
#########################################################################################################

# For webcam input:
cap = cv2.VideoCapture() # change if you have multi cam
cap.open('http://172.18.39.139:8000')
arduino = serial.Serial(port='/dev/ttyACM0',baudrate=2000000,timeout=0.8)
with mp_hands.Hands(
    max_num_hands=1,
    model_complexity=0,
    min_detection_confidence=0.8,
    min_tracking_confidence=0.8) as hands:
  while cap.isOpened():
    success, image = cap.read()
    if not success:
      print("Ignoring empty camera frame.")
      # If loading a video, use 'break' instead of 'continue'.
      continue

    # To improve performance, optionally mark the image as not writeable to
    # pass by reference.
    image.flags.writeable = False
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    results = hands.process(image)
    counter = 0 # landmark counter
    wrist = 4
    pinky = 20
    ring_finger = 16
    middle_finger = 12
    index_finger = 8
    # Draw the hand annotations on the image.
    image.flags.writeable = True
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    image_height, image_width, _ = image.shape
    counter = 0
    if results.multi_hand_landmarks:
      for hand_landmarks in results.multi_hand_landmarks:
        #print('landmarks:',hand_landmarks)
        #print(
          #f'Index finger tip coordinates: (',
          #f'{hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].x * image_width}, '
          #f'{hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].y * image_height})'
      #)
        #print('thump location: ',hand_landmarks.landmark[wrist].y)
        #print('pinky location: ',hand_landmarks.landmark[pinky].y)
        #print('ring finger  location: ',hand_landmarks.landmark[ring_finger].y)
        #print('middle finger location: ',hand_landmarks.landmark[middle_finger].y)
        #print('idex finger location: ',hand_landmarks.landmark[index_finger].y)
        #print('datatype: ',type(hand_landmarks.landmark[wrist].y)) # for debugging only
        #arduino.write('thump position'.encode())
        w = str(round(hand_landmarks.landmark[wrist].y,3))
        p = str(round(hand_landmarks.landmark[pinky].y,3))
        r_f = str(round(hand_landmarks.landmark[ring_finger].y,3))
        m_f = str(round(hand_landmarks.landmark[middle_finger].y,3))
        i_f = round(hand_landmarks.landmark[index_finger].y,3)
        if (i_f >= 0.7):
            i_f = 0.7
        elif (i_f <= 0.4 and i_f > 0.7):
            i_f = 0.4
        i_f = str(i_f)
        print('idex finger location: ',w)
        arduino.write(bytes(w+','+p+','+r_f+','+m_f+','+i_f,'utf-8'))
        #time.sleep(0.005)
        mp_drawing.draw_landmarks(
            image,
            hand_landmarks,
            mp_hands.HAND_CONNECTIONS,
            mp_drawing_styles.get_default_hand_landmarks_style(),
            mp_drawing_styles.get_default_hand_connections_style())
        x = [landmark.x for landmark in hand_landmarks.landmark]
        y = [landmark.y for landmark in hand_landmarks.landmark]
        center = np.array([np.mean(x)*image_width, np.mean(y)*image_height]).astype('int32')
        cv2.rectangle(image, (center[0]-300,center[1]-300), (center[0]+300,center[1]+300), (255,0,0), 2)
    # Flip the image horizontally for a selfie-view display.
    cv2.imshow('MediaPipe Hands', cv2.flip(image, 1))
    if cv2.waitKey(5) & 0xFF == 27:
      break
cap.release()
arduino.close()
