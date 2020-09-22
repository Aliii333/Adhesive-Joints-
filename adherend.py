import csv


class adherend:
    def __init__(self, request):
        self.adFile = csv.reader(open("adherends.txt", mode="r"))
        self.request = request

    def readFile(self):
        adherendValues = 0
        for row in self.adFile:
            name = row[0]
            if name == self.request:
                adherendValues = [row[0], row[1], row[2], row[3], row[4], row[5]]
        if adherendValues == 0:
            print("Database does not contain adherend")
            return [0, 0, 0]
        else:
            return adherendValues
