import numpy as np
import cv2
import os
import imutils

NMS_THRESHOLD=0.3
MIN_CONFIDENCE=0.2

import cv2

# Load an image from file
image = cv2.imread("C:/Users/sophy/Pictures/walking.jpg")

# Resize the image
image = cv2.resize(image, (416, 416))

# Convert the image to a blob
blob = cv2.dnn.blobFromImage(image, 1 / 255.0, (416, 416), swapRB=True, crop=False)

config_path = 'path/to/config/file.cfg'
weights_path = 'path/to/weights/file.weights'
layer_name = 'yolo_layer_name'
personidz = 0  # ID of the person class

model = cv2.dnn.readNetFromDarknet(config_path, weights_path)

model.setInput(blob)
layerOutputs = model.forward(layer_name)

boxes = []
centroids = []
confidences = []

(H, W) = image.shape[:2]

for output in layerOutputs:
    for detection in output:
         scores = detection[5:]
         classID = np.argmax(scores)
         confidence = scores[classID]

         if classID == personidz and confidence > MIN_CONFIDENCE:
              box = detection[0:4] * np.array([W, H, W, H])
              (centerX, centerY, width, height) = box.astype("int")

              x = int(centerX - (width / 2))
              y = int(centerY - (height / 2))

              boxes.append([x, y, int(width), int(height)])
              centroids.append((centerX, centerY))
              confidences.append(float(confidence))

idxs = cv2.dnn.NMSBoxes(boxes, confidences, MIN_CONFIDENCE, NMS_THRESHOLD)

if len(idxs) > 0:
    for i in idxs.flatten():
        (x, y) = (boxes[i][0], boxes[i][1])
        (w, h) = (boxes[i][2], boxes[i][3])

        cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)

cv2.imshow("Output", image)
cv2.waitKey(0)