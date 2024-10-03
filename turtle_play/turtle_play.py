################################################
# Title     : Draw and Play with Turtle
# Author    : balarcode
# Version   : 1.0
# Date      : 3rd October 2024
# File Type : Python Script / Program
# File Test : Verified on Python 3.12.6
# Comments  : The program contains few methods to draw and play with the Python Turtle library.
#             Refer to Turtle documentation here: https://docs.python.org/3/library/turtle.html.
#             You might have to build Python with tcl-tk GUI options to run the code.
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
# Draw a Turtle with its shape stamped on the screen
################################################
turtle.title("Welcome to Turtle Draw and Play! - Drawing a turtle with turtle shape stamped on the screen")
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
# Exit the program
################################################
turtle.title("Click on the screen to exit. Thank you!")
turtle.exitonclick()
