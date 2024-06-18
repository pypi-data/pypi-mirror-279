import seededturtle.randturtle as randturtle
import turtle as t
import random
import pytest
import regex as re
from time import sleep

def test_heartTurtle(): #prints a pinkheart using basic turtle commands (turning, forward, backward, etc.)
        myturtle = t.Turtle()
        myturtle.fillcolor("pink")
        myturtle.begin_fill()
        myturtle.left(50)
        myturtle.forward(133)
        myturtle.circle(50, 200)
        myturtle.right(140)
        myturtle.circle(50, 200)
        myturtle.forward(133)
        myturtle.end_fill()
        #clear the screen
        t.clearscreen()
        assert True == True


def test_randturtle():
    assert re.match(r'^[0-9a-zA-Z!@#$%^&*()]{16}$', randturtle.generateRandomSeed().strip()) is not None #matches the regex pattern
    for n in range(0, 2):
        myturtle = randturtle.generateRandomTurtle(randturtle.generateRandomSeed(), 1.5)
        t.clearscreen()
    assert True == True

def test_randturtle_declaredseed():
    myseed = "I1Ov3rUxToNsR4NdTuRtLeS1234$$"
    assert re.match(r'^[0-9a-zA-Z!@#$%^&*()]{16,}$', myseed.strip()) is not None #matches the regex pattern
    myturtle = randturtle.generateRandomTurtle(myseed, 1.5)
    t.clearscreen()
    assert True == True

def test_randturtle_staticcolor():
    myseed = "I1Ov3rUxToNsR4NdTuRtLeS1234$$"
    assert re.match(r'^[0-9a-zA-Z!@#$%^&*()]{16,}$', myseed.strip()) is not None #matches the regex pattern
    myturtle = randturtle.generateRandomTurtle(myseed, 1.5, color="255,0,0")
    t.clearscreen()
    assert True == True

def test_randturtle_staticfill():
    myseed = "I1Ov3rUxToNsR4NdTuRtLeS1234$$"
    assert re.match(r'^[0-9a-zA-Z!@#$%^&*()]{16,}$', myseed.strip()) is not None #matches the regex pattern
    myturtle = randturtle.generateRandomTurtle(myseed, 1.5, fill="255,0,0")
    t.clearscreen()
    assert True == True

def test_randturtle_staticcolorfill():
    myseed = "I1Ov3rUxToNsR4NdTuRtLeS1234$$"
    assert re.match(r'^[0-9a-zA-Z!@#$%^&*()]{16,}$', myseed.strip()) is not None #matches the regex pattern
    myturtle = randturtle.generateRandomTurtle(myseed, 1.5, "255,0,0", "255,0,0")
    t.clearscreen()
    assert True == True

def test_randturtle_setiter():
    myseed = "I1Ov3rUxToNsR4NdTuRtLeS1234$$"
    assert re.match(r'^[0-9a-zA-Z!@#$%^&*()]{16,}$', myseed.strip()) is not None #matches the regex pattern
    for n in range(0, 3):
        myturtle = randturtle.generateRandomTurtle(myseed, 0.5, iterations=5*n)
        t.clearscreen()
    assert True == True