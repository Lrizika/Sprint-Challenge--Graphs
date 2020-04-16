from enum import IntEnum
from collections import deque


class Direction(IntEnum):
	n = 0
	e = 1
	s = 2
	w = 3

	def offset(self, amount):
		return self.__class__((self + amount) % 4)

	def right(self):
		return self.offset(1)

	def left(self):
		return self.offset(-1)

	def opposite(self):
		return self.offset(2)


class Player:
	def __init__(self, starting_room):
		self.current_room = starting_room

	def travel(self, direction, show_rooms=False):
		next_room = self.current_room.get_room_in_direction(direction)
		if next_room is not None:
			self.current_room = next_room
			if (show_rooms):
				next_room.print_room_description(self)
		else:
			print("You cannot move in that direction.")

	def _find_nearest_unvisited(self, visited):
		search_visited = set()
		to_visit = deque()
		to_visit.append([self.current_room])
		routes = deque()
		routes.append([])
		while len(to_visit):
			current_path = to_visit.pop()
			current_route = routes.pop()
			if current_path[-1] not in visited:
				return current_route
			elif current_path[-1] in search_visited:
				continue
			else:
				search_visited.add(current_path[-1])
				for direction in Direction:
					direction = direction.offset(2)
					room = current_path[-1].get_room_in_direction(direction.name)
					if room is not None:
						to_visit.appendleft(current_path + [room])
						routes.appendleft(current_route + [direction.name])

	def traverse(self, num_rooms=499):
		visited = set()
		route = []
		while len(visited) < num_rooms:
			visited.add(self.current_room)
			new_route = self._find_nearest_unvisited(visited)
			route.extend(new_route)
			for direction in new_route:
				self.travel(direction)
		return route

