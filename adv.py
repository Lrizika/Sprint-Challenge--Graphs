#!/usr/bin/env python

from room import Room
from player import Player
from world import World

import random
from ast import literal_eval

# Load world
world = World()


# You may uncomment the smaller graphs for development and testing purposes.
# map_file = "maps/test_line.txt"
# map_file = "maps/test_cross.txt"
# map_file = "maps/test_loop.txt"
# map_file = "maps/test_loop_fork.txt"
map_file = "maps/main_maze.txt"

# Loads the map into a dictionary
room_graph=literal_eval(open(map_file, "r").read())
world.load_graph(room_graph)

# Print an ASCII map
# world.print_rooms()


# print(player._find_nearest_unvisited(set()))
# traversal_path = player.build_traversal()
player = Player(world.starting_room)
best_path = player.traverse()
print(f'Starting best length: {len(best_path)}')
for diff_threshold in range(5):
	print(f'Tuning on diff_threshold: {diff_threshold}')
	for seed in range(20):
		player = Player(world.starting_room)
		traversal_path = player.traverse(
			seed=seed,
			seed_weight=0.05,
			diff_threshold=diff_threshold,
			diff_weight=0.2,
			# locality_radius=1,
			locality_weight=0.4,
		)
		# print(len(traversal_path))
		if len(traversal_path) < len(best_path):
			print(f'New best path - diff_threshold {diff_threshold}, seed {seed}, length: {len(traversal_path)}')
			best_path = traversal_path
traversal_path = best_path
# Fill this out with directions to walk
# traversal_path = ['n', 'n']



# TRAVERSAL TEST
visited_rooms = set()
player.current_room = world.starting_room
visited_rooms.add(player.current_room)

for move in traversal_path:
	player.travel(move)
	visited_rooms.add(player.current_room)

if len(visited_rooms) == len(room_graph):
	print(f"TESTS PASSED: {len(traversal_path)} moves, {len(visited_rooms)} rooms visited")
else:
	print("TESTS FAILED: INCOMPLETE TRAVERSAL")
	print(f"{len(room_graph) - len(visited_rooms)} unvisited rooms")



#######
# UNCOMMENT TO WALK AROUND
#######
player.current_room.print_room_description(player)
while True:
	cmds = input("-> ").lower().split(" ")
	if cmds[0] in ["n", "s", "e", "w"]:
		player.travel(cmds[0], True)
	elif cmds[0] == "q":
		break
	else:
		print("I did not understand that command.")
