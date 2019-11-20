from django.contrib.auth.models import User
from adventure.models import Player, Room
import pdb
import secrets

class CreateWorld:
    def __init__(self, num_rooms):
        self.num_rooms = num_rooms
        self.grid_view = {}

        self.create_rooms()

    def place_maze_with_validation(self, rooms_created, prev_room, home, home_start, x, y):
        # print(f"\nSTART ROOM CREATION")
        if home == None:
            # print(f"\nSET HOME")
            room = Room(rooms_created, f"This is room {rooms_created}", f"This is a generic room called {rooms_created}.", x, y)
            room.save()
            self.grid_view[(x,y)] = room.id
            return {"prev_room": room}

        rm_dir = ["n", "e", "w", "s"]
        rvrm_dir = ["s", "w", "e", "n"]
        ran = secrets.randbelow(4)
        check_dir = rm_dir[ran]
        rvcheck_dir = rvrm_dir[ran]
        dir_values = {"n":1, "e":1, "w":-1, "s":-1}

        if check_dir == "n" or check_dir == "s":
            y += dir_values[check_dir]
        elif check_dir == "e" or check_dir == "w":
            x += dir_values[check_dir]
            
        if home_start and getattr(home, f"{check_dir}_to", 0) == 0:
            # print(f"\nSTART FROM HOME")
            room = Room(rooms_created, f"This is room {rooms_created}", f"This is a generic room called {rooms_created}.", x, y)
            room.save()
            home.connectRooms(room, check_dir)
            room.connectRooms(home, rvcheck_dir)
            self.grid_view[(x,y)] = room.id
        elif getattr(prev_room, f"{check_dir}_to", 0) == 0:
            # print(f"\nROOM DIRECTION EMPTY")
            if (x,y) in self.grid_view:
                # print(f"\nROOM EXISTS SO CANNOT PLACE")
                rm_id = self.grid_view[(x,y)]
                nxt_rm = Room.objects.filter(id=rm_id)[0]
                return self.place_maze_with_validation(rooms_created, nxt_rm, home, False, x, y)
            else:
                # print(f"\nPLACE ROOM AT DIRECTION")
                room = Room(rooms_created, f"This is room {rooms_created}", f"This is a generic room called {rooms_created}.", x, y)
                room.save()
                prev_room.connectRooms(room, check_dir)
                room.connectRooms(prev_room, rvcheck_dir)
                self.grid_view[(x,y)] = room.id
        else:
            # print(f"\nROOM EXISTS")
            rm_id = getattr(prev_room, f"{check_dir}_to", 0)
            # print(f"\nROOM: {prev_room.id} | DIRECTIONAL ROOM ID: {rm_id}")
            # pdb.set_trace()
            nxt_rm = Room.objects.filter(id=rm_id)[0]
            # pdb.set_trace()
            return self.place_maze_with_validation(rooms_created, nxt_rm, home, False, x, y)
        return {"prev_room":room}


    def create_rooms(self):
        Room.objects.all().delete()

        rooms_to_create = self.num_rooms
        prev_room = None
        home = None
        rooms_created = 1
        while rooms_to_create >= rooms_created:
            # print(f"\n~~~~~~~~~~\nWHILE START room: {rooms_created}\n")
            returned_vals = self.place_maze_with_validation(rooms_created, prev_room, home, True, 0, 0)
            prev_room = returned_vals["prev_room"]
            if rooms_created == 1:
                home = prev_room
            rooms_created += 1
            # print(f"\nWHILE END\n~~~~~~~~~~\n")