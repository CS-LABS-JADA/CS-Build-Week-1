from django.contrib.auth.models import User
from adventure.models import Player, Room
import pdb
import secrets

class CreateWorld:
    def __init__(self, num_rooms):
        self.num_rooms = num_rooms
        self.open_spaces = []
        self.grid_view = {}

        self.create_rooms()
    
    def get_edges(self, room):
        # print(f"ROOM: {room.id}")
        if getattr(room, f"n_to", 0) == 0:
            self.open_spaces.append((room.id, "n"))
        if getattr(room, f"e_to", 0) == 0:
            self.open_spaces.append((room.id, "e"))
        if getattr(room, f"s_to", 0) == 0:
            self.open_spaces.append((room.id, "s"))
        if getattr(room, f"w_to", 0) == 0:
            self.open_spaces.append((room.id, "w"))

    def place_maze_with_validation(self, rooms_created):
        x=0; y=0
        if rooms_created == 1:
            room = Room(rooms_created, f"This is room {rooms_created}", f"This is a generic room called {rooms_created}.", x, y)
            room.save()
            self.get_edges(room)
            self.grid_view[(x,y)] = True
            return
        
        max = len(self.open_spaces)
        rand = secrets.randbelow(max)
        rev_dir = {"n":"s", "e":"w", "s":"n", "w":"e"}
        dir_val = {"n":1, "e":1, "s":-1, "w":-1}
        if self.open_spaces[rand] is not None:
            rm_id = self.open_spaces[rand][0]
            curr_rm = Room.objects.filter(id=rm_id)[0]
            rm_dir = self.open_spaces[rand][1]
            x = getattr(curr_rm, "x", 0)
            y = getattr(curr_rm, "y", 0)
            if rm_dir == "n" or rm_dir == "s":
                y += dir_val[rm_dir]
            if rm_dir == "w" or rm_dir == "e":
                x += dir_val[rm_dir]
            if (x,y) in self.grid_view:
                # print("can't place recurse")
                del self.open_spaces[rand]
                self.place_maze_with_validation(rooms_created)
            else:
                # print("place in space")
                room = Room(rooms_created, f"This is room {rooms_created}", f"This is a generic room called {rooms_created}.", x, y)
                room.save()
                rev_rm_dir = rev_dir[self.open_spaces[rand][1]]
                curr_rm.connectRooms(room, rm_dir)
                room.connectRooms(curr_rm, rev_rm_dir)
                del self.open_spaces[rand]
                self.get_edges(room)
        else:
            self.place_maze_with_validation(rooms_created)


    def create_rooms(self):
        Room.objects.all().delete()

        rooms_to_create = self.num_rooms
        rooms_created = 1
        while rooms_to_create >= rooms_created:
            # print(f"\n~~~~~~~~~~\nWHILE START room: {rooms_created}\n")
            self.place_maze_with_validation(rooms_created)
            rooms_created += 1
            # print(f"self.open_spaces: {self.open_spaces}")
            # print(f"\nWHILE END\n~~~~~~~~~~\n")