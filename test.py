# Test file still under develop
import pytest
import random
from zoo import Zoo
from animal import Animal
from caretaker import Caretaker
from enclosure import Enclosure


@pytest.fixture
def full_zoo():

    zoo = Zoo()

    zoo.add_animal(Animal("Timi", "Tiger", 12))
    zoo.add_animal(Animal("Rex", "Tiger", 9))
    zoo.add_animal(Animal("Melman", "Panther", 3))
    zoo.add_animal(Animal("Julien", "Panther", 7))
    zoo.add_animal(Animal("Marty", "Zebra", 8))
    zoo.add_animal(Animal("Mort", "Panther", 11))
    zoo.add_animal(Animal("Kowalski", "Pinguin", 21))
    zoo.add_animal(Animal("Sergey", "Bear", 1))
    zoo.add_animal(Animal("Gloria", "Hypo", 2))
    zoo.add_animal(Animal("Alex", "Lion", 5))

    zoo.add_caretaker(Caretaker("Max", "Vienna"))
    zoo.add_caretaker(Caretaker("Michel", "Kyiv"))
    zoo.add_caretaker(Caretaker("Roger", "Krems"))
    zoo.add_caretaker(Caretaker("Elena", "Salzburg"))

    zoo.add_enclosure(Enclosure('enc1', 150))
    zoo.add_enclosure(Enclosure('enc2', 100))
    zoo.add_enclosure(Enclosure('enc3', 75))

    return zoo


class TestAddFunctions:

    def test_add_animal(self):
        zoo1 = Zoo()
        initial_animals = len(zoo1.animals)
        tiger1 = Animal("Timi", "Tiger", 12)
        tiger2 = Animal("Rex", "Tiger", 9)
        zoo1.add_animal(tiger1)
        zoo1.add_animal(tiger2)
        assert len(zoo1.animals) != initial_animals
        assert len(zoo1.animals) == 2
        assert tiger1 in zoo1.animals

    def test_add_enclosure(self):
        zoo1 = Zoo()
        initial_enclosures = len(zoo1.enclosures)
        enclosure1 = Enclosure('enc1', 150)
        enclosure2 = Enclosure('enc2', 100)
        zoo1.add_enclosure(enclosure1)
        zoo1.add_enclosure(enclosure2)
        assert len(zoo1.enclosures) != initial_enclosures
        assert len(zoo1.enclosures) == 2
        assert enclosure2 in zoo1.enclosures

    def test_add_caretakers(self):
        zoo1 = Zoo()
        initial_caretakers = len(zoo1.caretakers)
        caretaker1 = Caretaker("Max", "Vienna")
        caretaker2 = Caretaker("Michel", "Kyiv")
        zoo1.add_caretaker(caretaker2)
        zoo1.add_caretaker(caretaker1)
        assert len(zoo1.caretakers) != initial_caretakers
        assert len(zoo1.caretakers) == 2
        assert caretaker2 in zoo1.caretakers


class TestSerious:

    def test_vet(self, full_zoo):
        for animal in full_zoo.animals:
            animal.vet()
            assert len(animal.medical_record) == 1

    def test_feed(self, full_zoo):
        for animal in full_zoo.animals:
            animal.feed()
            assert len(animal.feeding_record) == 1

    def test_animal_has_caretaker(self, full_zoo):
        for animal in full_zoo.animals:
            caretaker = random.choice(full_zoo.caretakers)
            caretaker.add_animal(animal)
        for animal in full_zoo.animals:
            assert animal.caretaker is not None
        for caretaker in full_zoo.caretakers:
            assert caretaker.animals is not []

    def test_animal_home(self, full_zoo):
        for animal in full_zoo.animals:
            home = random.choice(full_zoo.enclosures)
            full_zoo.animal_home(animal, home)
        for animal in full_zoo.animals:
            assert animal.enclosure is not None
        for enclosure in full_zoo.enclosures:
            assert enclosure.animals is not []

    def test_very_sad(self, full_zoo):
        # test death if animal doesn't have any caretaker or enclosure
        poor_animal = random.choice(full_zoo.animals)
        full_zoo.animal_died(poor_animal)
        assert poor_animal not in full_zoo.animals
        assert poor_animal in full_zoo.dead_animals
        # test if animal has everything
        poor_animal = random.choice(full_zoo.animals)
        home = random.choice(full_zoo.enclosures)
        caretaker = random.choice(full_zoo.caretakers)
        caretaker.add_animal(poor_animal)
        full_zoo.animal_home(poor_animal, home)
        full_zoo.animal_died(poor_animal)
        assert poor_animal not in full_zoo.animals
        assert poor_animal in full_zoo.dead_animals
        assert poor_animal not in home.animals
        assert poor_animal not in caretaker.animals

    def test_delete_animal(self, full_zoo):
        animal = random.choice(full_zoo.animals)
        home = random.choice(full_zoo.enclosures)
        caretaker = random.choice(full_zoo.caretakers)
        caretaker.add_animal(animal)
        full_zoo.animal_home(animal, home)
        assert animal in full_zoo.animals
        assert animal in home.animals
        assert animal in caretaker.animals
        full_zoo.remove_animal(animal)
        assert animal not in full_zoo.animals
        assert animal not in home.animals
        assert animal not in caretaker.animals

    def test_remove_enclosure(self, full_zoo):
        for animal in full_zoo.animals:
            home = random.choice(full_zoo.enclosures)
            full_zoo.animal_home(animal, home)
            assert animal.enclosure is not None
        enclosure = random.choice(full_zoo.enclosures)
        full_zoo.remove_enclosure(enclosure)
        assert enclosure not in full_zoo.enclosures
        for animal in enclosure.animals:
            assert animal.enclosure != enclosure.enclosure_id
        small_zoo = Zoo()
        animal1 = Animal('animal1', 'animal1', 1)
        enclosure1 = Enclosure('enclosure1', 100)
        small_zoo.add_animal(animal1)
        small_zoo.add_enclosure(enclosure1)
        small_zoo.animal_home(animal1, enclosure1)
        assert animal1 in enclosure1.animals
        small_zoo.remove_enclosure(enclosure1)
        assert animal1.enclosure is None
        assert enclosure1 not in small_zoo.enclosures


def test_ubertest(full_zoo):
    for animal in full_zoo.animals:
        caretaker = random.choice(full_zoo.caretakers)
        caretaker.add_animal(animal)
        home = random.choice(full_zoo.enclosures)
        full_zoo.animal_home(animal, home)
        assert animal.caretaker is not None and animal.enclosure is not None
        assert animal in caretaker.animals and animal in home.animals
    for i in range(random.randint(0, len(full_zoo.animals))):
        animal = random.choice(full_zoo.animals)
        animal.feed().vet()
        assert animal.feeding_record is not [] and animal.medical_record is not []
    # happy child
    mother = random.choice(full_zoo.animals)
    kid = mother.birth()
    full_zoo.add_animal(kid)
    enclosure = full_zoo.get_enclosure(mother.enclosure)
    caretaker = full_zoo.get_caretaker(mother.caretaker)
    assert kid.common_name == mother.common_name and kid.species == mother.specie and kid.age == 0
    assert kid in enclosure.animals and kid in caretaker.animals
    # cleaning
    for i in range(random.randint(0, len(full_zoo.enclosures))):
        enclosure = random.choice(full_zoo.enclosures)
        enclosure.clean()
        assert enclosure.cleaning_record is not []
    # very sad (((
    poor_animal = random.choice(full_zoo.animals)
    full_zoo.animal_died(poor_animal)
    assert poor_animal not in full_zoo.animals
    assert poor_animal in full_zoo.dead_animals
    assert poor_animal not in full_zoo.get_enclosure(poor_animal.enclosure).animals
    assert poor_animal not in full_zoo.get_caretaker(poor_animal.caretaker).animals
