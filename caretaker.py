import uuid


class Caretaker:

    def __init__(self, name, address):
        self.caretaker_id = str(uuid.uuid4())
        self.name = name
        self.address = address
        self.animals = []

    def add_animal(self, animal):
        self.animals.append(animal)
        animal.caretaker = self.caretaker_id
