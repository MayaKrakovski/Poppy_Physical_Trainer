from pypot.creatures import PoppyTorso
import time

def raise_arms_bend_elbows_90():
    for i in range(1):
        poppy.r_shoulder_x.goto_position(-90, 1, wait=False)
        poppy.l_shoulder_x.goto_position(90, 1, wait=False)
        poppy.r_elbow_y.goto_position(90, 1.5, wait=False)
        poppy.l_elbow_y.goto_position(90, 1.5, wait=True)
        poppy.r_elbow_y.goto_position(0, 1, wait=False)
        poppy.l_elbow_y.goto_position(0, 1, wait=True)

if __name__ == '__main__':
    poppy = PoppyTorso(simulator='vrep')  # for simulator
    print("init robot")
    for m in poppy.motors:  # motors need to be initialized, False=stiff, True=loose
        m.compliant = False
    for m in poppy.motors:
        if not m.name == 'r_elbow_y' and not m.name == 'l_elbow_y' and not m.name == 'head_y':
            m.goto_position(0, 1, wait=True)
    poppy.head_y.goto_position(-20, 1, wait=True)
    poppy.r_shoulder_x.goto_position(-10, 1, wait=True)
    poppy.l_shoulder_x.goto_position(10, 1, wait=True)
    poppy.r_elbow_y.goto_position(90, 1, wait=True)
    poppy.l_elbow_y.goto_position(90, 1, wait=True)
    print("finish init")
    time.sleep(1)
    raise_arms_bend_elbows_90()