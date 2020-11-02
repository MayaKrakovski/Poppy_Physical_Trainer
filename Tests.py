# -*- coding: utf-8 -*-
import winsound
import time
import random
import copy
import Tkinter
from poppy_torso import PoppyTorso
from PIL import Image

if __name__ == "__main__":
    poppy = PoppyTorso()

    for m in poppy.motors:  # motors need to be initialized, False=stiff, True=loose
        m.compliant = False
    for m in poppy.motors:
        if not m.name == 'r_elbow_y' and not m.name == 'l_elbow_y':
            m.goto_position(0, 1, wait=True)
        else:
            m.goto_position(90, 1, wait=True)

    poppy.l_elbow_y.goto_position(0, 3, wait=False)
    poppy.r_elbow_y.goto_position(0, 3, wait=True)
    poppy.r_shoulder_x.goto_position(0, 3, wait=True)
    time.sleep(10)
    print("finish")

