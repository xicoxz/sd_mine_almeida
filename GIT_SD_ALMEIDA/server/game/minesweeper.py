import random
import re
import time
from string import ascii_lowercase
import stubs


class MineSweeper:

    def __init__(self):
        self.players = []
        self.currgrid = None
        self.points = 0
        self.grid = []
        self.size = None
        self.n_mines=None
        self.turn = ""
        self.flags = []
        self.starttime = 0
        self.ongoing_game = False
        self.is_first_move = True
        self.helpmessage = ("Type the column followed by the row (eg. a5). "
                            "To put or remove a flag, add 'f' to the cell (eg. a5f).")

        # self.showgrid(self.currgrid)

    def startgame(self):
        if not self.ongoing_game:
            self.ongoing_game = True

            return False

        return self.ongoing_game

    def addplayer(self, player):
        if player in self.players:
            return stubs.PLAYER_EXISTS
        else:
            if len(self.players) == 0:
                self.turn = player
            self.players.append(player)
            print(self.players)
            return True

    def is_turn(self, player):
        return player == self.turn

    def removeplayer(self, player):
        self.players.pop(player)

    def makemove(self, move):
        minesleft = self.n_mines - len(self.flags)
        result = self.parseinput(move, self.size, self.helpmessage + '\n')

        message = result['message']
        cell = result['cell']

        if cell:
            # print('\n\n')
            rowno, colno = cell

            if not self.grid:
                self.grid, self.mines = self.setupgrid(cell)
            if not self.starttime:
                self.starttime = time.time()

            if not self.currgrid:
                self.gridsize = len(self.grid)
                self.currgrid = [[' ' for i in range(self.gridsize)] for i in range(self.gridsize)]
            currcell = self.currgrid[rowno][colno]
            flag = result['flag']

            if flag:
                # Add a flag if the cell is empty
                if currcell == ' ':
                    self.currgrid[rowno][colno] = 'F'
                    self.flags.append(cell)
                    if self.grid[rowno][colno] == 'X':
                        self.points += 1
                    else:
                        self.points -= 3
                # Remove the flag if there is one
                elif move == 'F':
                    self.currgrid[rowno][colno] = ' '
                    self.flags.remove(cell)
                    self.points += 3
                else:
                    message = 'Cannot put a flag there'

            # If there is a flag there, show a message
            elif cell in self.flags:
                message = 'There is a flag there'

            elif self.grid[rowno][colno] == 'X':
                print('Game Over {}, You got {} points.\n'.format(self.player, self.points))
                # self.showgrid(self.grid)
                # if self.playagain():
                # self.playgame()
                return True

            elif move == ' ':
                self.showcells(self.grid, self.currgrid, rowno, colno)

            else:
                message = "That cell is already shown"

            if set(self.flags) == set(self.mines):
                minutes, seconds = divmod(int(time.time() - self.starttime), 60)
                print(
                    'You Win {} '
                    'It took you {} minutes and {} seconds and you got {} points.\n'.format(self.player, minutes,
                                                                                            seconds, self.points))
                self.showgrid(self.grid)
                if self.playagain():
                    self.playgame()
                return

        # self.showgrid(self.currgrid)
        return message

    def setupgrid(self, start):
        emptygrid = [['0' for i in range(self.size)] for i in range(self.size)]

        mines = self.getmines(emptygrid, start, self.n_mines)

        for i, j in mines:
            emptygrid[i][j] = 'X'

        grid = self.getnumbers(emptygrid)

        return (grid, mines)

    def showgrid(self):
        self.gridsize = len(self.grid)
        map = ""

        horizontal = '   ' + (4 * self.gridsize * '-') + '-'

        # Print top column letters
        toplabel = '     '

        for i in ascii_lowercase[:self.gridsize]:
            toplabel = toplabel + i + '   '

        map += toplabel + '\n' + horizontal

        # Print left row numbers
        for idx, i in enumerate(self.grid):
            row = '{0:2} |'.format(idx + 1)

            for j in i:
                row = row + ' ' + j + ' |'

            map += row + '\n' + horizontal

        return map

    def getrandomcell(self, grid):
        self.gridsize = len(grid)

        a = random.randint(0, self.gridsize - 1)
        b = random.randint(0, self.gridsize - 1)

        return (a, b)

    def getneighbors(self, grid, rowno, colno):
        self.gridsize = len(grid)
        neighbors = []

        for i in range(-1, 2):
            for j in range(-1, 2):
                if i == 0 and j == 0:
                    continue
                elif -1 < (rowno + i) < self.gridsize and -1 < (colno + j) < self.gridsize:
                    neighbors.append((rowno + i, colno + j))

        return neighbors

    def getmines(self, grid, start, numberofmines):
        mines = []
        neighbors = self.getneighbors(grid, *start)

        for i in range(numberofmines):
            cell = self.getrandomcell(grid)
            while cell == start or cell in mines or cell in neighbors:
                cell = self.getrandomcell(grid)
            mines.append(cell)

        return mines

    def getnumbers(self, grid):
        for rowno, row in enumerate(grid):
            for colno, cell in enumerate(row):
                if cell != 'X':
                    # Gets the values of the neighbors
                    values = [grid[r][c] for r, c in self.getneighbors(grid,
                                                                       rowno, colno)]

                    # Counts how many are mines
                    grid[rowno][colno] = str(values.count('X'))

        return grid

    def showcells(self, grid, currgrid, rowno, colno):
        # Exit function if the cell was already shown
        if currgrid[rowno][colno] != ' ':
            return

        # Show current cell
        currgrid[rowno][colno] = grid[rowno][colno]

        # Get the neighbors if the cell is empty
        if grid[rowno][colno] == '0':
            for r, c in self.getneighbors(grid, rowno, colno):
                # Repeat function for each neighbor that doesn't have a flag
                if currgrid[r][c] != 'F':
                    self.showcells(grid, currgrid, r, c)

    def parseinput(self, inputstring, gridsize, helpmessage):
        cell = ()
        flag = False
        message = "Invalid cell. " + helpmessage

        pattern = r'([a-{}])([0-9]+)(f?)'.format(ascii_lowercase[gridsize - 1])
        validinput = re.match(pattern, inputstring)

        if inputstring == 'help':
            message = helpmessage

        elif validinput:
            rowno = int(validinput.group(2)) - 1
            colno = ascii_lowercase.index(validinput.group(1))
            flag = bool(validinput.group(3))

            if -1 < rowno < gridsize:
                cell = (rowno, colno)
                message = ''

        return {'cell': cell, 'flag': flag, 'message': message}

    def playagain(self):
        choice = input('Play again? (y/n): ')

        return choice.lower() == 'y'
