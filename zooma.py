from flask import Flask, jsonify
from flask_restx import Api, reqparse, Resource
from zoo_json_utils import ZooJsonEncoder 
from zoo import Zoo
from animal import Animal
from caretaker import Caretaker
from enclosure import Enclosure

my_zoo = Zoo()

zooma_app = Flask(__name__)
# need to extend this class for custom objects, so that they can be jsonified
zooma_app.json_encoder = ZooJsonEncoder 
zooma_api = Api(zooma_app)

animal_parser = reqparse.RequestParser()
animal_parser.add_argument('Species', type=str, required=True, help='The specie of the animal, e,g. Panthera tigris')
animal_parser.add_argument('Name', type=str, required=True, help='The common name of the animal, e.g., Rex')
animal_parser.add_argument('Age', type=int, required=True, help='The age of the animal, e.g., 12')

enclosure_parser = reqparse.RequestParser()
enclosure_parser.add_argument('Name', type=str, required=True, help='The name of the Enclosure, e.g., Tiger Cave 123')
enclosure_parser.add_argument('Area', type=int, required=True, help='Area of the Enclosure, e.g., 20')

caretaker_parser = reqparse.RequestParser()
caretaker_parser.add_argument('Name', type=str, required=True, help='The name of the caretaker, e.g., Mike')
caretaker_parser.add_argument('Address', type=str, required=True, help='Address of the caretaker, e.g., Ringstraße 13')


animal = reqparse.RequestParser()
animal.add_argument('animal_id', type=str, required=True)

enclosure = reqparse.RequestParser()
enclosure.add_argument('enclosure_id', type=str, required=True)


# ANIMALS
@zooma_api.route('/animal')
class AddAnimalAPI(Resource):
    @zooma_api.doc(parser=animal_parser)
    def post(self):
        # get the post parameters 
        args = animal_parser.parse_args()
        species = args['Species']
        name = args['Name']
        age = args['Age']
        # create a new animal object
        if age < 0:
            return jsonify("Age could not be a negative value")
        new_animal = Animal(species, name, age)
        # add the animal to the zoo
        my_zoo.add_animal(new_animal)
        return jsonify(new_animal) 
    

@zooma_api.route('/animal/<animal_id>')
class AnimalID(Resource):

    def get(self, animal_id):
        search_result = my_zoo.get_animal(animal_id)
        if not search_result:
            return jsonify(f"Animal with ID {animal_id} was not found")
        return jsonify(search_result)
    
    def delete(self, animal_id):
        targeted_animal = my_zoo.get_animal(animal_id)
        enclosure = my_zoo.get_enclosure(targeted_animal.enclosure)
        caretaker = my_zoo.get_caretaker(targeted_animal.caretaker)
        if not targeted_animal:
            return jsonify(f"Animal with ID {animal_id} was not found")
        if enclosure:
            enclosure.animals.remove(targeted_animal)
        if caretaker:
            caretaker.animals.remove(targeted_animal)
        my_zoo.remove_animal(targeted_animal)
        return jsonify(f"Animal with ID {animal_id} was removed")


@zooma_api.route('/animals/<animal_id>/feed')
class FeedAnimal(Resource):

    def post(self, animal_id):
        targeted_animal = my_zoo.get_animal(animal_id)
        if not targeted_animal:
            return jsonify(f"Animal with ID {animal_id} was not found")
        targeted_animal.feed()
        return jsonify(targeted_animal)
    
     
@zooma_api.route('/animals')
class AllAnimals(Resource):
    def get(self):
        if not my_zoo.animals:
            return jsonify('No animals detected')
        return jsonify(my_zoo.animals)


@zooma_api.route('/animals/<animal_id>/vet')
class VetAnimal(Resource):
    def post(self, animal_id):
        targeted_animal = my_zoo.get_animal(animal_id)
        if not targeted_animal:
            return jsonify(f"Animal with ID {animal_id} was not found")
        targeted_animal.vet()
        return jsonify(targeted_animal)


@zooma_api.route('/animal/<animal_id>/home')
class HomeAnimal(Resource):
    @zooma_api.doc(parser=enclosure)
    def post(self, animal_id):
        enclosure_id = enclosure.parse_args()['enclosure_id']
        targeted_animal = my_zoo.get_animal(animal_id)
        targeted_enclosure = my_zoo.get_enclosure(enclosure_id)
        if not targeted_animal:
            return jsonify(f'Animal with ID {animal_id} was not found')
        if not targeted_enclosure:
            return jsonify(f'Enclosure with ID {enclosure_id} was not found')
        if not targeted_animal.enclosure:
            targeted_animal.enclosure = enclosure_id
            targeted_enclosure.animals.append(targeted_animal)
            return jsonify(targeted_animal)
        else:
            present_enclosure = my_zoo.get_enclosure(targeted_animal.enclosure)
            present_enclosure.animals.remove(targeted_animal)
            targeted_animal.enclosure = targeted_enclosure.enclosure_id
            targeted_enclosure.animals.append(targeted_animal)
            return jsonify(targeted_animal)


@zooma_api.route('/animal/birth')
class AnimalBirth(Resource):

    @zooma_api.doc(parser=animal)
    def post(self):
        args = animal.parse_args()
        animal_id = args['animal_id']
        mother = my_zoo.get_animal(animal_id)
        enclosure = my_zoo.get_enclosure(mother.enclosure)
        caretaker = my_zoo.get_caretaker(mother.caretaker)
        if not mother:
            return jsonify(f"Animal with ID {animal_id} was not found")
        child = mother.birth()
        my_zoo.add_animal(child)
        if enclosure:
            enclosure.animals.append(child)
        if caretaker:
            caretaker.add_animal(child)
        return jsonify(child)
# animals death


@zooma_api.route('/animal/death')
class AnimalDie(Resource):

    @zooma_api.doc(parser=animal)
    def post(self):
        args = animal.parse_args()
        animal_id = args['animal_id']
        targeted_animal = my_zoo.get_animal(animal_id)
        enclosure = my_zoo.get_enclosure(targeted_animal.enclosure)
        caretaker = my_zoo.get_caretaker(targeted_animal.caretaker)
        if not targeted_animal:
            return jsonify(f"Animal with ID {animal_id} was not found")
        if enclosure:
            enclosure.animals.remove(targeted_animal)
        if caretaker:
            caretaker.animals.remove(targeted_animal)
        my_zoo.animal_died(targeted_animal)
        return jsonify(f"Animal with ID {animal_id} died. RIP. Always in our hearts (((")
# animals stat


@zooma_api.route('/animal/stat')
class AnimalStatistics(Resource):
    def get(self):
        statistics = my_zoo.animals_statistics()
        return jsonify(statistics)


# ENCLOSURES
@zooma_api.route('/enclosure')
class AddEnclosureAPI(Resource):
    @zooma_api.doc(parser=enclosure_parser)
    def post(self):
        # get the post parameters
        args = enclosure_parser.parse_args()
        name = args['Name']
        area = args['Area']
        if area < 0:
            return jsonify("Area could not be a negative value")
        new_enclosure = Enclosure(name, area)
        # add the enclosure to the zoo
        my_zoo.add_enclosure(new_enclosure)
        return jsonify(new_enclosure)


@zooma_api.route('/enclosures')
class AllEnclosures(Resource):
    def get(self):
        return jsonify(my_zoo.enclosures)


@zooma_api.route('/enclosures/<enclosure_id>/clean')
class CleanEnclosure(Resource):
    def post(self, enclosure_id):
        targeted_enclosure = my_zoo.get_enclosure(enclosure_id)
        if not targeted_enclosure:
            return jsonify(f"Enclosure with ID {enclosure_id} was not found")
        targeted_enclosure.clean()
        return jsonify(targeted_enclosure)


@zooma_api.route('/enclosures/<enclosure_id>/animals')
class AllAnimalsInEnclosure(Resource):
    def get(self, enclosure_id):
        targeted_enclosure = my_zoo.get_enclosure(enclosure_id)
        if not targeted_enclosure:
            return jsonify(f"Enclosure with ID {enclosure_id} was not found")
        return jsonify(targeted_enclosure.animals)


@zooma_api.route('/enclosure/<enclosure_id>')
class EnclosureId(Resource):
    def delete(self, enclosure_id):
        targeted_enclosure = my_zoo.get_enclosure(enclosure_id)
        if not targeted_enclosure:
            return jsonify(f"Enclosure with ID {enclosure_id} was not found")
        my_zoo.remove_enclosure(targeted_enclosure)
        return jsonify(f"Enclosure with ID {enclosure_id} was removed")


# CARETAKERS
@zooma_api.route('/caretaker/')
class AddCaretakerAPI(Resource):
    @zooma_api.doc(parser=caretaker_parser)
    def post(self):
        args = caretaker_parser.parse_args()
        name = args['Name']
        address = args['Address']
        new_caretaker = Caretaker(name, address)
        my_zoo.add_caretaker(new_caretaker)
        return jsonify(new_caretaker)


@zooma_api.route('/caretaker/<caretaker_id>/care/<animal_id>/')
class CaretakerTakeCare(Resource):
    def post(self, caretaker_id, animal_id):
        targeted_animal = my_zoo.get_animal(animal_id)
        targeted_caretaker = my_zoo.get_caretaker(caretaker_id)
        previous_caretaker = my_zoo.get_caretaker(targeted_animal.caretaker)
        if previous_caretaker:
            previous_caretaker.animals.remove(targeted_animal)
        if not targeted_caretaker:
            return jsonify(f"Caretaker with ID {caretaker_id} was not found")
        if not targeted_animal:
            return jsonify(f"Animal with ID {animal_id} was not found")
        targeted_caretaker.add_animal(targeted_animal)
        return jsonify(targeted_caretaker)


@zooma_api.route('/caretaker/<caretaker_id>/care/animals')
class AllAnimalsAtCaretaker(Resource):
    def get(self, caretaker_id):
        targeted_caretaker = my_zoo.get_caretaker(caretaker_id)
        if not targeted_caretaker:
            return jsonify(f"Caretaker with ID {caretaker_id} was not found")
        return jsonify(targeted_caretaker.animals)


# caretaker stats
@zooma_api.route('/caretakers/stats')
class CaretakersStats(Resource):
    def get(self):
        stats = my_zoo.caretakers_statistics()
        return jsonify(stats)


@zooma_api.route('/caretaker/<caretaker_id>')
class CaretakerId(Resource):
    def delete(self, caretaker_id):
        targeted_caretaker = my_zoo.get_caretaker(caretaker_id)
        if not targeted_caretaker:
            return jsonify(f"Caretaker with ID {caretaker_id} was not found")
        my_zoo.remove_caretaker(targeted_caretaker)
        return jsonify(f"Caretaker with ID {caretaker_id} was removed")


@zooma_api.route('/caretakers')
class AllCaretakers(Resource):
    def get(self):
        return jsonify(my_zoo.caretakers)


# TASKS
@zooma_api.route('/tasks/cleaning/')
class CleaningTasks(Resource):
    def get(self):
        return jsonify(my_zoo.cleaning())


@zooma_api.route('/tasks/medical/')
class MedicalTasks(Resource):
    def get(self):
        return jsonify(my_zoo.medical())


@zooma_api.route('/tasks/feeding/')
class FeedingTasks(Resource):
    def get(self):
        return jsonify(my_zoo.feeding())


if __name__ == '__main__':
    zooma_app.run(debug=False, port=7890)
