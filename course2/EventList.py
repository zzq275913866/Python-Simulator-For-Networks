import bisect


class EventList:
    elements = []

    def ins(self, x):
        bisect.insort(self.elements, x)

    def remove_first(self):
        if len(self.elements) == 0:
            return
        ev = self.elements.pop(0)
        return ev
