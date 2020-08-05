#!/usr/bin/env python
import rospy
from std_msgs.msg import UInt16
from geometry_msgs.msg import Twist


class Control:
    def __init__(self):
        rospy.init_node("control", anonymous=True)
        self.servo_pub = rospy.Publisher('/servo', UInt16, queue_size=10)
        self.serv = UInt16()
        self.mani_state = UInt16()
        self.ar_marker = -1
        self.call = -1
        self.home = -1
        self.frame_mode = "Ready to Raise up" #before raise up
        self.mani_mode = "Ready to Pick up box" 
        

    def main(self):
        print("Starting,,,")
        while True:
            # 1. Program starting trigger subscribe
            self.starting_trigger()
            if self.frame_mode == "Raise up": #When recieve the control msg: 1 by sender.py 
		        #Raise up the frame
                self.PickUp()
                print(self.frame_mode)
                self.servo_pub.publish(self.serv)
                self.frame_mode = "Ready to Put down"
                
            elif self.frame_mode == "Put down": #When recieve the control msg: 2 by sender.py 
                #Put down the frame
                self.PickDown()
                print(self.frame_mode)
                self.servo_pub.publish(self.serv)
                self.frame_mode = "Ready to Raise up"
                
            elif self.mani_mode == "Release small box":
                self.mani_mode = "Ready to Pick up box"
                #release small box count
                
            elif self.mani_mode == "Pick up large box":
                self.mani_mode = "Ready to Release large box"
                
            elif self.mani_mode == "Release large box":
                self.mani_mode = "Ready to Pick up box"
                    
    def starting_trigger(self):
        rospy.Subscriber("/control_frame", UInt16, self.StartingCallback)
        rospy.Subscriber("/Mani_state", UInt16, self.ManiCallback)
        rospy.Subscriber("/call", UInt16, self.CallCallback)        
        rospy.Subscriber("/home", UInt16, self.HomeCallback)
        
       
    def StartingCallback(self, data):
        if self.mani_mode == "Pick up large box" and data.data == 1:
            self.frame_mode = "Raise up"
            print("setting mode Raise up")
        elif self.mani_mode == "Release large box" and data.data == 2 and self.home == 1:
            self.frame_mode = "Put down"
            self.home = -1
            print("setting mode Put down")

            
    def ManiCallback(self, data):
        if self.mani_mode == "Ready to Pick up box" and self.ar_marker == 1 and data.data == 1:
           self.mani_mode = "Release small box"
           print("Setting mode Release small box")
           
        elif self.mani_mode == "Ready to Pick up box" and self.ar_marker == 2 and data.data == 0:
            self.mani_mode = "Pick up large box" 
            print("Setting Pick up large box")
            
        elif self.mani_mode == "Ready to Release large box" and self.ar_marker == 2 and data.data == 1 and self.call == 1:
            self.mani_mode = "Release large box"
            self.call = -1
            print("Setting mode Release large box")

    def CallCallback(self, data):
        self.call = data.data  
        
    def HomeCallback(self, data):
        self.home = data.data 
        
    def Delay(self, data):
        self.rate = rospy.Rate(data)
        self.rate.sleep()

    def PickUp(self):
        self.Delay(3)
        self.serv.data = 2000
        self.Delay(3)

    def PickDown(self):
        self.Delay(3)
        self.serv.data = 0
        self.Delay(3)
        


Turtle = Control()

if __name__ == "__main__":
    Turtle.main()
