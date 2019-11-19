from django.contrib.auth.models import User
from adventure.models import Player, Room
import pdb

class CreateWorld:
    def __init__(self, num_rooms):
        self.num_rooms = num_rooms

        self.create_rooms()

    def place_room(self, rooms_created, prev_room):
        # pdb.set_trace()
        room = Room(rooms_created, "A Generic Room", "This is a generic room.")
        if prev_room != None:
            room.s_to = int(prev_room.id)
            prev_room.n_to = rooms_created
            prev_room.save()
            room.save()
        prev_room = room
        room.save()
        rooms_created += 1
        return {"rooms_created": rooms_created, "prev_room":prev_room}


    def create_rooms(self):
        Room.objects.all().delete()

        rooms_to_create = self.num_rooms
        prev_room = None
        rooms_created = 1
        # pdb.set_trace()
        while rooms_to_create >= rooms_created:
            returned_vals = self.place_room(rooms_created, prev_room)
            rooms_created = returned_vals["rooms_created"]
            prev_room = returned_vals["prev_room"]