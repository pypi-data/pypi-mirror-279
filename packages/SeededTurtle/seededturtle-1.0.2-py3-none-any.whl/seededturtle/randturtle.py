import random
import turtle as t
from time import sleep
import regex as re

class RandomTurtleValueError(Exception):
    def __init__(self, message):
        self.message = message

def generateRandomSeed(): #returns a random seed which is a string containing 0-9, a-z, and A-Z
    return ''.join(random.choice('0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!@#$%^&*()') for i in range(16))

def generateRandomColor(): #returns a string of three comma seperated integers between 0 and 255 representing R, G, and B values
    return str(random.randint(0, 255)) + "," + str(random.randint(0, 255)) + "," + str(random.randint(0, 255))

#   The Algorithm for generating a random turtle from a seed is as follows:
#   Randomize the value that we use for random.randint() and random.random()
#   by setting random.seed() to the seed passed in, whether that was randomly
#   generated or inputted by the user. Also has optional parameters for time,
#   color, and fill color. If fill is set to "none" then the turtle will not
#   be filled. If color is set to "random" then the turtle will be filled with
#   a random color. If color or fill is set to a string of three comma seperated
#   integers in the format "R,G,B" then the turtle will be filled/colored with that
#   color. The time parameter is the time in seconds that the turtle will be displayed
#   for before doing anything else (sleeps the thread). The function returns the turtle
#   object that was created. If invalid parameters are passed in, the function
#   will return raise a RandomTurtleValueError.

def generateRandomTurtle(seed, time=0, fill="none", color="random", iterations=100):
    if re.match(r'^[0-9a-zA-Z!@#$%^&*()]{16,}$', seed.strip()) == None:
        raise RandomTurtleValueError("Invalid seed value passed in: %s" % seed)
    elif color != "random" and re.match(r'^[0-9]{1,3},[0-9]{1,3},[0-9]{1,3}$', color) == None and color != "random":
        raise RandomTurtleValueError("Invalid color value passed in: %s" % color)
    elif fill != "none" and re.match(r'^[0-9]{1,3},[0-9]{1,3},[0-9]{1,3}$', fill) == None:
        raise RandomTurtleValueError("Invalid fill value passed in: %s" % fill)
    myturtle = t.Turtle()
    myturtle.screen.colormode(255);
    myturtle.speed(0)
    colorString = color
    random.seed(seed)
    if fill!="none":
        myturtle.fillcolor(int(fill.split(',')[0]), int(fill.split(',')[1]), int(fill.split(',')[2]))
        myturtle.begin_fill()
    angle = int(random.randint(25,180))
    steps = int(500*(angle/180))
    for i in range(0, iterations):
        if color == "random":
            colorString = generateRandomColor()
        colorArray = colorString.split(",")
        myturtle.color(int(colorArray[0]), int(colorArray[1]), int(colorArray[2]))
        myturtle.right(angle)
        if i==0:
            myturtle.backward(int(steps/2))
        myturtle.forward(steps)
    if fill=="none":
        myturtle.end_fill()
    sleep(time)
    return myturtle