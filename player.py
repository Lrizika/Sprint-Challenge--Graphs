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

	def _find_nearest_unvisited(
			self,
			visited,
			seed=None,
			seed_weight=0,
			diff_threshold=2,
			diff_weight=0.3,
			# locality_radius=1,
			locality_weight=0.5,
	):
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

				# START HEURISTICS BLOCK
				direction_weights = {
					direction: 0 for direction in Direction
				}

				# Random seed heuristic
				if seed_weight:
					for direction in direction_weights:
						direction_weights[direction] += random.random() * seed_weight

				# Distance from start heuristic
				# Encourages areas further from start
				if diff_weight:
					diff_max = max(abs(x_diff), abs(y_diff))
					if diff_max != 0:
						x_rel = abs(x_diff) / diff_max
						y_rel = abs(y_diff) / diff_max
						if x_diff > diff_threshold:
							direction_weights[Direction.e] += diff_weight * x_rel
						if x_diff < -diff_threshold:
							direction_weights[Direction.w] += diff_weight * x_rel
						if y_diff > diff_threshold:
							direction_weights[Direction.n] += diff_weight * y_rel
						if y_diff < -diff_threshold:
							direction_weights[Direction.s] += diff_weight * y_rel

				# Locality heuristic
				# Encourages areas with fewer undiscovered nodes
				if locality_weight:
					locality_scores = {}
					for direction in Direction:
						locality_scores[direction] = 0
						room = current_path[-1].get_room_in_direction(direction.name)
						if room is not None:
							for d2 in Direction:
								if d2 == direction.opposite():
									continue
								r2 = room.get_room_in_direction(d2.name)
								if r2 is None:
									locality_scores[direction] += 1
					max_score = float(max(locality_scores.values()))
					for direction in Direction:
						if locality_scores[direction]:
							direction_weights[direction] += \
								locality_scores[direction] / \
								max_score * \
								locality_weight



				# Deprecated: edges priority heuristic
				# for i in range(len(Direction)):
				# 	direction = starting_direction.offset(i)
				# 	room = current_path[-1].get_room_in_direction(direction.name)
				# 	if room is not None:
				# 		starting_direction = direction
				# 		break

				# END HEURISTICS BLOCK
				# print(direction_weights)
				for direction in sorted(
						direction_weights, key=direction_weights.get, reverse=True
				):
					room = current_path[-1].get_room_in_direction(direction.name)
					if room is not None:
						to_visit.appendleft(current_path + [room])
						routes.appendleft(current_route + [direction.name])

				# for i in range(len(Direction)):
				# 	direction = starting_direction.offset(i)

	def traverse(self, num_rooms=499, **kwargs):
		visited = set()
		route = []
		while len(visited) < num_rooms:
			visited.add(self.current_room)
			new_route = self._find_nearest_unvisited(visited, **kwargs)
			route.extend(new_route)
			for direction in new_route:
				self.travel(direction)
		return route

