# python packages
import random
# internal packages
from block import *

class Maze():
	def __init__(self, length, height):
		self.length = length
		self.height = height
		self.maze = [None] * length * height
		# set up the maze
		self.generate_maze()

	def __repr__(self):
		string_length = self.length + 1
		string_height = self.height + 1
		string_maze = [None] * string_length * string_height
		
		amaze = ''
		for location, character in enumerate(string_maze):
			# get initial index
			nw = location - string_length - 1
			ne = location - string_length
			sw = location - 1
			se = location
			# recalibrate to 'true self' indices
			nw = nw - (nw // (string_length))  - 1
			ne = ne - (ne // (string_length))  - 1
			sw = sw - (sw // (string_length))  - 1
			se = se - (se // (string_length))  - 1

			# this happens when quad is on a western boundary.
			west = sw == se
			# this happens when quad is on a eastern boundary.
			east = nw == ne
			# this happens when quad is on a northern boundary.
			north = nw < 0 or ne < 0
			# this happens when quad is on a southern boundary.
			south = sw >= len(self.maze) - 1 or se >= len(self.maze) - 1

			print(se)


			# 00 01 02 02
			# 03 04 05 05
			# 06 07 08 08
			# 09 10 11 11
			# 12 13 14 14
			

			# check if quad is on the boundary
			if west:
				nw = None
				sw = None

			# check if quad is on the boundary
			if east:
				ne = None
				se = None

			# check if quad is on the boundary
			if north:
				nw = None
				ne = None

			# check if quad is on the boundary
			if south:
				sw = None
				se = None

			# print(
			# 	'---\n'
			# 	f'nw {nw}\n'
			# 	f'ne {ne}\n'
			# 	f'sw {sw}\n'
			# 	f'se {se}\n\n'
			# 	f'north {north}\n'
			# 	f'south {south}\n'
			# 	f'east  {east}\n'
			# 	f'west  {west}\n'
			# )

			if not (west or north or south) and (nw and sw):
				# grab quad nodes neighbors.
				north_item = self.maze[sw].neighbors['north']
				south_item = self.maze[nw].neighbors['south']
				# affirm whether they share an edge.
				north_bool = south_item == self.maze[sw]
				south_bool = north_item == self.maze[nw]
				# update variable if they do.
				if north_bool and south_bool:
					west = True

			if not (east or north or south) and (ne and se):
				# grab quad nodes neighbors.
				north_item = self.maze[se].neighbors['north']
				south_item = self.maze[ne].neighbors['south']
				# affirm whether they share an edge.
				north_bool = north_item == self.maze[ne]
				south_bool = south_item == self.maze[se]
				# update variable if they do.
				if north_bool and south_bool:
					east = True

			if not (north or east or west) and (nw and ne):
				# grab quad nodes neighbors.
				east_item = self.maze[ne].neighbors['east']
				west_item = self.maze[nw].neighbors['west']
				# affirm whether they share an edge.
				east_bool = east_item == self.maze[ne]
				west_bool = west_item == self.maze[nw]
				# update variable if they do.
				if east_bool and west_bool:
					north = True

			if not (south or east or west) and (sw and se):
				# grab quad nodes neighbors.
				east_item = self.maze[se].neighbors['east']
				west_item = self.maze[sw].neighbors['west']
				# affirm whether they share an edge.
				east_bool = east_item == self.maze[se]
				west_bool = west_item == self.maze[sw]
				# update variable if they do.
				if east_bool and west_bool:
					south = True

			glyph = get_glyph(north, south, east, west)
			if location % string_length == 0:
				amaze += '\n'
			amaze += glyph
			print(amaze)



		return 'WiP'

	def get_block(self, row_id, column_id):
		'''
		returns the cell located at given coordinates.
		'''
		location = row_id * self.height + column_id
		block = self.maze[location]
		return block

	def get_row(self, row_id):
		'''
		returns the nth full row.
		'''
		east = row_id * self.height
		west = east + self.length
		row = self.maze[east:west]
		return row

	def get_column(self, column_id):
		'''
		returns the nth full column.
		'''
		num_columns = self.length
		column = self.maze[column_id::num_columns]
		return column

	def get_each_row(self):
		'''
		returns an array arrays; a list of every row.
		'''
		each_row = []
		for row_id in range(0, self.height):
			each_row.append(self.get_row(row_id))
		return each_row

	def get_each_column(self):
		'''
		returns an array arrays; a list of every column.
		'''
		each_column = []
		for column_id in range(0, self.length):
			each_column.append(self.get_column(column_id))
		return each_column

	def generate_maze(self, loc = None):
		'''
		generates a perfect maze.
		its done recursively via a depth-first traversal tree.
		this is a setter function; it does not return anything.
		---
		key = cardinal direction
		rev = reversed cardinal direction
		loc = root location
		nbr = neighbor location
		'''
		if loc is None:
			# start the trees loc at a random point in the maze.
			# this doesnt infer a start/exit in the finished maze.
			# one can always find a path from any point A to B;
			# the program will decide these points later.
			loc = random.randint(0, len(self.maze) - 1)
			# note our visited list exists as the maze property.

		# first, fill the maze spot with an empty block.
		self.maze[loc] = Block()

		# grab the location id from each cardinal direction.
		neighbor_locations = {
			'north': loc - self.length,
			'south': loc + self.length,
			'east': loc - 1,
			'west': loc + 1,
		}

		# this is useful for doubly-linked vertices.
		reverse_compass = {
			'north': 'south',
			'south': 'north',
			'east': 'west',
			'west': 'east',
		}

		# validate will remove indices that are out-of-bounds.
		def validate(location):
			if len(self.maze) > location >= 0:
				return location
			else:
				return None

		# update neighbors with validate.
		for key, nbr in neighbor_locations.items():
			# it is safe to update a key's value in a loop;
			# it isnt safe to update a key in a loop.
			neighbor_locations[key] = validate(nbr)

		for key, nbr in neighbor_locations.items():
			# rev reverses key, a cardinal direction.
			rev = reverse_compass[key]
			# nbr is empty, representing a maze boundary.
			if nbr is None:
				self.maze[loc].neighbors[key] = None
				pass

			# nbr is an int, representing a spot in maze.
			else:
				# this spot is empty! fill it up!
				if self.maze[nbr] is None:
					# generate a new maze block.
					self.generate_maze(nbr)
					# link up the net / graph / tree.
					self.maze[loc].neighbors[key] = self.maze[nbr]
					self.maze[nbr].neighbors[rev] = self.maze[loc]

				# this spot is filled.
				else:
					pass


def get_glyph(north, south, east, west):
	'''
	this function returns a maze drawing character.
	'''
	# == FIXME ==
	# this function is awkwardly large.
	# not sure where to put it semantically.
	# == TODO ==
	# these unicode characters must be converted!
	# like emojis, its a code smell to have them.

	# four passages
	if north and south and east and west:
		glyph = ' '
	# three passages
	elif south and east and west and not (north):
		glyph = '╵'
	elif north and east and west and not (south):
		glyph = '╷'
	elif north and south and west and not (east):
		glyph = '╶'
	elif north and south and east and not (west):
		glyph = '╴'
	# two passages
	elif north and south and not (east or west):
		glyph = '─'
	elif north and east and not (south or west):
		glyph = '┐'
	elif north and west and not (south or east):
		glyph = '┌'
	elif south and east and not (north or west):
		glyph = '┘'
	elif south and west and not (north or east):
		glyph = '└'
	elif east and west and not (north or south):
		glyph = '│'
	# one passage
	elif north and not (south or east or west):
		glyph = '┬'
	elif south and not (north or east or west):
		glyph = '┴'
	elif east and not (north or south or west):
		glyph = '┤'
	elif west and not (north or south or east):
		glyph = '├'
	# zero passages
	elif not (north or south or east or west):
		glyph = '┼'

	return glyph