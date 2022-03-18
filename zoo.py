import random


class Zoo:

    def __init__(self):
        self.animals = []
        self.caretakers = []
        self.enclosures = []
        self.dead_animals = []

    # all functions that are related to animals

    def add_animal(self, animal):
        self.animals.append(animal)

    def remove_animal(self, animal):
        self.animals.remove(animal)

    def animal_died(self, animal):
        self.dead_animals.append(animal)
        self.animals.remove(animal)

    def get_animal(self, animal_id):
        for animal in self.animals:
            if animal.animal_id == animal_id:
                return animal

    def animals_statistics(self):
        # total animal per species
        animal_per_specie = {}
        animals = []
        if not self.animals:
            return 'No animals detected'
        for animal in self.animals:
               animals.append(animal.species)
        for animal in animals:
            animal_per_specie[animal] = animals.count(animal)
            # Average number per enclosure
        animals_per_enclosure = []
        for enclosure in self.enclosures:
            animals_per_enclosure.append(len(enclosure.animals))
        if len(animals_per_enclosure) > 0:
            average_number_of_animals_per_enclosure = sum(animals_per_enclosure)/len(animals_per_enclosure)
        else:
            average_number_of_animals_per_enclosure = 'No Animals in enclosures'
        animals_from_different_species = 0
        # Number of enclosures with animals form multiple species
        for enclosure in self.enclosures:
            animal_in_enclosure = []
            for animal in enclosure.animals:
                animal_in_enclosure.append(animal.species)
            if len(set(animal_in_enclosure)) != 1:
                animals_from_different_species += 1
        # available space per animal in enclosure
        available_space_in_enclosure = {}
        if self.enclosures:
            for enclosure in self.enclosures:
                if len(enclosure.animals) > 0:
                    available_space_in_enclosure[f'{enclosure.enclosure_id}'] = f'{(enclosure.area / len(enclosure.animals))} m²'
                else:
                    available_space_in_enclosure[f'{enclosure.enclosure_id}'] = 'No Animals'
        else:
            available_space_in_enclosure = 'No Enclosures detected'
        return {'Animals per species': animal_per_specie,
                'Average number of animals per enclosure': average_number_of_animals_per_enclosure,
                'Animals from different species in the same enclosure': animals_from_different_species,
                'Available space per animal in enclosure': available_space_in_enclosure}

    # All functions that are related to enclosures

    def add_enclosure(self, enclosure):
        self.enclosures.append(enclosure)

    def remove_enclosure(self, enclosure):
        self.enclosures.remove(enclosure)
        if not self.enclosures:
            for animal in enclosure.animals:
                animal.enclosure = None
        else:
            for animal in enclosure.animals:
                new_enclosure = random.choice(self.enclosures)
                animal.enclosure = new_enclosure.enclosure_id
                new_enclosure.animals.append(animal)

    def get_enclosure(self, enclosure_id):
        for enclosure in self.enclosures:
            if enclosure.enclosure_id == enclosure_id:
                return enclosure

    # All functions that are related to caretakers

    def add_caretaker(self, caretaker):
        self.caretakers.append(caretaker)

    def remove_caretaker(self, caretaker):
        self.caretakers.remove(caretaker)
        for animal in caretaker.animals:
            if not self.caretakers:
                animal.caretaker = None
            else:
                new_caretaker = random.choice(self.caretakers)
                animal.caretaker = new_caretaker.caretaker_id
                new_caretaker.animals.append(animal)

    def get_caretaker(self, caretaker_id):
        for caretaker in self.caretakers:
            if caretaker.caretaker_id == caretaker_id:
                return caretaker

    def caretakers_statistics(self):
        animals_per_worker = []
        if not self.caretakers:
            return 'No caretakers detected'
        for caretaker in self.caretakers:
            animals_per_worker.append(len(caretaker.animals))
        lazy_ass = min(animals_per_worker)
        average_dude = sum(animals_per_worker) / len(animals_per_worker)
        hard_worker = max(animals_per_worker)
        return {'minimum': lazy_ass, 'average': average_dude, 'maximum': hard_worker}
# TASKS

    def cleaning(self):
        cleaning_plan = {}
        for enclosure in self.enclosures:
            person = random.randrange(0, len(self.caretakers))
            if len(enclosure.cleaning_record) > 0:
                last_one = enclosure.cleaning_records[-1]
                month = last_one.month
                day = last_one.day
                month_more = int(month)
                if day < (31 - 3):
                    future_day = day + 3
                else:
                    month_more += 1
                    future_day = 3 - (31 - day)
                cleaning_plan[enclosure.enclosure_id] = f"Clean the enclosure on {future_day}/{month_more}. Responsible person {self.caretakers[person].name}"
            else:
                cleaning_plan[enclosure.enclosure_id] = f"Clean right NOW!!! Responsible person {self.caretakers[person].name}"
        return cleaning_plan

    def medical(self):
        medical_plan = {}
        for animal in self.animals:
            if len(animal.medical_record) > 0:
                last_one = animal.medical_record[-1]
                month = last_one.month
                day = last_one.day
                month_more = int(month) + 1
                if day < 31:
                    future_day = day + 7
                else:
                    month_more += 1
                    future_day = 7 - (31 - day)

                medical_plan[animal.animal_id] = f"Check the animal on {future_day}/{month_more}."
            else:
                medical_plan[animal.animal_id] = f"Check animal health right NOW!!!"
        return medical_plan

    def feeding(self):
        feeding_plan = {}
        for animal in self.animals:
            try:
                caretaker = self.get_caretaker(animal.caretaker)
            except ValueError:
                caretaker = self.caretakers[random.randrange(0, len(self.caretakers))]
            if len(animal.feeding_record) > 0:
                last_one = animal.feeding_record[-1]
                month = last_one.month
                day = last_one.day
                month_more = int(month)
                if day < (31 - 2):
                    future_day = day + 2
                else:
                    month_more += 2
                    future_day = 2 - (31 - day)
                feeding_plan[animal.animal_id] = f"Feed the animal on {future_day}/{month_more}. Responsible person {caretaker.name}"
            else:
                feeding_plan[animal.animal_id] = f"Feed the animal right NOW!!! Responsible person {caretaker.name}"
        return feeding_plan
