################################################
# Title     : Draw and Play with Turtle
# Author    : balarcode
# Version   : 1.1
# Date      : 8th October 2024
# File Type : Python Script / Program
# File Test : Verified on Python 3.12.6
# Comments  : The program contains few methods to draw and play with the Python Turtle library.
#             Refer to Turtle documentation here: https://docs.python.org/3/library/turtle.html.
#             You might have to build Python with tcl-tk GUI options to run the code. Steps to 
#             install Python interface to Tcl-Tk GUI toolkit on Mac OS (Apple Silicon) has been
#             included in README.md file.
#
# All Rights Reserved.
################################################

import turtle
import time

turtle.Screen()
turtle.title("Welcome to Turtle Draw and Play!")

################################################
# Draw a pentagon
################################################
turtle.title("Welcome to Turtle Draw and Play! - Drawing a pentagon")
bob = turtle.Turtle()
angle = 72
distance = 100
for _ in range(5):
    bob.forward(distance)
    bob.left(angle)

time.sleep(2)
turtle.clearscreen()

################################################
# Draw a hexagon slowly to watch the animation
################################################
turtle.title("Welcome to Turtle Draw and Play! - Drawing a hexagon slowly for an animation")
jazz = turtle.Turtle()
jazz.color("red")
jazz.speed(1)
angle = 60
distance = 100
for _ in range(12):
    jazz.forward(distance)
    jazz.left(angle)

time.sleep(2)
turtle.clearscreen()

################################################
# Draw a hexagon with Turtle shape stamped on the screen
################################################
turtle.title("Welcome to Turtle Draw and Play! - Drawing a hexagon with turtle shape stamped on the screen")
bluey = turtle.Turtle()
bluey.shape("turtle")
bluey.color("blue")
bluey.speed(2)
bluey.stamp()
angle = 60
distance = 100
for _ in range(12):
    bluey.forward(distance)
    bluey.stamp()
    bluey.left(angle)

time.sleep(2)
turtle.clearscreen()

################################################
# Draw a circle of Turtle shapes
################################################
turtle.title("Welcome to Turtle Draw and Play! - Drawing a circle of turtle shapes")
tom = turtle.Turtle()
tom.shape("turtle")
tom.color("green")
tom.speed(2)
tom.penup()
angle = 36
distance = 100
for size in range(10):
    tom.forward(distance)
    tom.stamp()
    tom.forward(-distance)
    tom.right(angle)

time.sleep(2)
turtle.clearscreen()

################################################
# Draw an outward spiral of Turtle shapes
################################################
turtle.title("Welcome to Turtle Draw and Play! - Drawing an outward spiral of turtle shapes")
spiral = turtle.Turtle()
spiral.color("orange")
spiral.shape("turtle")
spiral.speed(2)
spiral.up()
angle = 24
distance = 5
for _ in range(30):
    spiral.stamp()
    spiral.forward(distance)
    spiral.right(angle)
    distance += 2

time.sleep(2)
turtle.clearscreen()

################################################
# Exit the program
################################################
turtle.title("Click on the screen to exit. Thank you!")
turtle.exitonclick()
