import matplotlib.pyplot as mpl


class graphOutput:
    def __init__(self, className):
        mpl.close('all')
        self.className = className

    def createFA(self):
        area = self.className.overlapLength * self.className.width
        stress = []
        for i in range(len(self.className.x)):
            stress.append(self.className.load / area)
        print(max(stress) / 1E+6)
        return [value / 1E+6 for value in stress]

    def createSigma(self):
        yieldStress = []
        for i in range(len(self.className.x)):
            yieldStress.append(self.className.yieldStress)
        return yieldStress

    def outputGraph(self):
        if self.className.className == "HartSmith":
            mpl.figure(self.className.className + ' Tensile Stress')
            mpl.plot(self.className.x, [value / 1E+6 for value in self.className.tensile], label='Tensile Stress')
            mpl.legend()
            mpl.xlabel('Distance from overlap centre / m')
            mpl.ylabel('Tensile Stress / MPa')
            mpl.title('Normal Stress in adhesive joint ' + str(self.className.className))
        mpl.figure(self.className.className + ' Shear Stress')
        mpl.plot(self.className.x, [value / 1E+6 for value in self.className.shear], label='Shear Stress')
        mpl.legend()
        mpl.plot(self.className.x, self.createFA(), label='Force/Area Calculation')
        mpl.legend()
        mpl.xlabel('Distance from overlap centre / m')
        mpl.ylabel('Shear Stress / MPa')
        mpl.title('Shear Stress in adhesive joint ' + str(self.className.className))
        mpl.show()