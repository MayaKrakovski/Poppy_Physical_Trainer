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
        print ("camera init")

    # Start camera application
    def playRealsense(self):
        rStart = Realsense()
        rStart.start()

    # Stop camera application
    def stopRealsense(self):
        rStop = Realsense()
        rStop.stop()
        # clear received data
        while self.getSkeletonData() is not None:
            continue

    # Client - read messages
    def getSkeletonData(self):
        self.sock.settimeout(1.0) #to check
        try:
            data, address = self.sock.recvfrom(4096)
            self.sock.settimeout(None) #to check
            data = data.split('/')
            jointsStr = []
            for i in data:
                joint = i.split(',')
                jointsStr.append(joint)
            # now change to float values
            joints = [] #joints data
            for j in jointsStr:
                joints.append(self.createJoint(j))
            return joints
        except socket.timeout:  # fail after 1 second of no activity
            print("Didn't receive data! [Timeout]")
            # TODO Maybe add a meesage to the user that the camera don't recieve data?
            return None

    # input - joint data list ; output - joint object
    def createJoint(self, jointList):
        try:
            new_joint = joint (jointList[0], float(jointList[1]) , float(jointList[2]), float(jointList[3]))
            return new_joint
        except:
            print("could not create new joint: list index out of range")
            # TODO Maybe add a meesage to the user that the camera don't recognize joint?
            return None

    # input - all joints data, required joint number ; output - data of the required joint only
    def findJointData(self, jointsList, jointNumber):
        flag = False #did the joint number exist
        jointData = []
        if jointsList!=None:
            for i in jointsList:
                if  i!=None and i.type == jointNumber:
                    jointData.append(i)
                    flag = True
        if flag:
            return jointData
        else:
            return False

    # input - 2 joints lists; output - T if y(a)>y(b)
    def compareYbetweenJoints(self, jointA, jointB):
        for i in jointA:
            for j in jointB:
                if (i.y>j.y):
                    return True
        return False

    # Calculate angle between joints
    def calc_angle(self, joint1, joint2, joint3):
        a = self.calc_dist(joint1, joint2)
        b = self.calc_dist(joint1, joint3)
        c = self.calc_dist(joint2, joint3)
        try:
            rad_angle = math.acos((a ** 2 + b ** 2 - c ** 2) / (2 * a * b))
            deg_angle = (rad_angle * 180) / math.pi
            return round(deg_angle, 2)
        except:
            print("could not calculate the angle")

    # Calculate distance between joints
    def calc_dist(self, joint1, joint2):
        distance = math.hypot(joint1.x - joint2.x,
                              joint1.y - joint2.y)
        return distance

    def run_exercise(self):
        self.playRealsense()
        getattr(self, s.req_exercise)() # running the method of the requested exercise
        self.stopRealsense()
        if (s.success_exercise):
            time.sleep(1)
            s.str_to_say = self.random_encouragement()

    def random_encouragement(self):
        rand = random.random()
        if rand < 0.33:
            s.screen.switch_frame(WellDonePage)
            return "well done"
        elif rand < 0.67:
            s.screen.switch_frame(VeryGoodPage)
            return "very Good"
        else:
            s.screen.switch_frame(ExcellentPage)
            return "excellent"

    ####### Exercises #######

    def hello_waving(self): # check if the participant waved
        while (s.req_exercise == "hello_waving"):
            joints = self.getSkeletonData()
            JOINT_RIGHT_SHOULDER = self.findJointData(joints, "12")
            JOINT_RIGHT_HAND = self.findJointData(joints, "15")
            if (not JOINT_RIGHT_SHOULDER or not JOINT_RIGHT_HAND):
                continue
            if (self.compareYbetweenJoints(JOINT_RIGHT_HAND, JOINT_RIGHT_SHOULDER)):
                s.waved = True
                s.req_exercise = ""
                return True

    def exercise_three_joints(self, exercise_name, joint_num1, joint_num2, joint_num3,up_lb,
                            up_ub, down_lb, down_ub): #TODO add depth check
        flag = False
        counter = 0
        list_joints = [[joint_num1, joint_num2, joint_num3]]
        while (s.req_exercise == exercise_name):
            joints = self.getSkeletonData()
            ''' TODO the if condition of not joint1 or not joint2 or not joint3 can be change to the length of joints
            or sending a messeage to the user that one of the joints was not recognize'''
            joint1 = self.findJointData(joints, joint_num1)
            joint2 = self.findJointData(joints, joint_num2)
            joint3 = self.findJointData(joints, joint_num3)
            if not joint1 or not joint2 or not joint3:
                continue
            for i in range(0, len(joint1)):
                angle = self.calc_angle(joint2[i], joint3[i], joint1[i])
                new_entry = [joint1[i], joint2[i], joint3[i], angle]
                print (angle)
                if ((up_lb<angle<up_ub) & (not flag)):
                    print("up")
                    counter = self.counting_flag(counter)
                    flag = True
                    new_entry.append("up")
                if ((down_lb<angle<down_ub) & (flag)):
                    print("down")
                    flag = False
                    print (counter)
                    new_entry.append("down")
                if (counter == s.rep):
                    s.req_exercise = ""
                    s.success_exercise = True
                    break
                list_joints.append(new_entry)
        print ("finish with" + str(counter))
        print(list_joints)
        Excel.wf_joints(exercise_name,list_joints)
        s.ex_list.append([exercise_name, counter])
        if (s.success_exercise):
            return True

    def exercise_six_joints(self, exercise_name, joint_r1, joint_r2, joint_r3, joint_l1, joint_l2, joint_l3, up_lb,
                            up_ub, down_lb, down_ub): #TODO add depth check
        flag = False
        counter = 0
        list_joints = [[joint_r1, joint_r2, joint_r3, joint_l1, joint_l2, joint_l3]]
        while (s.req_exercise == exercise_name):
            joints = self.getSkeletonData()
            jointr1 = self.findJointData(joints, joint_r1)
            jointr2 = self.findJointData(joints, joint_r2)
            jointr3 = self.findJointData(joints, joint_r3)
            jointl1 = self.findJointData(joints, joint_l1)
            jointl2 = self.findJointData(joints, joint_l2)
            jointl3 = self.findJointData(joints, joint_l3)
            if not jointr1 or not jointr2 or not jointr3 or not jointl1 or not jointl2 or not jointl3:
                continue
            for i in range(0, len(jointr1)):
                right_angle = self.calc_angle(jointr2[i], jointr3[i], jointr1[i])
                left_angle = self.calc_angle(jointl2[i], jointl3[i], jointl1[i])
                new_entry = [jointr1[i], jointr2[i], jointr3[i],jointl1[i], jointl2[i], jointl3[i], right_angle,
                             left_angle]
                print (right_angle)
                print (left_angle)
                if ((up_lb<right_angle<up_ub) & (up_lb<left_angle<up_ub) & (not flag)):
                    print("up")
                    counter = self.counting_flag(counter)
                    flag = True
                    new_entry.append("up")
                if ((down_lb<right_angle<down_ub) & (down_lb<left_angle<down_ub) & (flag)):
                    print("down")
                    flag = False
                    new_entry.append("down")
                    print (counter)
                if (counter == s.rep):
                    s.req_exercise = ""
                    s.success_exercise = True
                    break
                list_joints.append(new_entry)
        print ("finish with" + str(counter))
        Excel.wf_joints(exercise_name,list_joints)
        s.ex_list.append([exercise_name, counter])
        if (s.success_exercise):
            return True

    def raise_arms_horizontally_separate(self):
        while (s.req_exercise == "raise_arms_horizontally_separate"):
            continue

    def raise_right_arm_horiz(self):
        self.exercise_three_joints("raise_right_arm_horiz", "3", "12", "15",  90, 120, 30, 50)

    def raise_left_arm_horiz(self):
        self.exercise_three_joints("raise_left_arm_horiz", "3", "6", "9", 90, 120, 30, 50)

    def raise_arms_horizontally(self):
        self.exercise_six_joints("raise_arms_horizontally","3", "12", "15", "3", "6", "9", 90, 120, 30, 50)

    def raise_arms_horiz_turn(self):
        up_time_counter = 0
        count = 0
        list_joints = [[3,12,13,6,7]]
        while (s.req_exercise == "raise_arms_horiz_turn"):
            last_time = time.time()
            joints = self.getSkeletonData()
            jointr1 = self.findJointData(joints, "12")
            jointr2 = self.findJointData(joints, "13")
            jointl1 = self.findJointData(joints, "6")
            jointl2 = self.findJointData(joints, "7")
            joint_torso = self.findJointData(joints, "3")
            if not joint_torso or not jointr1 or not jointr2 or not jointl1 or not jointl2:
                continue
            for i in range(0, len(jointr1)):
                right_angle = self.calc_angle(jointr1[i], joint_torso[i], jointr2[i])
                left_angle = self.calc_angle(jointl1[i], joint_torso[i], jointl2[i])
                new_entry = [joint_torso[i], jointr1[i], jointr2[i], jointl1[i], jointl2[i], right_angle, left_angle]
                print (right_angle)
                print (left_angle)
                if (90 < right_angle < 130) and (90 < left_angle < 130):
                    up_time_counter = up_time_counter + (time.time() - last_time)
                    if (up_time_counter>count):
                        count = self.counting_flag(count)
                        up_time_counter = up_time_counter - 1
                        new_entry.append(count)
                    print (up_time_counter)
                    last_time = time.time()
                if (up_time_counter >= s.rep):
                    s.req_exercise = ""
                    s.success_exercise = True
                    break
                list_joints.append(new_entry)
        print ("finish with" + str(count))
        print(list_joints)
        Excel.wf_joints("raise_arms_horiz_turn", list_joints)
        s.ex_list.append(["raise_arms_horiz_turn", count])
        if (s.success_exercise):
            return True

    def bend_elbows(self):
        self.exercise_six_joints("bend_elbows", "12", "13", "15", "6", "7", "9", 2, 10, 165, 180)

    def exercise_three_joints_with_height(self, exercise_name, joint_num1, joint_num2, joint_num3,
                            up_height_ub, up_depth_lb, down_depth_ub, down_angle_lb, down_angle_ub):
        flag = False
        counter = 0
        exercise_name = s.req_exercise
        list_joints = [[12, 13, 15]]
        while (s.req_exercise == exercise_name):
            joints = self.getSkeletonData()
            jointr1 = self.findJointData(joints, joint_num1)
            jointr2 = self.findJointData(joints, joint_num2)
            jointr3 = self.findJointData(joints, joint_num3)
            if not jointr1 or not jointr2 or not jointr3:
                continue
            for i in range(0, len(jointr1)):
                height = abs(jointr1[i].y - jointr3[i].y)
                angle = self.calc_angle(jointr2[i], jointr1[i], jointr3[i])
                depth = abs(jointr1[i].z - jointr3[i].z)
                new_entry = [jointr1[i], jointr2[i], jointr3[i], height, angle, depth]
                print (height)
                print (angle)
                print (depth)
                print (flag)
                if (height < up_height_ub) & (depth > up_depth_lb) & (not flag):
                    print ("up")
                    counter = self.counting_flag(counter)
                    flag = True
                    new_entry.append("up")
                if (down_angle_lb < angle < down_angle_ub) & (depth < down_depth_ub) & flag:
                    print ("down")
                    flag = False
                    new_entry.append("down")
                if (counter == s.rep):
                    s.req_exercise = ""
                    s.success_exercise = True
                    break
                list_joints.append(new_entry)
        print ("finish with" + str(counter))
        print(list_joints)
        Excel.wf_joints(exercise_name,list_joints)
        s.ex_list.append([exercise_name, counter])
        if (s.success_exercise):
            return True

    def raise_right_arm_forward(self):
        self.exercise_three_joints_with_height("raise_right_arm_forward", "12", "13", "15", 45, 400, 80, 160, 190)

    def raise_left_arm_forward(self):
        self.exercise_three_joints_with_height("raise_left_arm_forward", "6", "7", "9", 45, 400, 80, 160, 190)

    def raise_arms_forward_separate(self):
        while (s.req_exercise == "raise_arms_forward_separate"):
            continue

    def raise_arms_forward(self):
        self.six_joints_with_height("raise_arms_forward", "12", "13", "15", "6", "7", "9", 45, 400, 160, 180, 80)

    def six_joints_with_height(self, exercise_name, joint_r1, joint_r2, joint_r3, joint_l1, joint_l2, joint_l3,
                               up_height_ub, up_dpeth_lb, down_angle_lb, down_angle_ub, down_dpeth_ub):
        flag = False
        counter = 0
        exercise_name = s.req_exercise
        list_joints = [[joint_r1, joint_r2, joint_r3, joint_l1, joint_l2, joint_l3]]
        while s.req_exercise == exercise_name:
            joints = self.getSkeletonData()
            jointr1 = self.findJointData(joints, "12")
            jointr2 = self.findJointData(joints, "13")
            jointr3 = self.findJointData(joints, "15")
            jointl1 = self.findJointData(joints, "6")
            jointl2 = self.findJointData(joints, "7")
            jointl3 = self.findJointData(joints, "9")
            if not jointr1 or not jointr2 or not jointr3 or not jointl1 or not jointl2 or not jointl3:
                continue
            for i in range(0, len(jointr1)):
                left_height = abs(jointl1[i].y - jointl3[i].y )
                left_angle = self.calc_angle(jointl2[i], jointl1[i], jointl3[i])
                left_depth = abs(jointl1[i].z - jointl3[i].z)
                right_height = abs(jointr1[i].y - jointr3[i].y)
                right_angle = self.calc_angle(jointr2[i], jointr1[i], jointr3[i])
                right_depth = abs(jointr1[i].z - jointr3[i].z)
                new_entry = [jointr1[i], jointr2[i], jointr3[i],jointl1[i], jointl2[i], jointl3[i], right_angle,
                             left_angle, right_height, left_height,right_depth,left_depth]
                print (left_height)
                print (right_height)
                if (left_height < up_height_ub) & (right_height < up_height_ub) & (right_depth > up_dpeth_lb) & \
                        (left_depth > up_dpeth_lb) & (not flag):
                    print ("up")
                    counter = self.counting_flag(counter)
                    flag = True
                    new_entry.append("up")
                if (down_angle_lb < left_angle < down_angle_ub) & (down_angle_lb < right_angle < down_angle_ub) & \
                        (right_depth < down_dpeth_ub) & (left_depth < down_dpeth_ub) & flag:
                    print ("down")
                    flag = False
                    new_entry.append("down")
                if counter == s.rep:
                    s.req_exercise = ""
                    s.success_exercise = True
                    break
                list_joints.append(new_entry)
        print ("finish with" + str(counter))
        print(list_joints)
        Excel.wf_joints(exercise_name, list_joints)
        s.ex_list.append([exercise_name, counter])
        if s.success_exercise:
            return True

    def raise_arms_forward_static(self):
        up_time_counter = 0
        count = 0
        last_time = 0
        exercise_name = s.req_exercise
        list_joints = [[12, 13, 15, 6, 7, 9]]
        while (s.req_exercise == "raise_arms_forward_static") or ( s.req_exercise == "raise_arms_forward_turn" ):
            last_time = time.time()
            joints = self.getSkeletonData()
            jointr1 = self.findJointData(joints, "12")
            jointr2 = self.findJointData(joints, "13")
            jointr3 = self.findJointData(joints, "15")
            jointl1 = self.findJointData(joints, "6")
            jointl2 = self.findJointData(joints, "7")
            jointl3 = self.findJointData(joints, "9")
            if not jointr1 or not jointr2 or not jointr3 or not jointl1 or not jointl2 or not jointl3:
                continue
            for i in range(0, len(jointr1)):
                right_height = abs(jointr1[i].y - jointr3[i].y)
                left_height = abs(jointl1[i].y - jointl3[i].y)
                right_depth = abs(jointr1[i].z - jointr3[i].z)
                left_depth = abs(jointl1[i].z - jointl3[i].z)
                new_entry = [jointr1[i], jointr2[i], jointr3[i],jointl1[i], jointl2[i], jointl3[i], right_height,
                             left_height,right_depth,left_depth]
                if (left_height < 45.0) & (right_height < 45.0) & (right_depth > 400) & (left_depth > 400):
                    up_time_counter = up_time_counter + (time.time() - last_time)
                    if (up_time_counter>count):
                        count = self.counting_flag(count)
                        up_time_counter = up_time_counter - 0.9
                        new_entry.append(count)
                    print (up_time_counter)
                    # last_time = time.time()
                if (up_time_counter >= s.rep-1):
                    s.req_exercise = ""
                    s.success_exercise = True
                    break
                last_time = time.time()
                list_joints.append(new_entry)
        print ("finish with" + str(count))
        print(list_joints)
        Excel.wf_joints(exercise_name,list_joints)
        s.ex_list.append([exercise_name, count])
        if (s.success_exercise):
            return True

    def raise_arms_forward_turn(self):
        self.raise_arms_forward_static()

    def exercise_seven_joints_two_angles(self, exercise_name, joint_torso_num, joint_r1, joint_r2, joint_r3, joint_l1,
                                         joint_l2, joint_l3,
                                         up_angle1_lb, up_angle1_ub, down_angle1_lb, down_angle1_ub,
                                         up_angle2_lb, up_angle2_ub, down_angle2_lb, down_angle2_ub):
        flag = False
        counter = 0
        list_joints = [[joint_torso_num, joint_r1, joint_r2, joint_r3, joint_l1, joint_l2, joint_l3]]
        while (s.req_exercise == exercise_name):
            joints = self.getSkeletonData()
            joint_torso = self.findJointData(joints, joint_torso_num)
            jointr1 = self.findJointData(joints, joint_r1)
            jointr2 = self.findJointData(joints, joint_r2)
            jointr3 = self.findJointData(joints, joint_r3)
            jointl1 = self.findJointData(joints, joint_l1)
            jointl2 = self.findJointData(joints, joint_l2)
            jointl3 = self.findJointData(joints, joint_l3)
            if not joint_torso or not jointr1 or not jointr2 or not jointr3 or not jointl1 or not jointl2 or not jointl3:
                continue
            for i in range(0, len(jointr1)):
                left_armpit_angle = self.calc_angle(jointl1[i], joint_torso[i], jointl2[i])
                left_elbow_angle = self.calc_angle(jointl2[i], jointl1[i], jointl3[i])
                right_armpit_angle = self.calc_angle(jointr1[i], joint_torso[i], jointr2[i])
                right_elbow_angle = self.calc_angle(jointr2[i], jointr1[i], jointr3[i])
                new_entry =[joint_torso[i], jointr1[i], jointr2[i], jointr3[i],jointl1[i], jointl2[i],
                            jointl3[i], right_armpit_angle, left_armpit_angle, right_elbow_angle,
                            left_elbow_angle]
                print (left_armpit_angle)
                print (left_elbow_angle)
                print (right_armpit_angle)
                print (right_elbow_angle)
                if ((up_angle1_lb < left_armpit_angle < up_angle1_ub and
                     up_angle1_lb < right_armpit_angle < up_angle1_ub) and
                    (up_angle2_lb < left_elbow_angle < up_angle2_ub and
                     up_angle2_lb < right_elbow_angle < up_angle2_ub) and (not flag)):
                    print("close")
                    counter = self.counting_flag(counter)
                    flag = True
                    new_entry.append("close")
                if ((down_angle1_lb < left_armpit_angle < down_angle1_ub and
                     down_angle1_lb < right_armpit_angle < down_angle1_ub) and
                        (down_angle2_lb < left_elbow_angle < down_angle2_ub and
                         down_angle2_lb < right_elbow_angle < down_angle2_ub) and flag):
                    print("open")
                    flag = False
                    new_entry.append("open")
                    print (counter)
                if (counter == s.rep):
                    s.req_exercise = ""
                    s.success_exercise = True
                    break
                list_joints.append(new_entry)
        print ("finish with" + str(counter))
        print(list_joints)
        Excel.wf_joints(exercise_name, list_joints)
        s.ex_list.append([exercise_name, counter])
        if (s.success_exercise):
            return True

    def raise_arms_bend_elbows(self):
        self.exercise_seven_joints_two_angles("raise_arms_bend_elbows", "3", "12", "13", "15", "6", "7", "9",
                                              90, 120, 90, 120, 0, 20, 140, 180)
    def raise_arms_90_and_up(self):
        self.exercise_seven_joints_two_angles("raise_arms_90_and_up", "3", "12", "13", "15", "6", "7", "9",
                                              120, 180, 90, 130, 80, 120, 60, 100)

    def open_hands_and_raise_up(self):
        self.exercise_six_joints("open_hands_and_raise_up", "3", "12", "13", "3", "6", "7", 160, 180, 100, 120)

    def open_arms_and_forward(self):
        flag = False
        counter = 0
        list_joints = [[3, 12, 13, 15, 6, 7, 9]]
        while s.req_exercise == "open_arms_and_forward":
            joints = self.getSkeletonData()
            joint_torso = self.findJointData(joints, "3")
            jointr1 = self.findJointData(joints, "12")
            jointr2 = self.findJointData(joints, "13")
            jointr3 = self.findJointData(joints, "15")
            jointl1 = self.findJointData(joints, "6")
            jointl2 = self.findJointData(joints, "7")
            jointl3 = self.findJointData(joints, "9")
            if not joint_torso or not jointr1 or not jointr2 or not jointr3 or not jointl1 or not jointl2 or \
                    not jointl3:
                continue
            for i in range(0, len(jointr1)):
                left_height = abs(jointl1[i].y - jointl3[i].y)
                left_angle = self.calc_angle(jointl1[i], joint_torso[i], jointl2[i])
                left_depth = abs(jointl1[i].z-jointl3[i].z)
                right_height = abs(jointr1[i].y - jointr3[i].y)
                right_angle = self.calc_angle(jointr1[i], joint_torso[i], jointr2[i])
                right_depth = abs(jointr1[i].z - jointr3[i].z)
                new_entry = [joint_torso[i], jointr1[i], jointr2[i], jointr3[i],jointl1[i], jointl2[i], jointl3[i],
                             right_height, left_height, right_angle, left_angle, right_depth, left_depth]
                print (left_depth)
                print (right_depth)
                print (left_height)
                print (left_angle)
                print (right_height)
                print (right_angle)
                if (left_height < 45) & (right_height < 45) & (right_depth>400) & (left_depth>400) & (not flag):
                    print ("close")
                    counter = self.counting_flag(counter)
                    new_entry.append("close")
                    flag = True
                if (90 < left_angle < 120) & (90 < right_angle < 120) & (right_depth < 70) & (left_depth < 70) & flag:
                    print ("open")
                    new_entry.append("open")
                    flag = False
                if (counter == s.rep):
                    s.req_exercise = ""
                    s.success_exercise = True
                    break
                list_joints.append(new_entry)
        print ("finish with" + str(counter))
        Excel.wf_joints("open_arms_and_forward", list_joints)
        s.ex_list.append(["open_arms_and_forward", counter])
        if (s.success_exercise):
            return True

    def open_and_close_arms_90(self):
        flag = False
        counter = 0
        list_joints = [[3, 12, 13, 15, 6, 7, 9]]
        while (s.req_exercise == "open_and_close_arms_90"):
            joints = self.getSkeletonData()
            joint_torso = self.findJointData(joints, "3")
            jointr1 = self.findJointData(joints, "12")
            jointr2 = self.findJointData(joints, "13")
            jointr3 = self.findJointData(joints, "15")
            jointl1 = self.findJointData(joints, "6")
            jointl2 = self.findJointData(joints, "7")
            jointl3 = self.findJointData(joints, "9")
            if not joint_torso or not jointr1 or not jointr2 or not jointr3 or not jointl1 or not jointl2 or not jointl3:
                continue
            for i in range(0, len(jointr1)):
                left_armpit_angle = self.calc_angle(jointl1[i], joint_torso[i], jointl2[i])
                left_elbow_angle = self.calc_angle(jointl2[i], jointl1[i], jointl3[i])
                right_armpit_angle = self.calc_angle(jointr1[i], joint_torso[i], jointr2[i])
                right_elbow_angle = self.calc_angle(jointr2[i], jointr1[i], jointr3[i])
                left_height = abs(jointl1[i].y - jointl2[i].y)
                left_depth = abs(jointl1[i].z - jointl2[i].z)
                right_height = abs(jointr1[i].y - jointr2[i].y)
                right_depth = abs(jointr1[i].z - jointr2[i].z)
                new_entry = [joint_torso[i], jointr1[i], jointr2[i], jointr3[i],jointl1[i], jointl2[i], jointl3[i],
                             right_armpit_angle, left_armpit_angle,right_elbow_angle, left_elbow_angle,
                             right_height, left_height, right_depth, left_depth]
                print (left_armpit_angle)
                print (left_elbow_angle)
                print (right_armpit_angle)
                print (right_elbow_angle)
                print (left_height)
                print (left_depth)
                print (right_height)
                print (right_depth)
                if (left_height < 100) & (right_height < 100) & (right_depth>180) & (left_depth>180) & (not flag):
                    print("close")
                    counter = self.counting_flag(counter)
                    new_entry.append("close")
                    flag = True
                if ((90 < left_armpit_angle < 130 and 90 < right_armpit_angle < 130) and
                        (60 < left_elbow_angle < 100 and 60 < right_elbow_angle <100) and
                        (right_depth<40) and (left_depth<40) and (flag)):
                    print("open")
                    new_entry.append("open")
                    flag = False
                    print (counter)
                if (counter == s.rep):
                    s.req_exercise = ""
                    s.success_exercise = True
                    break
                list_joints.append(new_entry)
        print ("finish with" + str(counter))
        Excel.wf_joints("open_and_close_arms_90", list_joints)
        s.ex_list.append(["open_and_close_arms_90", counter])
        if (s.success_exercise):
            return True






    def raise_arms_and_lean(self): #todo fill
        while (s.req_exercise == "raise_arms_and_lean"):
            continue

    def raise_left_arm_and_lean(self):
        up_time_counter = 0
        while (s.req_exercise == "raise_left_arm_and_lean"):
            last_time = time.time()
            joints = self.getSkeletonData()
            jointl1 = self.findJointData(joints, "6")
            jointl2 = self.findJointData(joints, "7")
            jointl3 = self.findJointData(joints, "9")
            if not jointl1 or not jointl2 or not jointl3:
                continue
            for i in range(0, len(jointl1)):
                right_height = abs(jointl1[i].y - jointl3[i].y)
                print (right_height)
                if (right_height > 300):
                    up_time_counter = up_time_counter + (time.time() - last_time)
                    print (time.time())
                    print (last_time)
                    print (up_time_counter)
                    last_time = time.time()
                if (up_time_counter >= s.rep):
                    s.req_exercise = ""
                    s.success_exercise = True
                    print ("finish with " + str(up_time_counter))
                    return True
                last_time = time.time()

    def raise_right_arm_and_lean(self):
        up_time_counter = 0
        while (s.req_exercise == "raise_right_arm_and_lean"):
            last_time = time.time()
            joints = self.getSkeletonData()
            jointr1 = self.findJointData(joints, "12")
            jointr2 = self.findJointData(joints, "13")
            jointr3 = self.findJointData(joints, "15")
            if not jointr1 or not jointr2 or not jointr3:
                continue
            for i in range(0, len(jointr1)):
                right_height = abs(jointr1[i].y - jointr3[i].y)
                print (right_height)
                if (right_height > 300):
                    up_time_counter = up_time_counter + (time.time() - last_time)
                    print (time.time())
                    print (last_time)
                    print (up_time_counter)
                    last_time = time.time()
                if (up_time_counter >= s.rep):
                    s.req_exercise = ""
                    s.success_exercise = True
                    print ("finish with " + str(up_time_counter))
                    return True
                last_time = time.time()

    # def raise_hands_and_fold_backward(self): #todo fill




    def counting_flag(self, counter):
        counter = counter + 1
        s.str_to_say=str(counter)
        # if counter == 1:
        #     numberstr= "OnePage"
        # s.screen.switch_frame(numberstr)
        print ("number %s" % (counter))
        return (counter)

    def run(self):
        print ("camera start")
        while (not s.finish_workout):
            if (s.req_exercise != ""):
                print ("camera starting: " + str(s.req_exercise))
                self.run_exercise()
        print ("camera done")



            # while (s.waved == False):
            #     print("waiting")
            #     s.waved = s.camera.wave()
            # s.camera.raise_right_arm_horiz()



#for tests
if __name__ == '__main__':
    s.rep = 2
    language = 'Hebrew'
    gender = 'Male'
    s.audio_path = 'audio files/' + language + '/' + gender + '/'
    s.tts = TTS()
    s.waved = False
    s.finish_workout = False
    s.success_exercise = False
    s.req_exercise = "open_arms_and_forward"
    Excel.create_workbook()
    s.camera = Camera()
    s.camera.start()