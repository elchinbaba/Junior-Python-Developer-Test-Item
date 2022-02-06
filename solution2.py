'''This is the simple solution for that task. It is passing all the floors along its direction until 
it finishes its work.'''

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
        if self.elevator.direction == 1:
            self.moveup()
        elif self.elevator.direction == -1:
            self.movedown()
    
    def moveup(self):
        '''Moving the elevator up'''
        if not self.elevator.currentfloor < self.lastfloor:
            self.elevator.direction = -1
            return
        self.elevator.currentfloor += 1

    def movedown(self):
        '''Moving the elevator down'''
        if not self.elevator.currentfloor > self.firstfloor:
            self.elevator.direction = 1
            return
        self.elevator.currentfloor -= 1

    def drop_off_and_pick_up(self):
        self.letpeople()
        self.getpeople()
    
    def getpeople(self):
        '''Taking people from the floor'''
        if self.elevator.currentfloor > 0:
            pickinguppeople = []
            if self.floors[self.elevator.currentfloor - 1].people:
                for person in self.floors[self.elevator.currentfloor - 1].people:
                    if person.direction == self.elevator.direction:
                        if not len(self.elevator.currentpeople) < 5:
                            for person in pickinguppeople:
                                self.floors[self.elevator.currentfloor - 1].people.remove(person)
                            return
                        self.elevator.currentpeople.append(person)
                        pickinguppeople.append(person)
                for person in pickinguppeople:
                    self.floors[self.elevator.currentfloor - 1].people.remove(person)
                if pickinguppeople:
                    print(str(len(pickinguppeople)) + " people have been picked up.\n")
            else:
                if self.elevator.currentfloor not in self.emptyfloors:
                    self.emptyfloors.append(self.elevator.currentfloor)
                
    def letpeople(self):
        '''Leaving the people in the elevator at the floor'''
        droppingoffpeople = []
        for person in self.elevator.currentpeople:
            if person.goalfloor == self.elevator.currentfloor:
                droppingoffpeople.append(person)
        for person in droppingoffpeople:
            self.elevator.currentpeople.remove(person)
        floors_peoplepickedup = [person.currentfloor for person in self.elevator.currentpeople]
        for person in droppingoffpeople:
            currentfloor = person.currentfloor
            if currentfloor not in floors_peoplepickedup and len(self.floors[currentfloor - 1].people) == 0 and currentfloor not in self.emptyfloors:
                self.emptyfloors.append(currentfloor)
        if droppingoffpeople:
            print(str(len(droppingoffpeople)) + " people have been dropped off.\n")

    def play(self):
        '''Elevator starts to move'''
        while True:
            if self.elevator.currentfloor != 0:
                print("---------Floor " + str(self.elevator.currentfloor) + "---------")
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
        self.direction = 1

class Floor:
    def __init__(self, numberfloor, people) -> None:
        self.numberfloor = numberfloor
        self.people = people

class Person:
    def __init__(self, currentfloor, goalfloor) -> None:
        self.currentfloor = currentfloor
        self.goalfloor = goalfloor
        self.direction = int((goalfloor-currentfloor)/abs(goalfloor-currentfloor))

numberfloor = randint(5,20)
numberpassengers = [randint(0,3) for i in range(numberfloor)]
peoples = [[Person(i + 1, choice([s for s in range(numberfloor) if s != i]) + 1) for j in range(numberpassengers[i])] for i in range(numberfloor)]

floors = [Floor(i + 1, peoples[i]) for i in range(numberfloor)]
elevator = Elevator(0, [])
building = Building(elevator, floors)

print ("Floors = " + str(numberfloor))

building.play()