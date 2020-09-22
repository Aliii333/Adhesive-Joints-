import math
import matplotlib.pyplot as mpl
from numpy import arange


class HartSmith:
    def __init__(self, load, adMod, adThick, pRatio, overlapLength, adhesiveThick, adShearMod, width, yieldStress):
        self.className = 'HartSmith'
        self.load = load
        self.adMod = adMod * 1E+9
        self.adThick = adThick / 1000
        self.pRatio = pRatio
        self.overlapLength = overlapLength / 1000
        self.adhesiveThick = adhesiveThick / 1000
        self.adShearMod = (adShearMod/(2*(1+self.pRatio))) * 1E+9
        self.width = width / 1000
        self.yieldStress = yieldStress * 1E+6
        self.unitLoad = self.load / self.width
        self.shear = []
        self.tensile = []
        self.x = arange(-self.overlapLength / 2, self.overlapLength / 2, self.overlapLength / 1000)

    def delta(self):
        return (self.adMod * self.adThick ** 3) / (12 * (1 - self.pRatio ** 2))

    def zeta(self):
        return math.sqrt(self.unitLoad / self.delta())

    def moment(self):
        tmp1 = (self.adThick + self.adhesiveThick) / 2
        tmp2 = 1 / (1 + self.zeta() * self.overlapLength / 2 + (self.zeta() ** 2 * self.overlapLength ** 2 / 6))
        return self.unitLoad * tmp1 * tmp2

    def gamma(self):
        tmp1 = (1 + 3 * (1 - self.pRatio ** 2)) / 4
        tmp2 = (2 * self.adShearMod / (self.adhesiveThick * self.adMod * self.adThick))
        return math.sqrt(tmp1 * tmp2)

    def alpha2(self):
        tmp1 = self.adShearMod / (self.adhesiveThick * self.adMod * self.adThick)
        tmp2 = 1 / (2 * self.gamma() * math.sinh(2 * self.gamma() * self.overlapLength / 2))
        tmp3 = 6 * (1 - self.pRatio ** 2) * self.moment() / self.adThick
        return tmp1 * (self.unitLoad + tmp3) * tmp2

    def charlie2(self):
        tmp1 = (self.alpha2() / self.gamma()) * math.sinh(2 * self.gamma() * self.overlapLength / 2)
        return (1 / 2*self.overlapLength) * (self.unitLoad - tmp1)

    def shearstress(self):
        for X in self.x:
            self.shear.append(self.alpha2() * math.cosh(2 * self.gamma() * X) + self.charlie2())

    def minimumValue(self):
        return min(self.shear) / 1000000

    def maximumValue(self):
        return max(self.shear) / 1000000

    def chi(self):
        tmp1 = self.adShearMod / (2 * self.delta() * self.adhesiveThick)
        return math.pow(tmp1, 0.25)

    def constA(self):
        tmp1 = math.sin(self.chi() * self.overlapLength / 2) - math.cos(self.chi() * self.overlapLength / 2)
        tmp2 = tmp1 * self.adShearMod * self.moment()
        tmp3 = self.adhesiveThick * self.delta() * (self.chi() ** 2) * math.exp(self.chi() * self.overlapLength / 2)
        return -tmp2 / tmp3

    def constB(self):
        tmp1 = math.sin(self.chi() * self.overlapLength / 2) + math.cos(self.chi() * self.overlapLength / 2)
        tmp2 = tmp1 * self.adShearMod * self.moment()
        tmp3 = self.adhesiveThick * self.delta() * (self.chi() ** 2) * math.exp(self.chi() * self.overlapLength / 2)
        return tmp2 / tmp3

    def tensilestress(self):
        for X in self.x:
            self.tensile.append(self.constA() * math.cosh(self.chi() * X) * math.cos(self.chi() * X) + self.constB() * math.sinh(self.chi() * X) * math.sin(self.chi() * X))

    def maximumValueTensile(self):
        return max(self.tensile) /1000000

if __name__ == '__main__':
    # Redundant code - Remove after testing is complete
    hartsmith = HartSmith(1000, 210, 0.0016, 0.35, 0.0125, 0.0002, 3.05E+9, 0.1, 82)
    hartsmith.shearstress()
    hartsmith.tensilestress()
    print(len(hartsmith.shear))
    print(len(hartsmith.x))
    print(hartsmith.shear)
