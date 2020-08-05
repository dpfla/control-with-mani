#!/usr/bin/env python
import rospy
from std_msgs.msg import UInt16
from geometry_msgs.msg import Twist


class Sender:
    def __init__(self):
        rospy.init_node("sender_mani", anonymous=True)
        self.sender_pub = rospy.Publisher('/Mani_state', UInt16, queue_size=10)
        self.send = UInt16()

    def main(self):
        while True:
            self.send.data = input("send the message 1 or 2:")
            self.sender_pub.publish(self.send)

Turtle = Sender()

if __name__ == "__main__":
    Turtle.main()
