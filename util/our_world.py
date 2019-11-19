from django.contrib.auth.models import User
from adventure.models import Player, Room
import pdb

class CreateWorld:
    def __init__(self, num_rooms):
        self.num_rooms = num_rooms

        self.create_rooms()

    def create_rooms(self):
        rooms_to_create = self.num_rooms
        prev_room = None
        rooms_created = 0
        # pdb.set_trace()
        while rooms_to_create >= rooms_created:
            # pdb.set_trace()
            room = Room(rooms_created, "A Generic Room", "This is a generic room.")
            if prev_room != None:
                # print(f'CREATE CONNECTIONS FOR ROOM | PREV_ROOM: {prev_room.id}')
                room.s_to = int(prev_room.id)
                prev_room.n_to = rooms_created
                prev_room.save()
                room.save()
            prev_room = room
            # print(f"rooms_created: {rooms_created} | room id: {room.id} | prev_room: {prev_room}")
            rooms_created += 1
        # print('\n\n\n~~~~END OF THE LINE~~~\n\n\n')