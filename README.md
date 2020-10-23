# Dactinote - Deep Q Learning for robot control

This project proposes a general solution for training robot control systems using neural networks.

## Basic Concept

Robot hardware is, frankly, not suited for the learning part of ML, which makes employing learning based solutions a bit more difficult.
Many people train their control software in game engines / physics simulations before deploying it to their robot.
Some people probably train their robots by connecting them to external servers with proper processing power.

I wish to make framework available that allows me to train control software on an external machine, while the robot is running.
That way, I hope to allow rapid training of prototype control software.

## Test Project

I have a prototype setup with a servo and a movable target.
I want the robot to be pointing it's servo towards the target at all time.

For starters, I'll be using MJPEG and JSON to communicate the robot's current state, given by a camera and the servo itself.

From that, I'll be constructing a loss function that determines how 'off' the heading of the servo is.

