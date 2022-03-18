import uuid
import datetime


class Enclosure:

    def __init__(self, name, area):
        self.enclosure_id = str(uuid.uuid4())
        self.name = name
        self.area = area
        self.animals = []
        self.cleaning_record = []

    def clean(self):
        self.cleaning_record.append(datetime.datetime.now())
