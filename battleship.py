import sys
'''
File: battleship.py
Author: Jason Fukumoto, 23445294
Purpose: The purpose of this program is to use classes to create a 10
x10 grid of objects and use two files: one to place ships on the grid,
and the other to determine if any of those ships have been hit.
'''
SHIP_SIZE = {'A': 5, 'B': 4, 'S': 3, 'D': 3, 'P': 2} #Global dictionary
TOTAL_SHIP = SHIP_SIZE['A'] + SHIP_SIZE['B'] + SHIP_SIZE['S'] + SHIP_SIZE[
    'D'] + SHIP_SIZE['P'] #Sums up the total sizes of each ship
SIZE = 10 #Size of the grid 10x10
P_SHIP = 0 #Index of ship of placement file
P_X1 = 1 #Index of x1 in placement file
P_Y1 = 2 #Index of y1 in placement file
P_X2 = 3 #Index of x2 in placement file
P_Y2 = 4 #Index of y2 in placement file
G_X = 0 #Index of x in guess file
G_Y = 1 #Index of y in guess file

'''
An instance of this class describes a grid position. Ship attribute is None,
initially grid is empty. Guess attribute is False initially, no guess yet.
Have setters and getters for the ship and guess attributes. Sets to True if 
guessed, and sets to a ship for position file.
'''
class GridPos:
    def __init__(self, x, y):
        self._x = x
        self._y = y
        self._ship = None
        self._guess = False

    def add_ship(self, ship):  # Used to change ship type to place on grid
        self._ship = ship

    def add_guess(self):  # Checks if the position has been guessed.
        self._guess = True

    def get_guess(self): # Checks if guess is true/false
        return self._guess

    def get_ship(self):  # Checks to see if a ship or None
        return self._ship

    def get_typeship(self):
        if self._ship is None:
            return 'N'
        return self._ship.get_shiptype()

    def __str__(self):  # For printing out grid, changes None to 'N'
        if self._ship is None:
            return 'N'
        return self._ship.get_shiptype()

'''
An instance of this class describes a board with placement of ships.
Attribute that creates a 10x10 grid. Can be changed by the global SIZE. An
attribute that has a sum of all the size of the ship to know when all the ships
have been hit. Methods that fill the board and process the guesses.
'''
class Board:
    def __init__(self): #Appends a GridPos object at every position of the grid
        self._grid = []
        for i in range(SIZE):
            inner = []
            for j in range(SIZE):
                inner.append(GridPos(i, j))
            self._grid.append(inner)
        self._totalship = TOTAL_SHIP #Sum of all the sizes of the ships

    '''
    Creates a ship instance and that gets passed in strings and integers to 
    add ship objects at each gridpos object. Has checks to see if invalid 
    placement and prints out errors.
    '''
    def fill_board(self, line):
        invalid = ' '.join(line) #Joins the line into a string to print error
        ship = line[P_SHIP] #Ship name
        x1 = int(line[P_X1]) #x1 coordinate as an integer
        x2 = int(line[P_X2]) #y1 coordinate as an integer
        y1 = int(line[P_Y1]) #x2 coordinate as an integer
        y2 = int(line[P_Y2]) #y2 coordinate as an integer
        s = Ship(ship, x1, y1, x2, y2) #Creates ship instance variable
        if x1 != x2 and y1 != y2: #Checks horiztonal errors
            print('ERROR: ship not horizontal or vertical: ' + invalid + '\n')
            sys.exit(1)
        elif x1 == x2:
            yparse = [int(y1), int(y2)] #Creates a list with y-coordinates
            ymax = max(yparse) #Gets a max
            ymin = min(yparse) #Gets a min
            difference = (ymax - ymin) + 1 #Difference of the max and min
            for i in range(difference): #Loops the size of the ship
                grid_obj = self._grid[i + ymin][x1] #variable for each object
                if grid_obj.get_ship() != None: #Checks if ships exist
                    print('ERROR: overlapping ship: ' + invalid + '\n')
                    sys.exit(1)
                grid_obj.add_ship(s) #Adds ship object to gridpos object
        elif y1 == y2:
            xparse = [int(x1), int(x2)]
            xmax = max(xparse)
            xmin = min(xparse)
            difference = (xmax - xmin) + 1
            for i in range(difference):
                grid_obj = self._grid[y1][i + xmin]
                if grid_obj.get_ship() != None:
                    print('ERROR: overlapping ship: ' + invalid + '\n')
                    sys.exit(1)
                grid_obj.add_ship(s)
    '''
    Processes the guess file to print out if a ship has been hit, missed, 
    illegal guess, ship sunk, and ends game. If the position has been guessed, 
    will get the gridpos object and changed it to True. 
    '''
    def process_guesses(self, guess_line):
        x = int(guess_line[G_X]) #x coordinate of guess file
        y = int(guess_line[G_Y]) #y coordinate of guess file
        if (0 <= x < SIZE) and (0 <= y < SIZE): #Checks bounds
            grid_obj = self.get_gridpos(x, y) #GridPos object
            if grid_obj.get_typeship() not in SHIP_SIZE: #Not a ship
                if grid_obj.get_guess(): #If true, has been guessed
                    print('miss (again)')
                else:                    #Hasn't been hit
                    grid_obj.add_guess() #Changed to True
                    print('miss')
            else:                       #Is a ship
                if grid_obj.get_guess(): #Checks if its been guessed
                    print('hit (again)')
                else:                    #Has not been guessed
                    if grid_obj.get_ship().get_sunk() == 1:
                        print(grid_obj.get_ship().get_shiptype() + ' sunk')
                    else:                #Not sunk
                        print('hit')
                    grid_obj.add_guess() #Changes to True
                    grid_obj.get_ship().ship_hit() #Reduce count of all ship
                    self.subtract_ship()           #Reduce count of each ships
            if self.get_totalship() == 0:
                print('all ships sunk: game over')
                sys.exit(1)
        else:
            print('illegal guess')
    '''
    Prints out the grid for testing purposes
    '''
    def show_grid(self):
        for i in range(SIZE):
            for j in range(SIZE):
                print(self._grid[i][j], '', end='')
            print()

    def subtract_ship(self): #Subtracts 1 from the size of a ship
        self._totalship -= 1

    def get_grid(self): #Gets grid
        return self._grid

    def get_totalship(self): #Gets total ship count
        return self._totalship

    def get_gridpos(self, x, y): #Gets an object at a grid position
        return self._grid[y][x]

'''
An instance of this class represents a ship. Class passes in strings and the
x and y coordinates. Methods that subtract from the total sum of the sizes of
the ships.
'''
class Ship:
    def __init__(self, ship, x1, y1, x2, y2):
        self._ship = ship
        self._x1 = int(x1)
        self._y1 = int(y1)
        self._x2 = int(x2)
        self._y2 = int(y2)
        self._shiphit = int(SHIP_SIZE[ship])

    def get_shiptype(self):
        return self._ship

    def ship_hit(self):
        self._shiphit -= 1

    def get_sunk(self):
        return self._shiphit
'''
Function to check if the placement file is valid. Prints out error and exits
the program. Passes in a set to check if a ship has already been placed.
'''
def check_placement(line, compo_set):
    ship = line[P_SHIP]
    x1 = int(line[P_X1])
    y1 = int(line[P_Y1])
    x2 = int(line[P_X2])
    y2 = int(line[P_Y2])
    xdiff1 = x2 - x1 + 1
    xdiff2 = x1 - x2 + 1
    ydiff1 = y2 - y1 + 1
    ydiff2 = y1 - y2 + 1
    invalid = ' '.join(line)
    if not((0 <= x1 < SIZE) and (0 <= y1 < SIZE) and
            (0 <= x2 < SIZE) and (0 <= y2 < SIZE)):
        print('ERROR: ship out-of-bounds: ' + invalid + '\n')
        sys.exit(1)
    elif (ship not in SHIP_SIZE) or (ship in compo_set):
        print('ERROR: fleet composition incorrect' + '\n')
        sys.exit(1)
    elif ship == 'A':
        size_a = SHIP_SIZE['A']
        if not((xdiff1 == size_a) or (xdiff2 == size_a) or
                (ydiff1 == size_a) or (ydiff2 == size_a)):
            print('ERROR: incorrect ship size: ' + invalid + '\n')
            sys.exit(1)
    elif ship == 'B':
        size_b = SHIP_SIZE['B']
        if not((xdiff1 == size_b) or (xdiff2 == size_b) or
                (ydiff1 == size_b) or (ydiff2 == size_b)):
            print('ERROR: incorrect ship size: ' + invalid + '\n')
            sys.exit(1)
    elif ship == 'S':
        size_s = SHIP_SIZE['S']
        if not((xdiff1 == size_s) or (xdiff2 == size_s) or
                (ydiff1 == size_s) or (ydiff2 == size_s)):
            print('ERROR: incorrect ship size: ' + invalid + '\n')
            sys.exit(1)
    elif ship == 'D':
        size_d = SHIP_SIZE['D']
        if not((xdiff1 == size_d) or (xdiff2 == size_d) or
                (ydiff1 == size_d) or (ydiff2 == size_d)):
            print('ERROR: incorrect ship size: ' + invalid + '\n')
            sys.exit(1)
    elif ship == 'P':
        size_p = SHIP_SIZE['P']
        if not((xdiff1 == size_p) or (xdiff2 == size_p) or
                (ydiff1 == size_p) or (ydiff2 == size_p)):
            print('ERROR: incorrect ship size: ' + invalid + '\n')
            sys.exit(1)
    compo_set.add(ship)


def main():
    try:
        compo_set = set() #Checks if a ship is already been placed
        b = Board()
        filename = input()
        placement_file = open(filename).readlines()
        if len(placement_file) != 5:
            print('ERROR: fleet composition incorrect')
            sys.exit(1)
        for place_line in placement_file:
            place_line = place_line.strip().split()
            check_placement(place_line, compo_set)
            b.fill_board(place_line)
    except FileNotFoundError:
        print('ERROR: Could not open file: ' + filename)
        sys.exit(1)
    try:
        filename = input()
        guess_file = open(filename)
        for guess_line in guess_file:
            guess_line = guess_line.strip().split()
            if len(guess_line) > 0:
                b.process_guesses(guess_line)
    except FileNotFoundError:
        print('ERROR: Cannot read file: ' + filename)
        sys.exit(1)

main()