import uuid 
import datetime


class Animal:

    def __init__(self, name, common_name, age):
        self.animal_id = str(uuid.uuid4())
        self.species = name
        self.common_name = common_name
        self.age = age
        self.feeding_record = []
        self.medical_record = []
        self.enclosure = None
        self.caretaker = None

    def feed(self):
        self.feeding_record.append(datetime.datetime.now())

    def vet(self):
        self.medical_record.append(datetime.datetime.now())

    def birth(self):
        return Child(self)


class Child(Animal):

    def __init__(self, mother):
        self.animal_id = str(uuid.uuid4())
        self.species = mother.species
        self.common_name = mother.common_name
        self.age = 0
        self.feeding_record = []
        self.medical_record = []
        self.enclosure = mother.enclosure
        self.caretaker = mother.caretaker
