from django.contrib.auth.models import User
from adventure.models import Player, Room
import pdb
import secrets

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

    def place_maze(self, rooms_created, prev_room, home, home_start):
        if home == None:
            # print("\n~~~~~~~~~~~~\nHOME NONE\n~~~~~~~~~~~~~\n")
            room = Room(rooms_created, "A Generic Room", "This is a generic room.")
            room.save()
            return {"rooms_created": rooms_created, "prev_room": room}

        rm_dir = ["n", "e", "w", "s"]
        rvrm_dir = ["s", "w", "e", "n"]
        ran = secrets.randbelow(4)
        # print(f"\nRandom Number: {ran}\n")
        check_dir = rm_dir[ran]
        rvcheck_dir = rvrm_dir[ran]
        # print(f"CHECK_DIR: {check_dir} | RVCHECK_DIR: {rvcheck_dir}")
        # print(f"GETATTR: {getattr(prev_room, '{check_dir}_to', 0)}")
        if home_start and getattr(home, f"{check_dir}_to", 0) == 0:
            # print("add room to HOME dir")
            room = Room(rooms_created, "A Generic Room", "This is a generic room.")
            setattr(home, f"{check_dir}_to", room.id)
            setattr(room, f"{rvcheck_dir}_to", home.id)
            room.save()
            home.save()
        elif getattr(prev_room, f"{check_dir}_to", 0) == 0:
            # print("add room to dir")
            room = Room(rooms_created, "A Generic Room", "This is a generic room.")
            setattr(prev_room, f"{check_dir}_to", room.id)
            setattr(room, f"{rvcheck_dir}_to", prev_room.id)
            prev_room.save()
            room.save()
        else:
            # print("traverse to next room")
            rm_id = getattr(prev_room, f"{check_dir}_to", 0)
            nxt_rm = Room.objects.filter(id=rm_id)[0]
            # print(f"nxt_rm: {nxt_rm}")
            return self.place_maze(rooms_created, nxt_rm, home, False)
        return {"rooms_created": rooms_created, "prev_room":room}


    def create_rooms(self):
        Room.objects.all().delete()

        rooms_to_create = self.num_rooms
        prev_room = None
        home = None
        rooms_created = 1
        # pdb.set_trace()
        while rooms_to_create >= rooms_created:
            print(f"ROOMS CREATED: {rooms_created}")
            # returned_vals = self.place_room(rooms_created, prev_room)
            returned_vals = self.place_maze(rooms_created, prev_room, home, True)
            rooms_created = returned_vals["rooms_created"]
            prev_room = returned_vals["prev_room"]
            if rooms_created == 1:
                home = prev_room
            print(f"\n\n~~~~~~~~~~\n\nprev_room: {prev_room} | home: {home}\n\n~~~~~~~~~~\n\n")
            rooms_created += 1