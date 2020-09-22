import math
from numpy import arange
import matplotlib.pyplot as mpl


class volkersen:
    def __init__(self, load, width, pRatio, adShearMod, tpAdThick, btmAdThick, adMod, adhesiveThick, overlapLength, yieldStress):
        self.className = 'Volkersen'
        self.load = load
        self.width = width / 1000
        self.pRatio = pRatio
        self.adShearMod = (adShearMod/(2*(1+self.pRatio))) / 1E+9
        self.tpAdThick = tpAdThick / 1000
        self.btmAdThick = btmAdThick / 1000
        self.adMod = adMod / 1E+9
        self.adhesiveThick = adhesiveThick / 1000
        self.overlapLength = overlapLength / 1000
        self.yieldStress = yieldStress * 1E+6
        self.shear = []
        self.x = arange(-0.5, 0.5, 0.01)


    def psi(self):
        return self.tpAdThick / self.btmAdThick

    def phi(self):
        return (self.adShearMod * self.overlapLength ** 2) / (self.adMod * self.tpAdThick * self.adhesiveThick)

    def omega(self):
        return math.sqrt((1 + self.psi()) * self.phi())

    def shearstress(self):
        for X in range(-50, 50, 1):
            self.shear.append((self.load * self.omega() * math.cosh(self.omega() * X / 100)) / (
                    2 * self.width * self.overlapLength * math.sinh(self.omega() / 2)) + (
                                      self.psi() - 1 / self.psi() + 1) * (self.omega() / 2) * (
                                      math.sinh(self.omega() * X / 100) / math.cosh(self.omega() / 2)))


    def failure(self):
        return math.sqrt(2)*max(self.shear)/1E+6

    def minimumValue(self):
        return min(self.shear) / 1E+6

    def maximumValue(self):
        return max(self.shear) / 1E+6