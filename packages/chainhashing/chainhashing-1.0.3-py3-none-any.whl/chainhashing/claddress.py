class hasharray:
    def __init__(self):
        self.array = [LinkedList() for _ in range(10)]
        self.size = 10

    def __init__(self, size):
        self.array = [LinkedList() for _ in range(size)]
        self.size = size

    def hFunc(self, key):
        value = 0
        for i in range(0,len(key)):
            value += ord(key[i])
        return value % self.size

    def insert(self, key):
        newElement = Element(key)
        index = self.hFunc(newElement.key)
        self.array[index].insert(newElement)

    def erase(self, key):
        index = self.hFunc(key)
        self.array[index].remove(key)

    def find(self, key):
        index = self.hFunc(key)
        for i in range(0, self.array[index].size):
            if self.array[index].get(i).key == key:
                return self.array[index].get(i)
        return None

    def printTable(self):
        print("Hash Table:\n")
        for i in range(0, self.size):
            print(f"Bucket {i}: ", end="")
            self.array[i].printList()
            print("", end="\n")

    def get_size(self):
        return self.size

    def get_values(self):
        values = ""
        for i in range(self.size):
            values += self.array[i].getList()
            if i != self.size - 1:
                values += ", "
        return values

    def clear(self):
        self.array = []
        self.size = 0
class LinkedList:
    def __init__(self):
        self.head = None
        self.size = 0

    def insert(self, newElement):
        if self.head == None:
            self.head = newElement
        else:
            temp = self.head
            while temp.next != None:
                temp = temp.next
            temp.next = newElement
        self.size += 1
        
    def remove(self, key):
        temp = self.head
        if temp.key == key:
            self.head = temp.next
            self.size -= 1
            return
        while temp.next != None:
            if temp.next.key == key:
                temp.next = temp.next.next
                self.size -= 1
                return
            temp = temp.next

    def get(self, index):
        temp = self.head
        for i in range(0, index):
            temp = temp.next
        return temp

    def printList(self):
        temp = self.head
        while temp != None:
            print(f"{temp.key}", end="")
            temp = temp.next
            if (temp != None):
                print(", ", end="")
        print("", end="\n")
    
    def getList(self):
        temp = self.head
        values = ""
        while temp != None:
            values += temp.key
            if temp.next != None:
                values += ", "
            temp = temp.next
        return values

    def get_size(self):
        return self.size

    def clear(self):
        self.head = None
        self.size = 0
class Element:
    def __init__(self):
        self.key = ""
        self.next = None
    def __init__(self, key):
        self.key = key
        self.next = None