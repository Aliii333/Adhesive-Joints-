import math
import matplotlib.pyplot as mpl
from numpy import arange


class Goland:
    def __init__(self, load, adMod, adThick, pRatio, overlapLength, adhesiveThick, adShearMod, width, yieldStress, elasticShearStrain, AdhesiveYieldStrength, substrateShearYieldStress):
        self.className = 'Goland'
        self.load = load
        self.adMod = adMod * 1E+9
        self.adThick = adThick / 1000
        self.pRatio = pRatio
        self.overlapLength = overlapLength / 1000
        self.adhesiveThick = adhesiveThick / 1000
        self.adShearMod = (adShearMod/(2*(1+self.pRatio))) * 1E+9
        self.width = width / 1000
        self.yieldStress = yieldStress * 1E+6
        self.elasticShearStrain = elasticShearStrain/1000
        self.AdhesiveYieldStrength = AdhesiveYieldStrength * 1E+6
        self.substrateShearYieldStress = substrateShearYieldStress * 1E+6
        self.unitLoad = self.load / self.width
        self.shear = []
        self.tensile = []
        self.x = arange(-self.overlapLength / 2, self.overlapLength / 2, self.overlapLength / 1000)
        self.smallX = 6.35/1000


    def constK(self):
        return (math.cosh(self.u2()*(self.overlapLength/2))/(math.cosh(self.u2()*(self.overlapLength/2))+2*math.sqrt(2)*math.sinh(self.u2()*(self.overlapLength/2))))

    def beta(self):
        return math.sqrt(8*(self.adShearMod/self.adMod)*(self.adThick/self.adhesiveThick))

    def u2(self):
        return math.sqrt((3*(1-self.pRatio**2))/2)*(1/self.adThick)*math.sqrt(self.unitLoad/(self.adThick*self.adMod))

    def shearstress(self):
        tmp1 = ((self.beta()*(self.overlapLength/2))/self.adThick)*(1+3*self.constK())*(math.cosh(self.beta()*self.smallX/self.adThick)/math.sinh(self.beta()*self.smallX/self.adThick))
        tmp2 = 3*(1-self.constK())
        return -(self.unitLoad/(8*(self.overlapLength/2)))*(tmp1+tmp2)

    def minimumValue(self):
        return min(self.shear) / 1000000

    def maximumValue(self):
        return max(self.shear) / 1000000

    def gamma(self):
        return self.elasticShearStrain/self.adThick

    def greekGamma(self):
        return (6*(self.adShearMod/self.adMod)*(self.adThick/self.adhesiveThick))**(1/4)

    def constKdash(self):
        return ((self.constK()*(self.overlapLength/2))/self.adThick)*math.sqrt(3*(1-self.pRatio**2)*(self.unitLoad/(self.adThick*self.adMod)))

    def constR1(self):
        return math.cosh(self.gamma())*math.sin(self.gamma())+math.sinh(self.gamma())*math.cos(self.gamma())

    def constR2(self):
        return math.sinh(self.gamma())*math.cos(self.gamma())-math.cosh(self.gamma())*math.sin(self.gamma())

    def delta(self):
        return (1/2)*(math.sin(2*self.gamma())+math.sinh(2*self.gamma()))

    def peelstress(self):
        tmp1 = ( (self.constR2()*self.gamma()**2*(self.constK()/2)) + (self.gamma()*self.constKdash()*math.cosh(self.gamma())*math.cos(self.gamma())) ) * ( math.cosh((self.gamma()*self.smallX)/(self.overlapLength/2))*math.cos((self.gamma()*self.smallX)/(self.overlapLength/2)) )
        tmp2 = ( (self.constR1()*self.gamma()**2*(self.constK()/2)) + (self.gamma()*self.constKdash()*math.sinh(self.gamma())*math.sin(self.gamma())) ) * ( math.sinh((self.gamma()*self.smallX)/(self.overlapLength/2))*math.sin((self.gamma()*self.smallX)/(self.overlapLength/2)) )
        return ((self.unitLoad*self.adThick)/(self.delta()*(self.overlapLength/2)**2)) * (tmp1+tmp2)

    def maximumPeel(self):
        return 0

    def Pa (self):
        return self.AdhesiveYieldStrength * self.width * self.overlapLength

    def Ps (self):
        return (self.substrateShearYieldStress*self.adThick*self.width)/(4)

if __name__ == '__main__':
    Goland = Goland(1000, 70, 1.62, 0.4, 12.7, 0.25, 4.82, 25.4, 49, 15)
    print("K constant", Goland.constK())
    #print("Beta: ", Goland.beta())
    #print("u2 : ", Goland.u2())
    #print(Goland.beta()*(Goland.overlapLength/2)/Goland.adThick)
    #print(Goland.beta()*Goland.smallX/Goland.adThick)
    #print(Goland.smallX)
    #print(Goland.overlapLength/2)
    print(Goland.gamma())
    print(Goland.delta())
    #print((math.cosh(Goland.beta()*Goland.smallX/Goland.adThick)))
    #print("Shear Stress", Goland.shearstress())
