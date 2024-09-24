from flask import Flask, render_template, Response, request
import RPi.GPIO as GPIO
import time
import cv2

app = Flask(__name__)

# Set up GPIO for motor control
motor_pin = 18
GPIO.setmode(GPIO.BCM)
GPIO.setup(motor_pin, GPIO.OUT)
pwm = GPIO.PWM(motor_pin, 1000)
pwm.start(0)

# Set up the camera
camera = cv2.VideoCapture(0)  # Use the default camera

def gen_frames():
    while True:
        success, frame = camera.read()  # Read the camera frame
        if not success:
            break
        else:
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/control', methods=['POST'])
def control():
    data = request.get_json()
    angle = data['angle']
    force = data['force']

    # Convert joystick data to PWM duty cycle
    duty_cycle = (force / 100) * 100  # Normalize force to PWM duty cycle

    # Apply PWM to control motor speed
    pwm.ChangeDutyCycle(duty_cycle)

    return 'OK'

@app.route('/stop', methods=['POST'])
def stop():
    # Stop the motor when the joystick is released
    pwm.ChangeDutyCycle(0)
    return 'OK'

if __name__ == '__main__':
    app.run(debug=True)
