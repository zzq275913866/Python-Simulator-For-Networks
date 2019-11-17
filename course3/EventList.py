class EventList:
    elements = []

    def ins(self, x):
        i = 1
        length = len(self.elements)
        while (i <= length and (self.elements[i-1].time < x.time)):
            i = i + 1

        if len(self.elements) == 0:
            self.elements.append(x)
        else:
            self.elements.insert(i-1, x)

    def removefirst(self):

        if len(self.elements) == 0:
            ev = []
            return

        ev = self.elements[0]
        del self.elements[0]
        return ev
