from flask import Flask,render_template,Response,url_for
import cv2
img=cv2.imread("cr7lm10.jpg")
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
app=Flask(__name__)
def generate():
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=6)
    for (x, y, w, h) in faces:
        cv2.rectangle(img, (x, y), (x+w, y+h), (255, 0, 0), 2)
        ret, buffer = cv2.imencode('.jpg', img)
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
