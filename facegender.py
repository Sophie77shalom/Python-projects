import cv2
import numpy as np
import face_recognition

# Load the cascade classifier for face detection
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades+'haarcascade_frontalface_default.xml')

# Load the input image
image_path =(r"C:\Users\sophy\Pictures\Camera Roll\group-of-people-18.jpg")
image = cv2.imread(image_path)

# Convert the image to grayscale
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Detect faces in the image using the cascade classifier
faces = face_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=3, minSize=(30, 30))

# Loop over each detected face
for (x, y, w, h) in faces:
    # Crop the face from the image
    face_image = image[y:y+h, x:x+w]

    # Use the face_recognition library to estimate the age and gender of the face
    face_encoding = face_recognition.face_encodings(face_image)[0]
    face_data = face_recognition.face_landmarks(face_image)
    age = face_recognition.api.age_and_gender(face_image)[0]
    gender = "Male" if face_recognition.api.age_and_gender(face_image)[1][0] > 0.5 else "Female"
    
    # Draw a rectangle around the face and label it with the estimated age and gender
    cv2.rectangle(image, (x, y), (x+w, y+h), (0, 255, 0), 2)
    cv2.putText(image, f"{gender}, {age}", (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)

# Display the output image
cv2.imshow("Faces Detected", image)
cv2.waitKey(0)
cv2.destroyAllWindows()
