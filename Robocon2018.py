import numpy as np
import matplotlib.pyplot as plt


class Field:
    def __init__(self, color, p1, p2, p3, RobotRadius):
        self.xsize = 500  # Array size x
        self.ysize = 850  # Array size y
        self.xfencemax = 5000  # mm
        self.yfencemax = 8500  # mm
        self.color = color
        self.p1 = p1
        self.p2 = p2
        self.p3 = p3
        self.RobotRadius = RobotRadius
        self.map = np.zeros((self.xsize, self.ysize))
        self.create_obstacle_map()
        plt.imshow(self.map, cmap="jet")

        plt.show()

    def measure_from_box(self, x, y, boxx, boxy, boxw):  # return R,theta(fromrobot)
        xmin = boxx-boxw/2
        xmax = boxx+boxw/2
        ymin = boxy-boxw/2
        ymax = boxy+boxw/2

        if xmin <= x <= xmax:  # in dx
            if y <= ymin:  # robot is bottom
                return ymin-y, 3*np.pi/2
            elif ymax <= y:  # robot is top
                return y-ymax, np.pi/2
            else:
                return 0, 0

        elif ymin <= y <= ymax:  # in dy
            if x <= xmin:  # robot is left
                return xmin-x, 0
            elif xmax <= x:  # robot is right
                return x-xmax, np.pi

        else:
            if xmax < x:  # robot is right
                if y > ymax:  # robot is right top
                    return np.sqrt((x-xmax)**2+(y-ymax)**2), np.arctan2(ymax-y, xmax-x)
                elif y < ymin:  # robot is right bottom
                    return np.sqrt((x-xmax)**2+(y-ymin)**2), np.arctan2(ymin-y, xmax-x)
            elif x < xmin:  # robot is left
                if y > ymax:  # robot is left top
                    return np.sqrt((x-xmin)**2+(y-ymax)**2), np.arctan2(ymax-y, xmin-x)
                elif y < ymin:  # robot is left bottom
                    return np.sqrt((x-xmin)**2+(y-ymin)**2), np.arctan2(ymin-y, xmin-x)
        return 0, 0

    def measure_near_point(self, x, y):
        Rlist = []
        Rlist.append((x, np.pi))  # fence left
        Rlist.append((self.xfencemax-x, 0))  # fence right
        Rlist.append((y-89, 3*np.pi/2))  # fence bottom
        Rlist.append((self.yfencemax-y, np.pi/2))  # fence top
        Rlist.append(self.measure_from_box(x, y, 2000, 1000, 500))  # 4
        Rlist.append(self.measure_from_box(x, y, 3000, 1500, 500))
        Rlist.append(self.measure_from_box(x, y, 4000, 1000, 500))  # 6
        Rlist.append(self.measure_from_box(x, y, 3000, 3500, 800))
        Rlist.append(self.measure_from_box(x, y, self.p1, 5500, 500))  # p1
        Rlist.append(self.measure_from_box(x, y, self.p2, 6500, 500))  # p2
        Rlist.append(self.measure_from_box(x, y, self.p3, 7500, 500))  # p3

        return (min(Rlist)[0] > self.RobotRadius)*min(Rlist)[0]

    def create_obstacle_map(self):
        for i in range(self.xsize):
            for j in range(self.ysize):
                self.map[i][j] = self.measure_near_point(
                    5000*i/self.xsize, 8500*j/self.ysize)


if __name__ == "__main__":
    field = Field('red', 1250, 3750, 1300, 400)
