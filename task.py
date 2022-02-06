'''This is the solution of the given task. In the task there was a situation which was not considered.
If the maximum floor elevator was going to visit is less than any floor has some people, those people
were going to stay in the same floor without getting picked up. But this code has a function is considering it.
This can be optimized by the function which picks up the people who are going to the closest floors.'''

from math import *
from random import *

class Building:
    def __init__(self, elevator, floors) -> None:
        self.elevator = elevator
        self.floors = floors
        self.lastfloor = len(floors)
        self.firstfloor = 1
        self.emptyfloors = []
    
    def move(self):
        '''Moving the elevator'''
        self.drop_off_and_pick_up()
        if self.elevator.direction == '+':
            self.moveup()
        elif self.elevator.direction == '-':
            self.movedown()
    
    def drop_off_and_pick_up(self):
        self.letpeople()
        self.getpeople()
    
    def letpeople(self):
        '''Leaving the people in the elevator at the floor'''
        droppingoffpeople = []
        for person in self.elevator.currentpeople:
            if person.goalfloor == self.elevator.currentfloor:
                droppingoffpeople.append(person)
                #self.elevator.currentpeople.remove(person)
        for person in droppingoffpeople:
            self.elevator.currentpeople.remove(person)
        floors_peoplepickedup = [person.currentfloor for person in self.elevator.currentpeople]
        for person in droppingoffpeople:
            currentfloor = person.currentfloor
            if currentfloor not in floors_peoplepickedup and len(self.floors[currentfloor - 1].people) == 0 and currentfloor not in self.emptyfloors:
                self.emptyfloors.append(currentfloor)
                print("Empty floors: " + str(self.emptyfloors))
        if droppingoffpeople:
            print(str(len(droppingoffpeople)) + " people have been dropped off.\n")

    def getpeople(self):
        '''Taking people from the floor'''
        if self.elevator.currentfloor != 0:
            if not self.elevator.currentpeople:
                print("Making a decision...")
                plusdirection = len([person for person in self.floors[self.elevator.currentfloor - 1].people if person.direction == 1])
                minusdirection = len([person for person in self.floors[self.elevator.currentfloor - 1].people if person.direction == -1])
                if plusdirection > minusdirection:
                    self.elevator.direction = '+'
                elif minusdirection > plusdirection:
                    self.elevator.direction = '-'
            
            pickinguppeople = []
            if self.floors[self.elevator.currentfloor - 1].people:
                for person in self.floors[self.elevator.currentfloor - 1].people:
                    if person.direction == convertit(self.elevator.direction):
                        if not len(self.elevator.currentpeople) < 5:
                            for person in pickinguppeople:
                                self.floors[self.elevator.currentfloor - 1].people.remove(person)
                            if pickinguppeople:
                                print(str(len(pickinguppeople)) + " people have been picked up.\n")
                            return
                        self.elevator.currentpeople.append(person)
                        pickinguppeople.append(person)
                        #self.floors[self.elevator.currentfloor - 1].people.remove(person)
                for person in pickinguppeople:
                    self.floors[self.elevator.currentfloor - 1].people.remove(person)
                if pickinguppeople:
                    print(str(len(pickinguppeople)) + " people have been picked up.\n")
                    #if len(self.floors[self.elevator.currentfloor - 1].people) == 0 and self.elevator.currentfloor not in self.emptyfloors:
                        #self.emptyfloors.append(self.elevator.currentfloor)
            else:
                if self.elevator.currentfloor not in self.emptyfloors:
                    self.emptyfloors.append(self.elevator.currentfloor)
                    print("Empty floors: " + str(self.emptyfloors))

    def moveup(self):
        '''Moving the elevator up'''
        self.updatelastfloor()
        if not self.elevator.currentfloor < self.lastfloor:
            self.elevator.direction = '-'
            return
        self.elevator.currentfloor += 1

    def updatelastfloor(self):
        '''Updating the last floor elevator is going to visit'''
        goalfloors = [person.goalfloor for person in self.elevator.currentpeople]
        if goalfloors:
            self.lastfloor = max(goalfloors)
            #print("Last floor = " + str(self.lastfloor))
        
        #The situation I talked about in the above.
        floorspeopleremain = [i + 1 for i in range(self.lastfloor, len(self.floors)) if self.floors[i].people]
        if floorspeopleremain:
            self.lastfloor = max(self.lastfloor, max(floorspeopleremain))
            #print("Last floor is " + str(self.lastfloor))
        for i in range(self.lastfloor, len(self.floors)):
            if len(self.floors[i].people) == 0 and i + 1 not in self.emptyfloors:
                self.emptyfloors.append(i + 1)
                print("Empty floors= " + str(self.emptyfloors))

    def movedown(self):
        '''Moving the elevator down'''
        self.updatefirstfloor()
        if not self.elevator.currentfloor > self.firstfloor:
            self.elevator.direction = '+'
            return
        self.elevator.currentfloor -= 1

    def updatefirstfloor(self):
        '''Updating the least floor elevator is going to visit'''
        goalfloors = [person.goalfloor for person in self.elevator.currentpeople]
        if goalfloors:
            self.firstfloor = min(goalfloors)
            #print("First floor = " + str(self.firstfloor))
        
        #The situation I talked about in the above.
        floorspeopleremain = [i + 1 for i in range(0, self.firstfloor) if self.floors[i].people]
        if floorspeopleremain:
            self.firstfloor = min(self.firstfloor, min(floorspeopleremain))
            #print("First floor is " + str(self.firstfloor))
        for i in range(0, self.firstfloor):
            if len(self.floors[i].people) == 0 and i + 1 not in self.emptyfloors:
                self.emptyfloors.append(i + 1)
                print("Empty floors= " + str(self.emptyfloors))

    def play(self):
        '''Elevator starts to move'''
        while True:
            if self.elevator.currentfloor != 0:
                print("-------------Floor " + str(self.elevator.currentfloor) + "-------------")
                print("In the floor " + str(self.floors[self.elevator.currentfloor - 1].numberfloor) + " there are " + str(len(self.floors[self.elevator.currentfloor - 1].people)) + " people:")
                for person in self.floors[self.elevator.currentfloor - 1].people:
                    print("from " + str(person.currentfloor) + " -> " + str(person.goalfloor))

                print("\n")

            self.move()

            if self.elevator.currentfloor != 0:
                print("In the elevator there are " + str(len(self.elevator.currentpeople)) + " people:")
                for person in self.elevator.currentpeople:
                    print("from " + str(person.currentfloor) + " -> " + str(person.goalfloor))
                
                print("\n")
                
            if len(self.emptyfloors) == len(self.floors):
                break

class Elevator:
    def __init__(self, currentfloor, people) -> None:
        self.currentfloor = currentfloor
        self.currentpeople = people
        self.direction = '+'

class Floor:
    def __init__(self, numberfloor, people) -> None:
        self.numberfloor = numberfloor
        self.people = people

class Person:
    def __init__(self, currentfloor, goalfloor) -> None:
        self.currentfloor = currentfloor
        self.goalfloor = goalfloor
        self.direction = int((goalfloor-currentfloor)/abs(goalfloor-currentfloor))

def convertit(var):
    '''Creating relation between [-1,1] and ['-','+']'''
    if var == '+':
        return 1
    elif var == 1:
        return '+'
    elif var == '-':
        return -1
    elif var == -1:
        return '-'

numberfloor = randint(5,20)
numberpassengers = [randint(0,9) for i in range(numberfloor)]
peoples = [[Person(i + 1, choice([s for s in range(numberfloor) if s != i]) + 1) for j in range(numberpassengers[i])] for i in range(numberfloor)]

floors = [Floor(i + 1, peoples[i]) for i in range(numberfloor)]
elevator = Elevator(0, [])
building = Building(elevator, floors)

print ("Floors = " + str(numberfloor))

building.play()