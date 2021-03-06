import os
import cv2
from flask import Flask, render_template, Response

app = Flask(__name__)
# app.config['SEVER_NAME'] = 'localhost:1000'

cap = cv2.VideoCapture(0)

def gen_frame():
    while 1:
        #read camera frames
        ret,frame = cap.read()

        if not ret:
            break
        else:
            success,buffer=cv2.imencode('.jpg', frame)
            frame=buffer.tobytes()

        yield(b'--frame\r\n'
                    b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    return Response(gen_frame(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)

# if __name__ == '__main__':
#     app.run()
#     # app.run(port=int(os.environ.get('PORT', 33507)))


