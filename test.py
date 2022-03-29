# Test file still under develop
import pytest
import random
from zoo import Zoo
from animal import Animal
from caretaker import Caretaker
from enclosure import Enclosure


@pytest.fixture
def zoo1():
    return Zoo()


@pytest.fixture
def tiger1():
    return Animal("Timi", "Tiger", 12)


@pytest.fixture
def tiger2():
    return Animal("Bobik", "Tiger", 2)


@pytest.fixture
def caretaker1():
    return Caretaker("Max", "Vienna")


@pytest.fixture
def caretaker2():
    return Caretaker("Jerome", "Munich")


@pytest.fixture
def enclosure1():
    return Enclosure("Enc 121", 100)


@pytest.fixture
def enclosure2():
    return Enclosure("Enc 123", 50)


class TestAddFunctions:

    def test_add_animal(self, zoo1, tiger1, tiger2):
        initial_animals = len(zoo1.animals)
        zoo1.add_animal(tiger1)
        zoo1.add_animal(tiger2)
        assert len(zoo1.animals) != initial_animals
        assert len(zoo1.animals) == 2
        assert tiger1 in zoo1.animals

    def test_add_enclosure(self, zoo1, enclosure1, enclosure2):
        initial_enclosures = len(zoo1.enclosures)
        zoo1.add_enclosure(enclosure1)
        zoo1.add_enclosure(enclosure2)
        assert len(zoo1.enclosures) != initial_enclosures
        assert len(zoo1.enclosures) == 2
        assert enclosure2 in zoo1.enclosures

    def test_add_caretakers(self, zoo1, caretaker1, caretaker2):
        initial_caretakers = len(zoo1.caretakers)
        zoo1.add_caretaker(caretaker2)
        zoo1.add_caretaker(caretaker1)
        assert len(zoo1.caretakers) != initial_caretakers
        assert len(zoo1.caretakers) == 2
        assert caretaker2 in zoo1.caretakers


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
    zoo.add_animal(Animal("Vasea", "Bear", 1))
    zoo.add_animal(Animal("Gloria", "Hypo", 2))
    zoo.add_animal(Animal("Alex", "Lion", 5))
    zoo.add_caretaker(Caretaker("Max", "Vienna"))
    zoo.add_caretaker(Caretaker("Michel", "Kyiv"))
    zoo.add_caretaker(Caretaker("Roger", "Krems"))
    zoo.add_caretaker(Caretaker("Elena", "Salzburg"))
    zoo.add_enclosure(Enclosure('enc1', 150))
    zoo.add_enclosure(Enclosure('enc1', 100))
    zoo.add_enclosure(Enclosure('enc1', 75))
    return zoo


class TestSerious:

    def test_animal_has_caretaker(self, full_zoo):
        for animal in full_zoo.animals:
            caretaker = random.choice(full_zoo.caretakers)
            caretaker.add_animal(animal)
        for animal in full_zoo.animals:
            assert animal.caretaker is not None
        for caretaker in full_zoo.caretakers:
            assert caretaker.animals is not []

    def test_animal_has_home(self, full_zoo):
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

    def test_delete(self, full_zoo):
        # test death if animal doesn't have any caretaker or enclosure
        animal = random.choice(full_zoo.animals)
        full_zoo.animal_died(animal)
        assert animal not in full_zoo.animals
        assert animal in full_zoo.dead_animals
        # test if animal has everything
        animal = random.choice(full_zoo.animals)
        home = random.choice(full_zoo.enclosures)
        caretaker = random.choice(full_zoo.caretakers)
        caretaker.add_animal(animal)
        full_zoo.animal_home(animal, home)
        full_zoo.animal_died(animal)
        assert animal not in full_zoo.animals
        assert animal in full_zoo.dead_animals
        assert animal not in home.animals
        assert animal not in caretaker.animalsf
