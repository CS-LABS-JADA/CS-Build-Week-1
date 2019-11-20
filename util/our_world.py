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
        if home == None:
            room = Room(rooms_created, f"This is room {rooms_created}", f"This is a generic room called {rooms_created}.")
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
            room = Room(rooms_created, f"This is room {rooms_created}", f"This is a generic room called {rooms_created}.")
            room.save()
            home.connectRooms(room, check_dir)
            room.connectRooms(home, rvcheck_dir)
            self.grid_view[(x,y)] = room.id
        elif getattr(prev_room, f"{check_dir}_to", 0) == 0:
            if (x,y) in self.grid_view:
                rm_id = self.grid_view[(x,y)]
                nxt_rm = Room.objects.filter(id=rm_id)[0]
                return self.place_maze_with_validation(rooms_created, nxt_rm, home, False, x, y)
            else:
                room = Room(rooms_created, f"This is room {rooms_created}", f"This is a generic room called {rooms_created}.")
                room.save()
                prev_room.connectRooms(room, check_dir)
                room.connectRooms(prev_room, rvcheck_dir)
                self.grid_view[(x,y)] = room.id
        else:
            rm_id = getattr(prev_room, f"{check_dir}_to", 0)
            nxt_rm = Room.objects.filter(id=rm_id)[0]
            return self.place_maze_with_validation(rooms_created, nxt_rm, home, False, x, y)
        return {"prev_room":room}


    def create_rooms(self):
        Room.objects.all().delete()

        rooms_to_create = self.num_rooms
        prev_room = None
        home = None
        rooms_created = 1
        while rooms_to_create >= rooms_created:
            returned_vals = self.place_maze_with_validation(rooms_created, prev_room, home, True, 0, 0)
            prev_room = returned_vals["prev_room"]
            if rooms_created == 1:
                home = prev_room
            rooms_created += 1