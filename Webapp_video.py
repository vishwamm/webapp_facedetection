from flask import Flask,render_template,Response,url_for
import cv2
img=cv2.VideoCapture(0)
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
app=Flask(__name__)
def generate():
    while True:
        ret, frame = img.read()
        if not ret:
            break
        else:
            ret, frame = img.read()
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=6)
            for (x, y, w, h) in faces:
                cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)
                ret, buffer = cv2.imencode('.jpg', frame)
                frame_bytes = buffer.tobytes()
                yield(b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes  + b'\r\n')
@app.route('/')
def index():
    return render_template('face_camera.html')
@app.route("/webcam")
def webcam():
    return Response(generate(), mimetype='multipart/x-mixed-replace; boundary=frame')
if __name__ == '__main__':
    app.run(debug=True)
