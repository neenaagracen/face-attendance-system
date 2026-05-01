import streamlit as st
import cv2
import face_recognition
import pickle
import pandas as pd
from datetime import datetime
import os

# Load model
with open("models/face_model.pkl", "rb") as f:
    data = pickle.load(f)

# Create attendance folder/file
os.makedirs("attendance", exist_ok=True)
attendance_file = "attendance/attendance.csv"

if not os.path.exists(attendance_file):
    pd.DataFrame(columns=["Name", "Time"]).to_csv(attendance_file, index=False)

st.title("🎓 Face Detection Attendance System")

menu = ["Register Face", "Mark Attendance", "View Attendance"]
choice = st.sidebar.selectbox("Menu", menu)

# ---------------- REGISTER ----------------
if choice == "Register Face":
    st.subheader("Register New Student")

    name = st.text_input("Enter Student Name")

    if st.button("Capture Faces"):
        if name == "":
            st.warning("Please enter a name")
        else:
            path = f"dataset/{name}"
            os.makedirs(path, exist_ok=True)

            cap = cv2.VideoCapture(0)
            count = 0

            st.info("Press ESC to stop")

            while count < 20:
                ret, frame = cap.read()
                if not ret:
                    break

                cv2.imshow("Register Face", frame)
                cv2.imwrite(f"{path}/{count}.jpg", frame)
                count += 1

                if cv2.waitKey(1) & 0xFF == 27:
                    break

            cap.release()
            cv2.destroyAllWindows()

            st.success("Face Registered Successfully!")

# ---------------- ATTENDANCE ----------------
elif choice == "Mark Attendance":
    st.subheader("Live Attendance")
    run = st.button("Start Camera")

    if run:
        cap = cv2.VideoCapture(0)

        while True:
            ret, frame = cap.read()
            if not ret:
                break

            rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            faces = face_recognition.face_locations(rgb)
            encodings = face_recognition.face_encodings(rgb, faces)

            for encoding, face in zip(encodings, faces):
                matches = face_recognition.compare_faces(data["encodings"], encoding)
                name = "Unknown"

                if True in matches:
                    index = matches.index(True)
                    name = data["names"][index]

                    if name != "Unknown":
                        df_existing = pd.read_csv(attendance_file)
                        today = datetime.now().strftime("%Y-%m-%d")

                        if not ((df_existing["Name"] == name) &
                                (df_existing["Time"].str.startswith(today))).any():

                            now = datetime.now()
                            dt_string = now.strftime("%Y-%m-%d %H:%M:%S")

                            df = pd.DataFrame([[name, dt_string]], columns=["Name", "Time"])
                            df.to_csv(attendance_file, mode='a', header=False, index=False)

                            st.success(f"{name} marked at {dt_string}")

                top, right, bottom, left = face
                cv2.rectangle(frame, (left, top), (right, bottom), (0,255,0), 2)
                cv2.putText(frame, name, (left, top-10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0,255,0), 2)

            cv2.imshow("Attendance", frame)

            if cv2.waitKey(1) & 0xFF == 27:
                break

        cap.release()
        cv2.destroyAllWindows()

# ---------------- VIEW ----------------
elif choice == "View Attendance":
    st.subheader("Attendance Records")
    df = pd.read_csv(attendance_file)
    st.dataframe(df)