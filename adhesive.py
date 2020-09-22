import csv


class adhesive:
    def __init__(self, request):
        self.adFile = csv.reader(open("adhesives.txt", mode="r"))
        self.request = request

    def readFile(self):
        adhesiveValues = 0
        for row in self.adFile:
            name = row[0]
            if name == self.request:
                adhesiveValues = [row[0], row[1], row[2], row[3], row[4], row[5]]
        if adhesiveValues == 0:
            print("Database does not contain adhesive")
            return [0, 0, 0, 0]
        else:
            return adhesiveValues

if __name__ == '__main__':
    ad = adhesive("AV119")
    ad.readFile()

