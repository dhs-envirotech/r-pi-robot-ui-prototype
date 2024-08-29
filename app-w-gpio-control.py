from flask import Flask, render_template, request
import RPi.GPIO as GPIO
import time

app = Flask(__name__)

# Set up GPIO for motor control
motor_pin = 18
GPIO.setmode(GPIO.BCM)
GPIO.setup(motor_pin, GPIO.OUT)
pwm = GPIO.PWM(motor_pin, 1000)
pwm.start(0)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/control', methods=['POST'])
def control():
    data = request.get_json()
    angle = data['angle']
    force = data['force']

    # Convert joystick data to PWM duty cycle
    duty_cycle = angle / 180 * 100

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
