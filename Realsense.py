import sys, os, time
import threading


class Realsense (threading.Thread) :

    def __init__(self):
        threading.Thread.__init__(self)
    def run(self):
        #Need to change for Nuitrack!
        # os.system("C:\\Users\\mayak\\Cubemos-Samples\\build\\cpp\\realsense\\Debug\\cpp-realsense.exe") # for Maya's computer
        os.system("C:\\Users\\Administrator\\Desktop\\NuitrackSDK\\Examples\\nuitrack_console_sample\\out\\build\\x64-Debug\\nuitrack_console_sample.exe")
        # os.system("C:\\cpp-realsense.exe")
    def stop(self):
        #Need to change for Nuitrack!
        os.system("taskkill /f /im  nuitrack_console_sample.exe")
        # os.system("taskkill /f /im  cpp-realsense.exe")

if __name__ == '__main__':
    r = Realsense()
    r.run()
