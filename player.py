from enum import IntEnum
from collections import deque
import random


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
		self.starting_x = starting_room.x
		self.starting_y = starting_room.y

	def travel(self, direction, show_rooms=False):
		next_room = self.current_room.get_room_in_direction(direction)
		if next_room is not None:
			self.current_room = next_room
			if (show_rooms):
				next_room.print_room_description(self)
		else:
			print("You cannot move in that direction.")

	def _find_nearest_unvisited(self, visited, seed=None, diff_threshold=2):
		if seed is not None:
			random.seed(seed)
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

				x_diff = self.current_room.x - self.starting_x
				y_diff = self.current_room.y - self.starting_y
				if seed is not None:
					starting_direction = Direction(random.randint(0, 3))
				else:
					starting_direction = Direction.n

				if x_diff > 0 and abs(x_diff) - abs(y_diff) > diff_threshold:
					starting_direction = Direction.e
				elif x_diff < 0 and abs(x_diff) - abs(y_diff) > diff_threshold:
					starting_direction = Direction.w
				elif y_diff > 0 and abs(y_diff) - abs(x_diff) > diff_threshold:
					starting_direction = Direction.n
				elif y_diff < 0 and abs(y_diff) - abs(x_diff) > diff_threshold:
					starting_direction = Direction.s

				for i in range(len(Direction)):
					direction = starting_direction.offset(i)
					room = current_path[-1].get_room_in_direction(direction.name)
					if room is not None:
						starting_direction = direction
						break

				for i in range(len(Direction)):
					direction = starting_direction.offset(i)
					room = current_path[-1].get_room_in_direction(direction.name)
					if room is not None:
						to_visit.appendleft(current_path + [room])
						routes.appendleft(current_route + [direction.name])

	def traverse(self, num_rooms=499, seed=None, diff_threshold=2):
		visited = set()
		route = []
		while len(visited) < num_rooms:
			visited.add(self.current_room)
			new_route = self._find_nearest_unvisited(visited, seed=seed, diff_threshold=diff_threshold)
			route.extend(new_route)
			for direction in new_route:
				self.travel(direction)
		return route

