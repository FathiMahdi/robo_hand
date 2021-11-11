import cv2
import mediapipe as mp
import serial
import time
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_hands = mp.solutions.hands

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

# For webcam input:
cap = cv2.VideoCapture() # change if you have multi cam
cap.open('http://172.18.39.139:8000')
arduino = serial.Serial(port='/dev/ttyACM0',baudrate=115200,timeout=0.1)
with mp_hands.Hands(
    max_num_hands=2,
    model_complexity=0,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5) as hands:
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
        print('landmarks:',hand_landmarks)
        print(
          f'Index finger tip coordinates: (',
          f'{hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].x * image_width}, '
          f'{hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].y * image_height})'
      )
        print('thump location: ',hand_landmarks.landmark[wrist].y*100)
        print('pinky location: ',hand_landmarks.landmark[pinky].y*100)
        print('ring finger  location: ',hand_landmarks.landmark[ring_finger].y*100)
        print('middle finger location: ',hand_landmarks.landmark[middle_finger].y*100)
        print('idex finger location: ',hand_landmarks.landmark[index_finger].y*100)
        #print('datatype: ',type(hand_landmarks.landmark[wrist].y)) # for debugging only
        #arduino.write('thump position'.encode())
        w = str(int(hand_landmarks.landmark[wrist].y*10))
        p = str(int(hand_landmarks.landmark[pinky].y*100))
        r_f = str(int(hand_landmarks.landmark[ring_finger].y*1000))
        m_f = str(int(hand_landmarks.landmark[middle_finger].y*10000))
        i_f = str(int(hand_landmarks.landmark[index_finger].y*100000))
        arduino.write(w.encode())
        #time.sleep(0.009)
        arduino.write(p.encode())
        #time.sleep(0.009)
        arduino.write(r_f.encode())
        #time.sleep(0.009)
        arduino.write(m_f.encode())
        #time.sleep(0.009)
        arduino.write(i_f.encode())
        time.sleep(0.2)
        #arduino.write(bytes(hand_landmarks.landmark[pinky],'utf-8'))
        #time.sleep(0.05)
        #arduino.write(bytes(hand_landmarks.landmark[wring_finger],'utf-8'))
        #time.sleep(0.05)
        #arduino.write(bytes(hand_landmarks.landmark[middle_finger],'utf-8'))
        #time.sleep(0.05)
        #arduino.write(bytes(hand_landmarks.landmark[index_finger],'utf-8'))
        #time.sleep(0.05)
        mp_drawing.draw_landmarks(
            image,
            hand_landmarks,
            mp_hands.HAND_CONNECTIONS,
            mp_drawing_styles.get_default_hand_landmarks_style(),
            mp_drawing_styles.get_default_hand_connections_style())
    # Flip the image horizontally for a selfie-view display.
    cv2.imshow('MediaPipe Hands', cv2.flip(image, 1))
    if cv2.waitKey(5) & 0xFF == 27:
      break
cap.release()
