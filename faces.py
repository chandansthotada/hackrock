import cv2
import os
import sqlite3
from datetime import datetime

# === Setup database ===
def init_db():
    conn = sqlite3.connect("voters.db")
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS users (
        aadhaar TEXT PRIMARY KEY,
        password TEXT
    )''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS votes (
        aadhaar TEXT PRIMARY KEY,
        party TEXT,
        timestamp TEXT
    )''')
    conn.commit()
    conn.close()

init_db()

# === Register user ===
def register_user(aadhaar, password):
    conn = sqlite3.connect("voters.db")
    cursor = conn.cursor()
    cursor.execute("INSERT OR REPLACE INTO users (aadhaar, password) VALUES (?, ?)", (aadhaar, password))
    conn.commit()
    conn.close()

# === Verify user credentials ===
def verify_user(aadhaar, password):
    conn = sqlite3.connect("voters.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE aadhaar=? AND password=?", (aadhaar, password))
    result = cursor.fetchone()
    conn.close()
    return result is not None

# === Capture face images for user ===
def capture_face(aadhaar):
    face_dir = f"faces/{aadhaar}"
    os.makedirs(face_dir, exist_ok=True)

    cap = cv2.VideoCapture(0)
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
    count = 0

    while count < 20:
        ret, frame = cap.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)
        for (x, y, w, h) in faces:
            face_img = frame[y:y+h, x:x+w]
            cv2.imwrite(f"{face_dir}/{count}.jpg", face_img)
            count += 1
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
        cv2.imshow("Capturing Face", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

# === Match live face with stored face images ===
def match_face(aadhaar):
    face_dir = f"faces/{aadhaar}"
    if not os.path.exists(face_dir):
        return False

    cap = cv2.VideoCapture(0)
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

    match_found = False
    ret, frame = cap.read()
    cap.release()

    if not ret:
        return False

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)

    for (x, y, w, h) in faces:
        live_face = gray[y:y+h, x:x+w]
        for img_file in os.listdir(face_dir):
            saved_img = cv2.imread(os.path.join(face_dir, img_file), cv2.IMREAD_GRAYSCALE)
            try:
                saved_face = cv2.resize(saved_img, (w, h))
                diff = cv2.absdiff(saved_face, live_face)
                score = diff.mean()
                if score < 50:  # Lower means more similar
                    match_found = True
                    break
            except:
                continue

    return match_found

# === Cast vote for a party ===
def cast_vote(aadhaar, party):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Insert the vote into the database
    conn = sqlite3.connect("voters.db")
    cursor = conn.cursor()
    cursor.execute("INSERT OR REPLACE INTO votes (aadhaar, party, timestamp) VALUES (?, ?, ?)",
                   (aadhaar, party, timestamp))
    conn.commit()
    conn.close()

    # Print the party name and timestamp in the console
    print(f"Vote casted for {party} at {timestamp}")