# basic pid concept code from Digikey: https://www.youtube.com/watch?v=tFVAaUcOm4I
import math
import time
#from TurtlePose import TurtlePose
from turtle import *

# Class to keep track of the current 2D position of a turtle, or a desired turtle position
class TurtlePose:

    # x, y, and rot are ints. rot represents degrees, turtle is a turtle object, and hideTurtle determines whether the turtle should be hidden.
    def __init__(self, x, y, rot, hideTurtle):
        self.x = x
        self.y = y
        self.rot = rot
        self.turtle = Turtle()
        if hideTurtle:
            self.turtle.hideturtle()
        self.turtle.penup()
        self.turtle.goto(x,y)
        self.turtle.setheading(rot)


    def setPos(self, x, y, rot):
        self.x = x
        self.y = y
        self.rot = rot
        self.turtle.goto(x, y)
        self.turtle.setheading(rot)

    def incrementRot(self, deltaRot):
        self.rot += deltaRot
        self.turtle.setheading(self.rot)

    def incrementXY(self, x, y):
        self.x += x
        self.y += y
        self.turtle.goto(self.x, self.y)

    def getX(self):
        return self.x

    def getY(self):
        return self.y

    def getRot(self):
        return self.rot
    
    def printPos(self):
        print("Turtle Position | X: ", self.x, " Y: ", self.y, " Theta:", self.rot)

    def distanceFromOrigin(self):
        return ((self.x ** 2) + (self.y ** 2)) ** 0.5

    def setSpeed(self, speed):
        self.turtle.speed(speed)

class PIDProfile:

    def __init__(self): 
            # Initialize variables
        self.k_p = 0.1
        self.k_i = 0
        self.k_d = 0.0
        self.k_pTheta = 0.1
        self.k_iTheta = 0.0
        self.k_dTheta = 0.0
        self.interval = 0.08 # interval should be replaced with current time - previoustime (which is stored in a variable in the while loop

        self.xError_prev = 0
        self.xIntegral = 0
        self.yError_prev = 0
        self.yIntegral = 0
        self.thetaError_prev = 0
        self.thetaIntegral = 0
        self.x_setpoint = 0
        self.y_setpoint = 0
        self.theta_setpoint = 0

    def setSetpoint(self, x_new, y_new, theta_new):
        self.x_setpoint = x_new
        self.y_setpoint = y_new
        self.theta_setpoint = theta_new

    def setPIDConstants(self, newKp, newKi, newKd, newKpTheta, newKiTheta, newKdTheta):
        self.k_p = newKp
        self.k_i = newKi
        self.k_d = newKd
        self.k_pTheta = newKpTheta
        self.k_iTheta = newKiTheta
        self.k_dTheta = newKdTheta

    def getOutput(self, currentX, currentY, currentTheta, x_setpoint, y_setpoint, theta_setpoint):

        # Get value from object
        xVal = currentX
        yVal = currentY
        thetaVal = currentTheta

        # Calculate the PID terms
        self.xError = x_setpoint - xVal
        self.xIntegral = self.xIntegral + (self.xError * self.interval)
        self.xDerivative = (self.xError - self.xError_prev) / self.interval
        xOutput = (self.k_p * self.xError) + (self.k_i * self.xIntegral) + (self.k_d * self.xDerivative)

        self.yError = y_setpoint - yVal
        self.yIntegral = self.yIntegral + (self.yError * self.interval)
        self.yDerivative = (self.yError - self.yError_prev) / self.interval
        yOutput = (self.k_p * self.yError) + (self.k_i * self.yIntegral) + (self.k_d * self.yDerivative)

        self.thetaError = theta_setpoint - thetaVal
        self.thetaIntegral = self.thetaIntegral + (self.thetaError * self.interval)
        self.thetaDerivative = (self.thetaError - self.thetaError_prev) / self.interval
        thetaOutput = (self.k_pTheta * self.thetaError) + (self.k_iTheta * self.thetaIntegral) + (self.k_dTheta * self.thetaDerivative)
    
    # Save value for next iteration
        self.xError_prev = self.xError
        self.yError_prev = self.yError
        self.thetaError_prev = self.thetaError

        print("Turtle Output | X: ", xOutput, " Y: ", yOutput, " Theta:", thetaOutput)

        # Return the output values
        return xOutput, yOutput, thetaOutput

    # Return errors
    def errors(self):
        return self.xError_prev, self.yError_prev, self.thetaError_prev

    def reset(self):
        self.xError_prev = 0
        self.xIntegral = 0
        self.yError_prev = 0
        self.yIntegral = 0
        self.thetaError_prev = 0
        self.thetaIntegral = 0
        PIDProfile.setSetpoint(0,0,0)
    
def promptUser():
    while True:
        try:
            x_val = int(input("Enter the X coordinate, an integer between -200 and 200 "))
            y_val = int(input("Enter the Y coordinate, an integer between -200 and 200 "))
            theta_val = int(input("Enter the rotation coordinate in degrees: ")) % 360
            if abs(x_val) <= 200 and abs(y_val <=200) and theta_val > -1:
                return x_val, y_val, theta_val
            else:
                print("Out of range input or inputs. Please enter integer values between +/- 200 for X and Y, and between 0 and 359 for theta.")
        except ValueError:
            print("Invalid input. Please enter integer values between -200 and 200 for X and Y, and an integer between 0 and 359 for theta.")

def promptUserTolerance():    
    while True:
        try:
            transTolerance = float(input("Enter the translational tolerance, preferably a small number, under 1: "))
            rotTolerance = float(input("Enter the rotational tolerance of the turtle in degrees, preferably a small number: "))
            return transTolerance, rotTolerance
        except ValueError:
            print("Invalid input. Please type a number instead.")
    
# Create our robot turtle
space = Screen()
# global Nocturne
ourTurtle = TurtlePose(0,0,0, False)

# Set turtle speed.
ourTurtle.setSpeed(0)

# Display the turtle object
ourTurtle.printPos()

# Create PID controller instance
pid_controller = PIDProfile()

while True:
    xGoal, yGoal, thetaGoal = promptUser()
    transTolerance, rotTolerance = promptUserTolerance()
    pid_controller.setSetpoint(xGoal, yGoal, thetaGoal)

    # Call getOutput in the pid controller so it calculates the error for the while loop
    xOut, yOut, thetaOut = pid_controller.getOutput(ourTurtle.getX(), ourTurtle.getY(), ourTurtle.getRot(), xGoal, yGoal, thetaGoal)

    while math.sqrt(pow(pid_controller.errors()[0], 2) + pow(pid_controller.errors()[1], 2)) > transTolerance or abs(pid_controller.errors()[2] > rotTolerance):
        #   Get current position of turtle object
        #   Feed into PID Controller
        xOut, yOut, thetaOut = pid_controller.getOutput(ourTurtle.getX(), ourTurtle.getY(), ourTurtle.getRot(), xGoal, yGoal, thetaGoal)
        #   Add output to current position
        #  Update turtle object position

        ourTurtle.incrementXY(xOut, yOut)
        ourTurtle.incrementRot(thetaOut)
        ourTurtle.printPos()
        time.sleep(0.02)

    print("Turtle within tolerance!")
    input("Want to move again? Press ENTER to continue.")