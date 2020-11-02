import Settings as s
from tts import TTS
import socket
import select
import threading
from Realsense import Realsense
from Joint import joint
import time
import math
import random
from GUI2 import WellDonePage, ExcellentPage, VeryGoodPage
import Excel


class Camera(threading.Thread):

    def __init__(self):
        threading.Thread.__init__(self)
        # Create socket for client-server communication
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.server_address = ('localhost', 8888)
        self.sock.bind(self.server_address)
        print ("CAMERA: init")

    # Start camera skeleton tracking application
    def playRealsense(self):
        rStart = Realsense()
        rStart.start()

    # Stop camera skeleton tracking application
    def stopRealsense(self):
        rStop = Realsense()
        rStop.stop()

    # Client - read messages
    def get_skeleton_data(self):
        '''
        The function takes the received data and return a list of joints.
        Using the defined socket to recieve skeleton data messages from the cpp code (Cubemos SDK sampels)
        The message structure is : {joint_id,x,y,z/joint_id,x,y,z/...} 1,-0.01,-0.22,1.10/2,0.16,-0.25,1.18/
        '''

        self.sock.settimeout(1.0) #to check
        try:
            data, address = self.sock.recvfrom(4096)
            self.sock.settimeout(None) #to check
            data = data.split('/')
            data.pop() # remove the last item in the list (which is empty because the split is by '/')
            jointsStr = []
            for i in data:
                joint = i.split(',')
                jointsStr.append(joint)
            # now change to float values
            joints = []  # joints data
            for j in jointsStr:
                joints.append(self.create_joint(j))
            return joints
        except socket.timeout:  # fail after 1 second of no activity
            print("CAMERA: Didn't receive data! [Timeout]")

    def create_joint(self, jointList):
        '''
        :param jointList: joint data as a string
        :return: Joint object or False if there is no data for creating Joint
        The y values of the joints are upside-down (as received from app), therefore is multiple by -1
        '''
        try:
            if (float(jointList[1]) == 0 or float(jointList[2])==0 or float(jointList[3])==0):
                print("CAMERA: could not create new joint: All coordinates are 0")
                return False
            else:
                new_joint = joint(jointList[0], float(jointList[1]) , float(jointList[2])*-1, float(jointList[3]))
                return new_joint
        except:
            print("CAMERA: could not create new joint: list index out of range")
            return False

    # input - , required joint number ; output -
    def find_joint_data(self, jointsList, jointNumber):
        '''
        :param jointsList: List of all joints which is not None!
        :param jointNumber: The number of the required joint
        :return: The required joint only or False if the joint not exist in the recieved message data
        '''
        for i in jointsList:
            if i is False:
                return False
            else:
                if i.type == jointNumber:
                    return i
        return False

    # Calculate distance between two joints
    def calc_dist(self, joint1, joint2):
        distance = math.hypot(joint1.x - joint2.x, joint1.y - joint2.y)
        return distance

    # Calculate angle between joints according to the law of cosines
    def calc_angle(self, joint1, joint2, joint3):
        '''
        :param joint1: Point C
        :param joint2: Point B
        :param joint3: Point A
        :return: ACB angle in degrees
        '''
        a = self.calc_dist(joint1, joint2)
        b = self.calc_dist(joint1, joint3)
        c = self.calc_dist(joint2, joint3)
        try:
            rad_angle = math.acos((a ** 2 + b ** 2 - c ** 2) / (2 * a * b))
            deg_angle = (rad_angle * 180) / math.pi
            return round(deg_angle, 2)
        except:
            print("CAMERA: could not calculate the angle")

    # ----------------------------- Exercise Recognition ---------------------------------
    '''
    Each exercise have a function with it's name - to recognize the user movements and the success in the exercise
    There are more general functions depending the nuber of the required joints for the exercise - these functions gets 
    the number of the required joints:
    1 - Spine                   
    2 - Right shoulder          8 - Right thigh
    3 - Right elbow             9 - Right knee
    4 - Right hand              10 - Right foot
    5 - Left shoulder           11 - Left thigh
    6 - Left elbow              12 - Left knee
    7 - Left hand               13 - Left foot

    '''

    def exercise_three_joints(self, joint_num1, joint_num2, joint_num3, up_ub, up_lb, down_ub, down_lb):
        '''
        Recognize 3 joint exercise
        :param joint_num1: Number of first required joint as string (Example: '1')
        :param joint_num2: Number of second required joint as string
        :param joint_num3: Number of third required joint as string
        :param up_ub: Upper bound of the angle for 'up' condition
        :param up_lb: Lower bound of the angle for 'up' condition
        :param down_ub: Upper bound of the angle for 'down condition
        :param down_lb: Lower bound of the angle for 'down' condition
        :return:
        '''

        flag = False
        counter = 0
        list_joints_excel = [[joint_num1, joint_num2, joint_num3]]
        # while counter!= 8:
        for i in range(1,400):
            joints = self.get_skeleton_data()
            if joints is not None:
                joint1 = self.find_joint_data(joints, joint_num1)
                joint2 = self.find_joint_data(joints, joint_num2)
                joint3 = self.find_joint_data(joints, joint_num3)
                if not joint1 or not joint2 or not joint3: # Data is not exist for one or more of the required joints
                    continue
                angle = self.calc_angle(joint2,joint1,joint3)
                new_entry = [joint1, joint2, joint3, angle]
                # if (up_lb < angle < up_ub) & (not flag):
                #     counter += 1
                #     print ("number %s" % counter)
                #     flag = True
                #     new_entry = [joint1, joint2, joint3, angle, 'up']
                # if (down_lb < angle < down_ub) & flag:
                #     flag = False
                #     new_entry = [joint1, joint2, joint3, angle, 'down']
                list_joints_excel.append(new_entry)
        return list_joints_excel



if __name__ == '__main__':
    rStart = Realsense()
    rStart.start()
    c = Camera()
    Excel.create_workbook()
    joints = c.exercise_three_joints('4','2','8',105,75,20,10)
    rStart.stop()
    s.worksheet = s.excel_workbook.add_worksheet("1")
    frame_number = 1

    for l in range(1, len(joints)):
        row = 1
        s.worksheet.write(0, frame_number, frame_number)
        for j in joints[l]:
            if type(j) == joint:
                j_ar = j.joint_to_array()
                for i in range(len(j_ar)):
                    s.worksheet.write(row, frame_number, str(j_ar[i]))
                    row += 1
            else:
                s.worksheet.write(row, frame_number, j)
                row += 1
        frame_number += 1

    s.worksheet = s.excel_workbook.add_worksheet("2")
    row = 0
    frame_number = 0
    for l in range(1, len(joints)):
        for j in joints[l]:
            if type(j) == joint:
                j_ar = j.joint_to_array()
                s.worksheet.write(row, 0, frame_number)
                for i in range(len(j_ar)):
                    s.worksheet.write(row, i + 1, str(j_ar[i]))
                row += 1
            else:
                s.worksheet.write(row-1, i + 2,j)
        frame_number += 1

    s.excel_workbook.close()
