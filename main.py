import pygame

from pygame.locals import *

from sys import exit

import random

import queue

from random import randrange

pygame.init()

# FPS = 10
# fpsClock = pygame.time.Clock()
clock = pygame.time.Clock()
time_save = 0

screen = pygame.display.set_mode((0, 0), FULLSCREEN, 32)
w = screen.get_width()
h = screen.get_height()


# PixelToScreenSize
def PSS(pixel):
    return int(w * (pixel / 1500))


# pygame.mouse.set_visible(False)
"""
loadBackground = pygame.image.load("Background.png").convert()
background = pygame.transform.scale(loadBackground, (w, h))
"""

mazeSize = 33
GridSize = PSS(20)
big = False

WallColour = (0, 0, 10)
passageColour = (255, 255, 255)
BackgroundColour = (255, 255, 255)

"""
WallColour = (0, 0, 100)
passageColour = (50, 255, 255)
BackgroundColour = (50, 100, 200)
"""


def getColumnRowPos(column, row):
    columnPixelPos = w / 2 - ((mazeSize / 2 + 1) * GridSize) + (column * GridSize)
    rowPixelPos = h / 2 - ((mazeSize / 2 + 1) * GridSize) + (row * GridSize)
    return columnPixelPos, rowPixelPos


def ColumnRowArrayPos(column, row):
    arraypos = (column + 1) + (row * mazeSize)
    return arraypos


class Cell:

    def __init__(self, column, row, color):
        self.column = column
        self.row = row
        self.color = color
        self.pos = getColumnRowPos(self.column, self.row)

    def show(self):
        pygame.draw.rect(screen, self.color, (self.pos[0], self.pos[1], GridSize, GridSize))
        # pygame.draw.rect(screen, (0, 0, 0), (self.pos[0], self.pos[1], \
        #                                    GridSize + int(int(GridSize / 5) / 2),
        #                                     GridSize + int(int(GridSize / 5) / 2)), int(GridSize / 5))


class Labyrinth:

    def __init__(self):
        self.border = []
        self.maze = []
        for x in range(mazeSize + 2):
            for y in range(mazeSize + 2):

                if x == 0 or x == mazeSize + 1:
                    self.border.append(Cell(y, x, WallColour))

                if 0 < x < mazeSize + 1:
                    if 0 < y < mazeSize + 1:
                        self.maze.append(Cell(y, x, passageColour))
                    if y == 0 or y == mazeSize + 1:
                        self.border.append(Cell(y, x, WallColour))

    def show(self):
        for x in range(len(self.maze)):
            self.maze[x].show()

        for x in range(len(self.border)):
            self.border[x].show()


class MazeGeneration:
    def __init__(self):
        self.mazeButtonRect = Rect(w / 2 - ((mazeSize / 2 + 2) * GridSize) - PSS(200), \
                                   h / 2 - ((mazeSize / 2 + 1) * GridSize) + (PSS(120) * 3), PSS(200), PSS(100))
        self.genMaze = False

        # for maze generation

        self.start = int(ColumnRowArrayPos(mazeSize / 2 - 1.5, 0))
        self.end = int(ColumnRowArrayPos(mazeSize / 2 - 1.5, mazeSize))

        self.player = self.start

        self.visitedCells = []
        self.counter = -1
        self.checkStop = False
        self.lastPlayerPos = 0
        self.goback = True
        self.gNormalMaze = False

    def preparePattern(self):

        # Generate starting grid
        for x in range(len(l.maze)):
            l.maze[x].color = passageColour

        count = 1
        for x in range(len(l.maze)):
            if count <= mazeSize:
                if x % 2 > 0:
                    l.maze[x].color = WallColour

            if mazeSize * 2 >= count > mazeSize:
                l.maze[x].color = WallColour

            if count > mazeSize * 2:
                count = 1
            count += 1

        self.genMaze = True
        self.checkStop = False
        self.visitedCells = []
        self.player = self.start

    def getdirectionsCells(self, x):
        directionsCells = {
            0: self.player - mazeSize * 2,
            1: self.player + 2,
            2: self.player + mazeSize * 2,
            3: self.player - 2
        }

        return directionsCells[x]

    def getWallCells(self, x):
        wallCells = {
            0: self.player - mazeSize,
            1: self.player + 1,
            2: self.player + mazeSize,
            3: self.player - 1
        }

        return wallCells[x]

    def gMaze(self):
        if self.player is self.start and self.checkStop is True:
            l.maze[self.player].color = passageColour
            self.genMaze = False
            if mg.gNormalMaze:
                nmg.makeHoles()
                self.gNormalMaze = False


        if self.player != self.start or self.checkStop is False:
            self.checkStop = True
            # makes a maze pattern
            l.maze[self.lastPlayerPos].color = passageColour
            if self.player not in self.visitedCells:
                self.visitedCells.append(self.player)

            possibleDir = [0, 0, 0, 0]

            """    """
            self.goback = True
            for x in range(4):
                if len(l.maze) > self.getdirectionsCells(x) >= 0:
                    if l.maze[self.getdirectionsCells(x)].color == passageColour \
                            and self.getdirectionsCells(x) not in self.visitedCells:
                        possibleDir[x] = 1

                        self.goback = False
                        self.counter = -1

            skipp = False
            if self.goback:

                for x in range(len(self.visitedCells) - 1, -1, -1):

                    if self.goback:

                        self.player = self.visitedCells[x]

                        for y in range(4):
                            if len(l.maze) > self.getdirectionsCells(y) >= 0:

                                if l.maze[self.getdirectionsCells(y)].color == \
                                        passageColour and self.getdirectionsCells(y) not in self.visitedCells:
                                    self.goback = False

                for x in range(4):
                    if len(l.maze) > self.getdirectionsCells(x) >= 0:
                        if l.maze[self.getdirectionsCells(x)].color == passageColour \
                                and self.getdirectionsCells(x) not in self.visitedCells:
                            possibleDir[x] = 1

            rc = []

            for x in range(4):
                if possibleDir[x] == 1:
                    rc.append(x)

            if len(rc) > 0:
                r = random.choice(rc)
                l.maze[self.getWallCells(r)].color = passageColour
                self.player = self.getdirectionsCells(r)
            l.maze[self.player].color = (255, 0, 0)
            self.lastPlayerPos = self.player

    def showBotton(self):

        pygame.draw.rect(screen, passageColour, self.mazeButtonRect)
        pygame.draw.rect(screen, (0, 0, 0), self.mazeButtonRect, 3)
        font = pygame.font.Font(None, 30)
        text1 = font.render("Generate", True, (0, 0, 0))
        text2 = font.render("Perfect Maze", True, (0, 0, 0))
        text_rect = text1.get_rect(center=(self.mazeButtonRect.centerx, self.mazeButtonRect.centery - 15))
        screen.blit(text1, text_rect)
        text_rect = text2.get_rect(center=(self.mazeButtonRect.centerx, self.mazeButtonRect.centery + 15))
        screen.blit(text2, text_rect)

    def checkBotton(self):
        Mouse_XY = pygame.mouse.get_pos()

        if (self.mazeButtonRect[0] < Mouse_XY[0] < self.mazeButtonRect[0] \
                + self.mazeButtonRect.width):
            if (self.mazeButtonRect[1] < Mouse_XY[1] < self.mazeButtonRect[1] \
                    + self.mazeButtonRect.height):
                mg.preparePattern()


def isMazeClear():
    mazeClear = True
    for x in range(len(l.maze)):
        if l.maze[x].color != passageColour:
            mazeClear = False
    return mazeClear


class Buttons:

    def __init__(self, y, butoonText):
        self.y = y
        self.ButtonRect = Rect(w / 2 + ((mazeSize / 2 + 2) * GridSize), \
                               h / 2 - ((mazeSize / 2 + 1) * GridSize) + (PSS(120) * y), PSS(200), PSS(100))
        self.buttonText = butoonText
        self.mazeCopy = []

    def show(self):
        pygame.draw.rect(screen, passageColour, self.ButtonRect)
        pygame.draw.rect(screen, (0, 0, 0), self.ButtonRect, 3)

        font = pygame.font.Font(None, 30)
        text = font.render(self.buttonText, True, (0, 0, 0))
        text_rect = text.get_rect(center=(self.ButtonRect.centerx, self.ButtonRect.centery))
        screen.blit(text, text_rect)

    def checkBotton(self):
        Mouse_XY = pygame.mouse.get_pos()

        if (self.ButtonRect[0] < Mouse_XY[0] < self.ButtonRect[0] \
                + self.ButtonRect.width):
            if (self.ButtonRect[1] < Mouse_XY[1] < self.ButtonRect[1] \
                    + self.ButtonRect.height):

                if self.y == 0 and mg.genMaze == False:
                    for x in range(len(l.maze)):
                        l.maze[x].color = passageColour
                    PledA.doPa = False
                if self.y > 0:
                    if not isMazeClear():
                        self.mazeCopy = []
                        for y in range(len(l.maze)):
                            self.mazeCopy.append(l.maze[y].color)

                    if isMazeClear():
                        if len(self.mazeCopy) > 0:
                            for y in range(len(l.maze)):
                                l.maze[y].color = self.mazeCopy[y]

    def showAllButtons(self):

        for x in range(len(b)):
            b[x].show()


class PledgeAlgorithmus:

    def __init__(self):
        self.start = [int(mazeSize / 2), 0]
        self.end = [int(mazeSize / 2), mazeSize - 1]
        self.player = self.start
        self.dir = 2
        self.mazeButtonRect = Rect(w / 2 - ((mazeSize / 2 + 2) * GridSize) - PSS(200), \
                                   h / 2 - ((mazeSize / 2 + 1) * GridSize), PSS(200), PSS(100))
        self.doPa = False

    def tabelToLine(self, tabel):
        line = tabel[0] + tabel[1] * mazeSize
        return line

    def LFRDir(self):
        changes = {
            0: [[self.player[0] - 1, self.player[1]], [self.player[0], self.player[1] - 1],
                [self.player[0] + 1, self.player[1]]],
            1: [[self.player[0], self.player[1] - 1], [self.player[0] + 1, self.player[1]],
                [self.player[0], self.player[1] + 1]],
            2: [[self.player[0] + 1, self.player[1]], [self.player[0], self.player[1] + 1],
                [self.player[0] - 1, self.player[1]]],
            3: [[self.player[0], self.player[1] + 1], [self.player[0] - 1, self.player[1]],
                [self.player[0], self.player[1] - 1]],
        }
        save = changes[self.dir]
        return save

    def turnLeft(self):
        if self.dir == 0:
            self.dir = 3
        else:
            self.dir -= 1

    def turnRight(self):
        if self.dir == 3:
            self.dir = 0
        else:
            self.dir += 1

    def wallOnTheLeft(self):
        IsWall = False
        if self.tabelToLine(self.LFRDir()[0]) >= len(l.maze):
            IsWall = True
        elif l.maze[self.tabelToLine(self.LFRDir()[0])].color == passageColour \
                and self.tabelToLine(self.LFRDir()[0]) >= 0 \
                and mazeSize - 1 >= self.LFRDir()[0][0] >= 0 \
                and mazeSize - 1 >= self.LFRDir()[0][1] >= 0:
            IsWall = False
        else:
            IsWall = True
        return IsWall

    def wallInFront(self):
        IsWall = False
        if self.tabelToLine(self.LFRDir()[1]) >= len(l.maze):
            IsWall = True
        elif l.maze[self.tabelToLine(self.LFRDir()[1])].color == passageColour \
                and self.tabelToLine(self.LFRDir()[1]) >= 0 \
                and mazeSize - 1 >= self.LFRDir()[1][0] >= 0 \
                and mazeSize - 1 >= self.LFRDir()[1][1] >= 0:
            IsWall = False
        else:
            IsWall = True
        return IsWall

    def moveToWall(self):
        pass

    def show(self):
        # show start and end
        l.maze[self.tabelToLine(self.start)].color = (100, 200, 0)

        start_x = l.maze[self.tabelToLine(self.start)].pos[0]
        start_y = l.maze[self.tabelToLine(self.start)].pos[1]
        end_x = l.maze[self.tabelToLine(self.end)].pos[0]
        end_y = l.maze[self.tabelToLine(self.end)].pos[1]
        pygame.draw.rect(screen, (100, 200, 0), (end_x, end_y, GridSize, GridSize))

        startRect = Rect(start_x, start_y, GridSize, GridSize)
        endRect = Rect(end_x, end_y, GridSize, GridSize)

        font = pygame.font.Font(None, GridSize + 5)
        text1 = font.render("S", True, (0, 0, 0))
        text2 = font.render("E", True, (0, 0, 0))

        text_rect1 = text1.get_rect(center=(startRect.centerx, startRect.centery))
        text_rect2 = text2.get_rect(center=(endRect.centerx, endRect.centery))
        screen.blit(text1, text_rect1)
        screen.blit(text2, text_rect2)

        # show Player

        player_x = l.maze[self.tabelToLine(self.player)].pos[0]
        player_y = l.maze[self.tabelToLine(self.player)].pos[1]

        pygame.draw.ellipse(screen, (255, 0, 0), (player_x, player_y, GridSize, GridSize))

    def move(self):

        if self.player != self.end:

            if not self.wallOnTheLeft():
                self.turnLeft()
                self.player = self.LFRDir()[1]
            else:

                while self.wallInFront():
                    self.turnRight()

                self.player = self.LFRDir()[1]
        else:
            l.maze[self.tabelToLine(self.start)].color = passageColour
            PledA.doPa = False

    def showBotton(self):

        pygame.draw.rect(screen, passageColour, self.mazeButtonRect)
        pygame.draw.rect(screen, (0, 0, 0), self.mazeButtonRect, 3)

        font = pygame.font.Font(None, 30)

        text2 = font.render("Wall follower", True, (0, 0, 0))

        text_rect = text2.get_rect(center=(self.mazeButtonRect.centerx, self.mazeButtonRect.centery))
        screen.blit(text2, text_rect)

    def checkBotton(self):
        Mouse_XY = pygame.mouse.get_pos()

        if (self.mazeButtonRect[0] < Mouse_XY[0] < self.mazeButtonRect[0] \
                + self.mazeButtonRect.width):
            if (self.mazeButtonRect[1] < Mouse_XY[1] < self.mazeButtonRect[1] \
                    + self.mazeButtonRect.height):
                PledA.doPa = True
                self.player = self.start


class BreadthFirstSearch:

    def __init__(self):

        self.doBFS = False
        self.createMazeBool = True
        self.start = [int(mazeSize / 2) + 1, 1]
        self.end = [int(mazeSize / 2) + 1, mazeSize + 1]
        self.pos = [self.start[0], self.start[1]]
        self.maze = []

        self.solution = []

        self.possibleSteps = []

        self.mazeButtonRect = Rect(w / 2 - ((mazeSize / 2 + 2) * GridSize) - PSS(200), \
                                   h / 2 - ((mazeSize / 2 + 1) * GridSize) + PSS(120), PSS(200), PSS(100))
        self.visitedCells = [self.pos]

    def createMaze(self):

        maze = []
        row1 = []
        for i in range(mazeSize + 2):
            row1.append("#")
        maze.append(row1)

        for i in range(mazeSize):
            row = ["#"]
            for j in range(mazeSize):
                if j == int(mazeSize / 2) and i == 0:
                    row.append("O")
                elif j == int(mazeSize / 2) and i == mazeSize - 1:
                    row.append("X")
                elif l.maze[j + i * mazeSize].color == WallColour:
                    row.append("#")
                else:
                    row.append(" ")
            row.append("#")
            maze.append(row)

        row2 = []
        for i in range(mazeSize + 2):
            row2.append("#")
        maze.append(row2)
        return maze


    def foundEnd(self):
        if self.maze[self.pos[1] - 1][self.pos[0]] == "X":
            return True
        if self.maze[self.pos[1]][self.pos[0] + 1] == "X":
            return True
        if self.maze[self.pos[1] + 1][self.pos[0]] == "X":
            return True
        if self.maze[self.pos[1]][self.pos[0] - 1] == "X":
            return True
        return False

    def posibleCells(self):

        cells = []

        if self.maze[self.pos[1] - 1][self.pos[0]] == " " and [self.pos[0], self.pos[1] - 1] not in self.visitedCells:
            cells.append([self.pos[0], self.pos[1] - 1])
        if self.maze[self.pos[1]][self.pos[0] + 1] == " " and [self.pos[0] + 1, self.pos[1]] not in self.visitedCells:
            cells.append([self.pos[0] + 1, self.pos[1]])
        if self.maze[self.pos[1] + 1][self.pos[0]] == " " and [self.pos[0], self.pos[1] + 1] not in self.visitedCells:
            cells.append([self.pos[0], self.pos[1] + 1])
        if self.maze[self.pos[1]][self.pos[0] - 1] == " " and [self.pos[0] - 1, self.pos[1]] not in self.visitedCells:
            cells.append([self.pos[0] - 1, self.pos[1]])
        return cells

    def move(self):

        if self.createMazeBool:
            self.maze = self.createMaze()
            self.createMazeBool = False

        if self.foundEnd():
            for i, el in enumerate(self.visitedCells):
                l.maze[self.tabelToLine(el[0], el[1])].color = (255, 255, 255)
            for i, el in enumerate(self.solution[0]):
                l.maze[self.tabelToLine(el[0], el[1])].color = (255, 0, 0)
            l.maze[self.tabelToLine(self.start[0], self.start[1])].color = (100, 200, 0)
            self.pos = [self.start[0], self.start[1]]
            self.visitedCells = [self.pos]
            self.solution = []
            self.possibleSteps = []
            self.createMazeBool = True
            BFS.doBFS = False

        else:

            if not self.solution:
                self.possibleSteps.extend(self.posibleCells())
            else:

                savePosibleCells = []
                savePosibleCells.extend(self.posibleCells())

                for i, el in enumerate(savePosibleCells):
                    save = []
                    if isinstance(self.solution[0][-1], list):
                        save.extend(self.solution[0])
                    else:
                        save.extend(self.solution)
                    save.append(savePosibleCells[i])
                    self.possibleSteps.append(save)

            self.solution = []
            #print("hucisuhi", self.possibleSteps)
            if isinstance(self.possibleSteps[0][-1], list):
                #print("1")
                self.solution.append(self.possibleSteps[0])
            else:
                #print("2")
                self.solution.append(self.possibleSteps[0])

            self.possibleSteps.pop(0)

            if isinstance(self.solution[0][-1], list):
                self.pos = self.solution[0][-1]
            else:
                self.pos = self.solution[0]
            #print("sol", self.solution, "pSteps", self.possibleSteps, "pos", self.pos)

            self.visitedCells.append(self.pos)

    def tabelToLine(self, column, row):
        line = (column - 1) + (mazeSize * (row - 1))
        return line

    def show(self):

        for i, el in enumerate(self.visitedCells):
            l.maze[self.tabelToLine(el[0], el[1])].color = (255, 0, 0)

        start_x = l.maze[self.tabelToLine(self.start[0], self.start[1])].pos[0]
        start_y = l.maze[self.tabelToLine(self.start[0], self.start[1])].pos[1]
        end_x = l.maze[self.tabelToLine(self.end[0], self.end[1] - 1)].pos[0]
        end_y = l.maze[self.tabelToLine(self.end[0], self.end[1] - 1)].pos[1]
        #pygame.draw.rect(screen, (100, 200, 0), (end_x, end_y, GridSize, GridSize))

        startRect = Rect(start_x, start_y, GridSize, GridSize)
        endRect = Rect(end_x, end_y, GridSize, GridSize)

        font = pygame.font.Font(None, GridSize + 5)
        text1 = font.render("S", True, (0, 0, 0))
        text2 = font.render("E", True, (0, 0, 0))

        text_rect1 = text1.get_rect(center=(startRect.centerx, startRect.centery))
        text_rect2 = text2.get_rect(center=(endRect.centerx, endRect.centery))
        screen.blit(text1, text_rect1)
        screen.blit(text2, text_rect2)


        l.maze[self.tabelToLine(self.start[0], self.start[1])].color = (100, 200, 0)
        l.maze[self.tabelToLine(self.end[0], self.end[1] - 1)].color = (100, 200, 0)

    def showBotton(self):

        pygame.draw.rect(screen, passageColour, self.mazeButtonRect)
        pygame.draw.rect(screen, (0, 0, 0), self.mazeButtonRect, 3)

        font = pygame.font.Font(None, 30)
        text2 = font.render("BFS", True, (0, 0, 0))
        text_rect = text2.get_rect(center=(self.mazeButtonRect.centerx, self.mazeButtonRect.centery))
        screen.blit(text2, text_rect)

    def checkBotton(self):
        Mouse_XY = pygame.mouse.get_pos()

        if (self.mazeButtonRect[0] < Mouse_XY[0] < self.mazeButtonRect[0] \
                + self.mazeButtonRect.width):
            if (self.mazeButtonRect[1] < Mouse_XY[1] < self.mazeButtonRect[1] \
                    + self.mazeButtonRect.height):
                BFS.doBFS = True

"""
class DepthFirstSearch:

    def __init__(self):

        self.doDFS = False
        self.start = int(ColumnRowArrayPos(mazeSize / 2 - 1.5, 0))
        self.end = int(ColumnRowArrayPos(mazeSize / 2 - 1.5, mazeSize))

        self.player = self.start

        self.visitedCells = []
        self.counter = -1
        self.checkStop = False
        self.lastPlayerPos = 0
        self.goback = True

        self.mazeButtonRect = Rect(w / 2 - ((mazeSize / 2 + 2) * GridSize) - 200, \
                                   h / 2 - ((mazeSize / 2 + 1) * GridSize) + 200 + GridSize * 2, 200, 100)


    def getdirectionsCells(self, x):
        wallCells = {
            0: self.player - mazeSize,
            1: self.player + 1,
            2: self.player + mazeSize,
            3: self.player - 1
        }
        return wallCells[x]

    def move(self):
        if self.player is self.start and self.checkStop is True:
            l.maze[self.player].color = passageColour
            self.genMaze = False

        if self.player != self.start or self.checkStop is False:
            self.checkStop = True
            # makes a maze pattern
            #l.maze[self.lastPlayerPos].color = passageColour
            if self.player not in self.visitedCells:
                self.visitedCells.append(self.player)

            possibleDir = [0, 0, 0, 0]

            """    """
            self.goback = True
            for x in range(4):
                if len(l.maze) > self.getdirectionsCells(x) >= 0:
                    if l.maze[self.getdirectionsCells(x)].color == passageColour \
                            and self.getdirectionsCells(x) not in self.visitedCells:
                        possibleDir[x] = 1

                        self.goback = False
                        self.counter = -1

            skipp = False
            if self.goback:

                for x in range(len(self.visitedCells) - 1, -1, -1):

                    if self.goback:

                        self.player = self.visitedCells[x]

                        for y in range(4):
                            if len(l.maze) > self.getdirectionsCells(y) >= 0:

                                if l.maze[self.getdirectionsCells(y)].color == \
                                        passageColour and self.getdirectionsCells(y) not in self.visitedCells:
                                    self.goback = False

                for x in range(4):
                    if len(l.maze) > self.getdirectionsCells(x) >= 0:
                        if l.maze[self.getdirectionsCells(x)].color == passageColour \
                                and self.getdirectionsCells(x) not in self.visitedCells:
                            possibleDir[x] = 1



            for x in range(len(possibleDir)):
                if possibleDir[x] == 1:
                    #l.maze[self.visitedCells[-1]].color = (255, 0, 0)
                    self.lastPlayerPos = self.player
                    self.player = self.getdirectionsCells(x)
            print(self.player)




    def tabelToLine(self, column, row):
        line = (column - 1) + (mazeSize * (row - 1))
        return line

    def showBotton(self):

        pygame.draw.rect(screen, passageColour, self.mazeButtonRect)
        pygame.draw.rect(screen, (0, 0, 0), self.mazeButtonRect, 3)

        font = pygame.font.Font(None, 30)
        text2 = font.render("DFS", True, (0, 0, 0))
        text_rect = text2.get_rect(center=(self.mazeButtonRect.centerx, self.mazeButtonRect.centery))
        screen.blit(text2, text_rect)

    def checkBotton(self):
        Mouse_XY = pygame.mouse.get_pos()

        if (self.mazeButtonRect[0] < Mouse_XY[0] < self.mazeButtonRect[0] \
                + self.mazeButtonRect.width):
            if (self.mazeButtonRect[1] < Mouse_XY[1] < self.mazeButtonRect[1] \
                    + self.mazeButtonRect.height):
                DFS.doDFS = True
"""

class gNormalMaze:

    def __init__(self):
        self.mazeButtonRect = Rect(w / 2 - ((mazeSize / 2 + 2) * GridSize) - PSS(200), \
                                   h / 2 - ((mazeSize / 2 + 1) * GridSize) + (PSS(120) * 2), PSS(200), PSS(100))

    def makeHoles(self):
        for x in range(int(mazeSize/2)):
            r = random.choice(l.maze)
            if r.color == WallColour:
                r.color = passageColour
            else:
                while r.color != WallColour:
                    r = random.choice(l.maze)
            r.color = passageColour


    def showBotton(self):

        pygame.draw.rect(screen, passageColour, self.mazeButtonRect)
        pygame.draw.rect(screen, (0, 0, 0), self.mazeButtonRect, 3)
        font = pygame.font.Font(None, 30)
        text1 = font.render("Generate", True, (0, 0, 0))
        text2 = font.render("Normal Maze", True, (0, 0, 0))
        text_rect = text1.get_rect(center=(self.mazeButtonRect.centerx, self.mazeButtonRect.centery - 15))
        screen.blit(text1, text_rect)
        text_rect = text2.get_rect(center=(self.mazeButtonRect.centerx, self.mazeButtonRect.centery + 15))
        screen.blit(text2, text_rect)

    def checkBotton(self):
        Mouse_XY = pygame.mouse.get_pos()

        if (self.mazeButtonRect[0] < Mouse_XY[0] < self.mazeButtonRect[0] \
                + self.mazeButtonRect.width):
            if (self.mazeButtonRect[1] < Mouse_XY[1] < self.mazeButtonRect[1] \
                    + self.mazeButtonRect.height):
                mg.preparePattern()
                mg.gNormalMaze = True




l = Labyrinth()
mg = MazeGeneration()
nmg = gNormalMaze()
b = [Buttons(0, "Clear")]
PledA = PledgeAlgorithmus()
BFS = BreadthFirstSearch()
#DFS = DepthFirstSearch()

for x in range(1, 4):
    b.append(Buttons(x, "Maze " + str(x)))

while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            exit()
        if event.type == KEYUP:
            if event.key == K_ESCAPE:
                exit()
            if event.key == K_g:
                # change size to 53 or 33
                if not big:
                    mazeSize = 33
                    GridSize = PSS(20)
                    big = True

                    l = Labyrinth()
                    mg = MazeGeneration()
                    nmg = gNormalMaze()
                    b = [Buttons(0, "Clear")]
                    PledA = PledgeAlgorithmus()
                    BFS = BreadthFirstSearch()

                    for x in range(1, 4):
                        b.append(Buttons(x, "Maze " + str(x)))
                else:
                    mazeSize = 53
                    GridSize = PSS(15)
                    big = False

                    l = Labyrinth()
                    mg = MazeGeneration()
                    nmg = gNormalMaze()
                    b = [Buttons(0, "Clear")]
                    PledA = PledgeAlgorithmus()
                    BFS = BreadthFirstSearch()

                    for x in range(1, 4):
                        b.append(Buttons(x, "Maze " + str(x)))

        if event.type == MOUSEBUTTONUP:
            mg.checkBotton()
            for x in range(len(b)):
                b[x].checkBotton()
            PledA.checkBotton()
            BFS.checkBotton()
            nmg.checkBotton()
            #DFS.checkBotton()

    screen.fill(BackgroundColour)
    l.show()
    mg.showBotton()
    nmg.showBotton()
    if mg.genMaze is True:
        mg.gMaze()

    for x in range(len(b)):
        b[x].show()
    time_passed = clock.tick()
    time_passed_seconds = time_passed / 1000.0
    time_save += time_passed_seconds

    BFS.showBotton()
    if BFS.doBFS:
        BFS.show()
        BFS.move()
    """
    DFS.showBotton()
    if DFS.doDFS:
        DFS.move()
    """
    if PledA.doPa:
        PledA.show()
        if time_save >= 0.05:
            PledA.move()
            time_save = 0


    PledA.showBotton()

    pygame.display.update()
    # fpsClock.tick(FPS)
