# class represent skeleton joint

class joint(object):

    def __init__(self, type, x, y, z):
        self.type = type
        self.x = x
        self.y = y
        self.z = z

    def __str__(self):
        return self.type+" "+str(self.x)+" "+str(self.y)+" "+str(self.z)

    def joint_to_array(self):
        arr = [self.type, self.x, self.y, self.z]
        return arr