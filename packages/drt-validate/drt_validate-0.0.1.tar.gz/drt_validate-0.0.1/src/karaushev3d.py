import math
import numpy as np

class Karaushev3d:

    """
    Keyword arguments:
    Qe -- расход воды в потоке выше выпуска сточных вод
    Qst -- расход сточных вод
    Vsr -- средняя скорость течения
    Sst -- концентрация вещества
    Se -- фоновая концентрация
    H -- средняя глубина водного объекта
    B -- ширина водного объекта
    D -- коэффициент турбулентной диффузии
    C -- коэффициент Шези
    M -- коэффициент Маннинга
    """
    def __init__(self, Qe, Qst, Vsr, Sst, Se, H, B, Nsh, length):
        self.Qe = Qe
        self.Qst = Qst
        self.Vsr = Vsr
        self.Sst = Sst
        self.Se = Se
        self.H = H
        self.B = B
        self.Nsh = Nsh
        self.g = 9.81
        self.length = length

        self.D = None
        self.C = None
        self.M = None
        self.arr = None
        self.deltaZ = None
        self.deltaX = None
        self.countZ = None
        self.countX = None

    def pre_calculate(self):
        print(f"H = {self.H}")

        self.C = math.pow(self.H, 1/6) / self.Nsh
        print(f'C = {self.C}')
        if self.C <= 60:
            self.M = 0.7 * self.C + 6
        else:
            self.M = 48

        print(f"M = {self.M}")
        self.D = self.g * self.H * self.Vsr / (self.M * self.C)
        print(f"D = {self.D}")
        self.deltaZ = self.Qst / (self.H * self.Vsr)
        self.deltaZ = round(self.deltaZ, 2)
        if self.deltaZ <= 5:
            self.deltaZ = 5
        print(f"dz = {self.deltaZ}")
        self.deltaX = (0.25 * self.Vsr * self.deltaZ * self.deltaZ) / self.D

        self.countX = math.ceil(self.length / self.deltaX)
        self.countZ = math.ceil(self.H / self.deltaZ)
        self.arr = np.zeros((self.countZ, self.countX))
        self.arr[:] = self.Se
        self.arr[0][0] = self.Sst



        return self.arr, self.deltaX

    def calculate_iteration(self, x, step):
        tmp = np.zeros((self.countZ, self.countX))
        for i in range(self.countZ):
            for j in range(self.countX):
                tmp[i][j] = (self.get(self.arr, i, j + 1) + self.get(self.arr, i, j - 1) +
                             self.get(self.arr, i + 1, j) + self.get(self.arr, i - 1, j)) / 4
        self.arr = tmp
        x += self.deltaX
        step += 1
        return self.arr, x, step

    def get(self, arr, i, j):
        if i >= len(arr):
            i = len(arr) - 1
        if j >= len(arr[0]):
            j = len(arr[0]) - 1

        if i < 0:
            i = 0
        if j < 0:
            j = 0

        return arr[i][j]
