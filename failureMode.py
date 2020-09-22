import math


class failureMode:
    def __init__(self, maxShearStress, maxPeelStress, adMod, adShearMod, GAdhesive, GAdherend, SubShearYieldStress, AdhesiveYieldStrength,
                 ThroughThinckness, InterlaminarShearStrength):
        self.maxShearStress = maxShearStress * 1E+6
        self.maxPeelStress = maxPeelStress * 1E+6
        self.adShearMod = adShearMod * 1E+9
        self.adMod = adMod * 1E+9
        self.GAdhesive = GAdhesive * 1E+9
        self.GAdherend = GAdherend * 1E+9
        self.SubShearYieldStress = SubShearYieldStress * 1E+6
        self.AdhesiveYieldStrength = AdhesiveYieldStrength * 1E+6
        self.X = ThroughThinckness *1E+6
        self.S = InterlaminarShearStrength *1E+6

    def substratePeelStress (self):
        return (self.maxPeelStress/self.adShearMod)*self.adMod

    def substrateShearStress (self):
        return (self.maxShearStress/self.GAdhesive)*self.GAdherend

    def principleStress1 (self):
        return (self.substratePeelStress() / 2) + math.sqrt((self.substratePeelStress() / 2) ** 2 + self.substrateShearStress() ** 2)

    def principleStress2 (self):
        return (self.substratePeelStress()/2) - math.sqrt((self.substratePeelStress()/2)**2 + self.substrateShearStress()**2)

    def vonMises (self):
        return (math.sqrt((self.principleStress1()**2)-self.principleStress1()*self.principleStress2()+(self.principleStress2()**2)))/1E+6

    def principleStress1Adhesive (self):
        return ((self.maxPeelStress/2) + math.sqrt((self.maxPeelStress/2)**2 + self.maxShearStress**2))/1E+6

    def principleStress2Adhesive (self):
        return ((self.maxPeelStress/2) - math.sqrt((self.maxPeelStress/2)**2 + self.maxShearStress**2))/1E+6
    def principleStress3Adhesive (self):
        return 0

    def DruckerPrager(self):
        return (((1.5-1)/(2*1.5)*(self.principleStress1Adhesive()+self.principleStress2Adhesive()+self.principleStress3Adhesive()) +
                ((1.5+1)/(2*1.5)))*(math.sqrt(((self.principleStress1Adhesive()-self.principleStress2Adhesive())**2 +
                                           (self.principleStress2Adhesive()-self.principleStress3Adhesive())**2 +
                                           (self.principleStress3Adhesive()-self.principleStress1Adhesive())**2)/2)))
    def TsaiWu(self):
        return ((self.substratePeelStress()/self.X)**2 + (self.substrateShearStress()/self.S)**2)



    def failureCheck (self, failureCheckType):

        if failureCheckType == "VonMises": #Von mises check
            if self.vonMises() > self.SubShearYieldStress:
                return "Von Mises: The joint (Substrate) will fail"
            else:
                return "Von Mises: The joint (Substrate) will not fail"

        elif failureCheckType == "DruckerPrager": #Druker prager check
            if self.DruckerPrager() >= self.AdhesiveYieldStrength:
                return "Drucker Prager: Adhesive will fail"
            else:
                return "Drucker Prager: Adhesive will not fail"

        elif failureCheckType == "TsaiWu": #TsaiWu Check
            if self.TsaiWu() <= 1:
                return "Tsai Wu: Composite Adherend will not fail"
            else:
                return "Tsai Wu: Composite Adherend will fail"
        elif failureCheckType == "choose":
                return "Check failure criteria from the drop-down menu"


if __name__ == '__main__':
    object_ = failureMode(7.704, 5.925, 75, 2.5, 1.2, 24, 276, 0,50,90)
    print(object_.substratePeelStress())
    print(object_.substrateShearStress())
    #print(object_.principleStress1())
    #print(object_.principleStress2())
    #print(object_.vonMises())
    #print(object_.failureCheck())
    #print("-----------")
    #print(object_.maxPeelStress)
    #print(object_.maxShearStress)
    #print(object_.principleStress1Adhesive())
    #print(object_.principleStress2Adhesive())
    #print(object_.DruckerPrager())
    #object_.function()
    print(object_.TsaiWu())
    print(object_.failureCheck(3))
