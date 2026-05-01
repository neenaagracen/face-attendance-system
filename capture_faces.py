import cv2
import os

name = input("Enter student name: ")
path = f"dataset/{name}"

os.makedirs(path, exist_ok=True)

cap = cv2.VideoCapture(0)
count = 0

print("Press ESC to stop")

while True:
    ret, frame = cap.read()
    if not ret:
        break

    cv2.imshow("Capture Faces", frame)

    # Save image
    cv2.imwrite(f"{path}/{count}.jpg", frame)
    count += 1

    if count == 30:
        break

    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()

print("Images captured successfully!")
