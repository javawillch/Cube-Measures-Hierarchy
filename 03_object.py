

class Point:
    def __init__(self, x, y):
        super().__init__()
        self.x=x
        self.y=y
    
    def show_point(self):
        print(self.x, self.y)

    def distance(self, targetX, targetY):
        return (((self.x-targetX)**2)+((self.y-targetY)**2))**0.5

p1=Point(1,5)
p2=Point(100,555)
print(p1.x, p1.y)
print(p2.x, p2.y)
p1.show_point()
print(p1.distance(0,0))


class FullName:
    def __init__(self, first, last):
        super().__init__()
        self.first=first
        self.last=last

people1=FullName("AAA", "DEW")
print(people1.first, people1.last)


class File:
    def __init__(self, name):
        super().__init__()
        self.name=name
        self.file=None # Not open file yet, default is None
    
    def open(self):
        self.file=open(self.name, mode="r", encoding="utf-8")
    
    def read(self):
        return self.file.read()

f1=File("inp_to_be_delete_measure_list.txt")
f1.open()
data=f1.read()
print(data)