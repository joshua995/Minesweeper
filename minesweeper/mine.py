"""
Joshua L
2025 May 19th
Top expert mode time: 53 seconds (May 19th, 2025)
Top expert mode time: 46 seconds (May 20th, 2025)
Top expert mode time: 44 seconds (May 21st, 2025)
Top intermediate mode time: 13 seconds (May 21st, 2025)
Top expert mode time: 33 seconds (May 23, 2025)
Top intermediate mode time: 10 seconds (May 23, 2025)
Top expert mode time: 24 seconds (May 24, 2025)
Top intermediate mode time: 8 seconds (May 24, 2025)
Top intermediate mode time: 7 seconds (May 26, 2025)
"""

import threading
import time
import pyautogui
from pyautogui import click, locateAllOnScreen
from sympy import Matrix
from math import ceil
import keyboard

pyautogui.PAUSE = 0.0000


class Tile:
    def __init__(self, x, y):
        self.pos = [x, y]  # 0 - grid size
        self.minesAroundTotal = 0
        self.minesAroundRemaining = 0
        self.flagged = False
        self.revealed = False
        self.tempRevealed = False
        self.neighbours = []
        self.tileIndexMatrix = -1
        self.equationMatrix = []
        self.counter = 0
        self.probList = []
        self.probability = 100

    def getNeighbours(self):
        if y := (self.pos[1] + 1 < GRID_DIM[1]):
            self.neighbours.append(grid[self.pos[0]][self.pos[1] + 1])
        if y1 := (self.pos[1] - 1 >= 0):
            self.neighbours.append(grid[self.pos[0]][self.pos[1] - 1])
        if x := (self.pos[0] + 1 < GRID_DIM[0]):
            self.neighbours.append(grid[self.pos[0] + 1][self.pos[1]])
        if x1 := (self.pos[0] - 1 >= 0):
            self.neighbours.append(grid[self.pos[0] - 1][self.pos[1]])
        if y and x:
            self.neighbours.append(grid[self.pos[0] + 1][self.pos[1] + 1])
        if y and x1:
            self.neighbours.append(grid[self.pos[0] - 1][self.pos[1] + 1])
        if y1 and x:
            self.neighbours.append(grid[self.pos[0] + 1][self.pos[1] - 1])
        if y1 and x1:
            self.neighbours.append(grid[self.pos[0] - 1][self.pos[1] - 1])

    def setRevealed(self, totalMines):
        self.revealed = True
        self.tempRevealed = True
        self.minesAroundTotal = totalMines
        self.minesAroundRemaining = totalMines

    def reveal(self):
        with lock:
            if self.revealed or self.flagged or self.tempRevealed:
                return
            self.tempRevealed = True
            click(
                BOARD_X[0] + (self.pos[1] * CELL_SIZE) + (CELL_SIZE / 2),
                BOARD_Y[0] + (self.pos[0] * CELL_SIZE) + (CELL_SIZE / 2),
            )

    def flag(self):
        self.flagged = True

    flagAllNeighbours = lambda self: [
        n.flag() for n in self.neighbours if not n.flagged and not n.revealed
    ]

    revealAllNeighbours = lambda self: [
        n.reveal() for n in self.neighbours if not n.flagged and not n.revealed
    ]

    def incrementCounter(self):
        self.counter += 1

    def removeMines(self):
        if not self.revealed:
            return
        self.counter = 0
        [self.incrementCounter() for n in self.neighbours if n.flagged]
        self.minesAroundRemaining = self.minesAroundTotal - self.counter
        return self.counter

    def getUnrevealedNeighbours(self):
        self.counter = 0
        [
            self.incrementCounter()
            for n in self.neighbours
            if not n.revealed and not n.flagged
        ]
        return self.counter

    def setEqMatrixAtPos(self, index, value):
        self.equationMatrix[index] = value

    def setProbListAtPos(self, index, value):
        self.probList[index] = value

    def setProbability(self, value):
        self.probability = value


lock = threading.Lock()

BOARD_X = [345, 1540]
BOARD_Y = [300, 940]

GRID_DIM = [16, 30]  # width 30 x height 20
CELL_SIZE = 40  #

MINE_COUNT = 99

grid = []

gameOver = False
win = False
changed = False


initGrid = lambda: (
    grid.clear(),
    [
        (
            grid.append([]),
            [grid[len(grid) - 1].append(Tile(x, y)) for y in range(GRID_DIM[1])],
        )
        for x in range(GRID_DIM[0])
    ],
    [[i.getNeighbours() for i in row] for row in grid],
)


def setGameOver():
    global gameOver
    gameOver = True


def setWin():
    global win
    win = True


def scanBoard():
    try:
        [
            grid[round(abs((BOARD_Y[0] - i.top) / CELL_SIZE))][
                round(abs((BOARD_X[0] - i.left) / CELL_SIZE))
            ].setRevealed(1)
            for i in locateAllOnScreen(
                "C:/Users/joshu/Documents/GitHub/Minesweeper/minesweeper/img/one.png",
                confidence=0.96,
                grayscale=True,
                region=(
                    BOARD_X[0],
                    BOARD_Y[0],
                    GRID_DIM[1] * CELL_SIZE,
                    GRID_DIM[0] * CELL_SIZE,
                ),
            )
        ]
    except:
        pass
    try:
        [
            grid[round(abs((BOARD_Y[0] - i.top) / CELL_SIZE))][
                round(abs((BOARD_X[0] - i.left) / CELL_SIZE))
            ].setRevealed(2)
            for i in locateAllOnScreen(
                "C:/Users/joshu/Documents/GitHub/Minesweeper/minesweeper/img/two.png",
                confidence=0.97,
                grayscale=True,
                region=(
                    BOARD_X[0],
                    BOARD_Y[0],
                    GRID_DIM[1] * CELL_SIZE,
                    GRID_DIM[0] * CELL_SIZE,
                ),
            )
        ]
    except:
        pass
    try:
        [
            grid[round(abs((BOARD_Y[0] - i.top) / CELL_SIZE))][
                round(abs((BOARD_X[0] - i.left) / CELL_SIZE))
            ].setRevealed(3)
            for i in locateAllOnScreen(
                "C:/Users/joshu/Documents/GitHub/Minesweeper/minesweeper/img/three.png",
                confidence=0.90,
                grayscale=True,
                region=(
                    BOARD_X[0],
                    BOARD_Y[0],
                    GRID_DIM[1] * CELL_SIZE,
                    GRID_DIM[0] * CELL_SIZE,
                ),
            )
        ]
    except:
        pass
    try:
        [
            grid[round(abs((BOARD_Y[0] - i.top) / CELL_SIZE))][
                round(abs((BOARD_X[0] - i.left) / CELL_SIZE))
            ].setRevealed(4)
            for i in locateAllOnScreen(
                "C:/Users/joshu/Documents/GitHub/Minesweeper/minesweeper/img/four.png",
                confidence=0.96,
                grayscale=True,
                region=(
                    BOARD_X[0],
                    BOARD_Y[0],
                    GRID_DIM[1] * CELL_SIZE,
                    GRID_DIM[0] * CELL_SIZE,
                ),
            )
        ]
    except:
        pass
    try:
        [
            grid[round(abs((BOARD_Y[0] - i.top) / CELL_SIZE))][
                round(abs((BOARD_X[0] - i.left) / CELL_SIZE))
            ].setRevealed(5)
            for i in locateAllOnScreen(
                "C:/Users/joshu/Documents/GitHub/Minesweeper/minesweeper/img/five.png",
                confidence=0.96,
                grayscale=True,
                region=(
                    BOARD_X[0],
                    BOARD_Y[0],
                    GRID_DIM[1] * CELL_SIZE,
                    GRID_DIM[0] * CELL_SIZE,
                ),
            )
        ]
    except:
        pass
    try:
        [
            grid[round(abs((BOARD_Y[0] - i.top) / CELL_SIZE))][
                round(abs((BOARD_X[0] - i.left) / CELL_SIZE))
            ].setRevealed(6)
            for i in locateAllOnScreen(
                "C:/Users/joshu/Documents/GitHub/Minesweeper/minesweeper/img/six.png",
                confidence=0.97,
                grayscale=True,
                region=(
                    BOARD_X[0],
                    BOARD_Y[0],
                    GRID_DIM[1] * CELL_SIZE,
                    GRID_DIM[0] * CELL_SIZE,
                ),
            )
        ]
    except:
        pass
    try:
        [
            grid[round(abs((BOARD_Y[0] - i.top) / CELL_SIZE))][
                round(abs((BOARD_X[0] - i.left) / CELL_SIZE))
            ].setRevealed(7)
            for i in locateAllOnScreen(
                "C:/Users/joshu/Documents/GitHub/Minesweeper/minesweeper/img/seven.png",
                confidence=0.97,
                grayscale=True,
                region=(
                    BOARD_X[0],
                    BOARD_Y[0],
                    GRID_DIM[1] * CELL_SIZE,
                    GRID_DIM[0] * CELL_SIZE,
                ),
            )
        ]
    except:
        pass
    try:
        [
            grid[round(abs((BOARD_Y[0] - i.top) / CELL_SIZE))][
                round(abs((BOARD_X[0] - i.left) / CELL_SIZE))
            ].setRevealed(8)
            for i in locateAllOnScreen(
                "C:/Users/joshu/Documents/GitHub/Minesweeper/minesweeper/img/eight.png",
                confidence=0.96,
                grayscale=True,
                region=(
                    BOARD_X[0],
                    BOARD_Y[0],
                    GRID_DIM[1] * CELL_SIZE,
                    GRID_DIM[0] * CELL_SIZE,
                ),
            )
        ]
    except:
        pass
    try:
        [
            grid[round(abs((BOARD_Y[0] - i.top) / CELL_SIZE))][
                round(abs((BOARD_X[0] - i.left) / CELL_SIZE))
            ].setRevealed(0)
            for i in locateAllOnScreen(
                "C:/Users/joshu/Documents/GitHub/Minesweeper/minesweeper/img/zero.png",
                confidence=0.565,
                grayscale=True,
                region=(
                    BOARD_X[0],
                    BOARD_Y[0],
                    GRID_DIM[1] * CELL_SIZE,
                    GRID_DIM[0] * CELL_SIZE,
                ),
            )
        ]
    except:
        pass
    try:
        [
            setGameOver()
            for _ in locateAllOnScreen(
                "C:/Users/joshu/Documents/GitHub/Minesweeper/minesweeper/img/mine.png",
                confidence=0.97,
                grayscale=True,
                region=(
                    BOARD_X[0],
                    BOARD_Y[0],
                    GRID_DIM[1] * CELL_SIZE,
                    GRID_DIM[0] * CELL_SIZE,
                ),
            )
        ]
    except:
        pass
    try:
        [
            (click(i.left, i.top), setWin())
            for i in locateAllOnScreen(
                "C:/Users/joshu/Documents/GitHub/Minesweeper/minesweeper/img/ok.png",
                confidence=0.60,
                grayscale=True,
            )
        ]
    except:
        pass


def setTileIndexGetUsableRevealedTiles():
    usableTiles, i = [], 0
    for row in grid:
        for tile in row:
            if (
                tile.revealed
                and tile.minesAroundRemaining > 0
                and not usableTiles.__contains__(tile)
            ):
                usableTiles.append(tile)
                for neighbour in tile.neighbours:
                    if (
                        not neighbour.revealed
                        and not neighbour.flagged
                        and neighbour.tileIndexMatrix == -1
                    ):
                        neighbour.tileIndexMatrix = i
                        i += 1
    return usableTiles, i


def createMatrix(usableTiles, length):
    matrix = []
    [
        (
            [tile.equationMatrix.append(0) for _ in range(length)],
            [
                tile.setEqMatrixAtPos(neighbour.tileIndexMatrix, 1)
                for neighbour in tile.neighbours
                if not neighbour.revealed and not neighbour.flagged
            ],
            tile.equationMatrix.append(tile.minesAroundRemaining),
            matrix.append(tile.equationMatrix),
        )
        for tile in usableTiles
    ]
    return matrix


isMines, isNotMines = None, None


def setMines(resultFromSolveMatrix):
    global isMines, isNotMines
    isMines, isNotMines = resultFromSolveMatrix


revealTileWithMatrix = lambda matrix: (
    setMines(solveMatrix(matrix)),
    [
        [
            (
                tile.removeMines(),
                (
                    (
                        tile.reveal() if isNotMine else tile.flag() if isMine else "",
                        setChanged(),
                    )
                    if (
                        not tile.flagged
                        and not tile.revealed
                        and (
                            (isNotMine := isNotMines.__contains__(tile.tileIndexMatrix))
                            or (isMine := isMines.__contains__(tile.tileIndexMatrix))
                        )
                    )
                    else ""
                ),
            )
            for tile in row
        ]
        for row in grid
    ],
)


def solveMatrix(matrix):
    aColumn = Matrix(matrix)
    xColumn = Matrix(aColumn.rref()[0])

    usableRows1IsMine0IsNot, usableRows0IsMine1IsNot = [], []
    for row in range(len(matrix)):
        sumOfUpperBound, sumOfLowerBound = 0, 0
        for index, val in enumerate(xColumn.row(row)):
            if index != len(xColumn.row(row)) - 1:
                if val > 0:
                    sumOfUpperBound += val
                elif val < 0:
                    sumOfLowerBound += val
        (
            usableRows1IsMine0IsNot.append(xColumn.row(row))
            if (
                sumOfUpperBound == xColumn.row(row)[len(xColumn.row(row)) - 1]
                and xColumn.row(row)[len(xColumn.row(row)) - 1] == 1
            )
            else (
                usableRows0IsMine1IsNot.append(xColumn.row(row))
                if (
                    sumOfLowerBound == xColumn.row(row)[len(xColumn.row(row)) - 1]
                    and xColumn.row(row)[len(xColumn.row(row)) - 1] == -1
                )
                else ""
            )
        )

        (
            [
                (usableRows0IsMine1IsNot.append(aColumn.row(row)))
                for val in aColumn.row(row)
                if val == 1
            ]
            if aColumn.row(row)[len(aColumn.row(row)) - 1] == 0
            else ""
        )

        sumOfUpperBound = 0
        for index, val in enumerate(aColumn.row(row)):
            if index == len(aColumn.row(row)) - 1:
                continue
            if val > 0:
                sumOfUpperBound += val

        (
            usableRows1IsMine0IsNot.append(aColumn.row(row))
            if (
                sumOfUpperBound == aColumn.row(row)[len(aColumn.row(row)) - 1]
                and aColumn.row(row)[len(aColumn.row(row)) - 1] != 0
            )
            else ""
        )
    isMine, isNotMine = [], []
    for row in usableRows1IsMine0IsNot:
        for index, val in enumerate(row):
            if index == len(row) - 1:
                break
            (
                isMine.append(index)
                if val == 1
                else isNotMine.append(index) if val == -1 else ""
            )
    for row in usableRows0IsMine1IsNot:
        for index, val in enumerate(row):
            if index == len(row) - 1:
                break
            (
                isMine.append(index)
                if val == -1
                else isNotMine.append(index) if val == 1 else ""
            )
    return isMine, isNotMine


def resetTile(tile):
    tile.tileIndexMatrix, tile.probability, tile.counter = -1, 100, 0
    tile.equationMatrix.clear()
    tile.probList.clear()


def revealTilesUsingSets():
    for row in grid:
        for tile in row:
            if tile.minesAroundRemaining <= 0:
                continue
            [[i.removeMines() for i in row] for row in grid]
            tileA, tileB, tileAOnly, tileBOnly = tile, tile, [], []
            nonFlaggedNeighboursForTileA, nonFlaggedNeighboursForTileB = (
                [],
                [],
            )
            for tileANeighbour in tileA.neighbours:
                (
                    nonFlaggedNeighboursForTileA.append(tileANeighbour)
                    if not tileANeighbour.flagged and not tileANeighbour.revealed
                    else ""
                )

                if tileANeighbour.minesAroundRemaining > 0:
                    tileB = tileANeighbour
            (
                setChanged()
                if tileA.minesAroundRemaining == len(nonFlaggedNeighboursForTileA)
                and [t.flag() for t in nonFlaggedNeighboursForTileA].__contains__(True)
                else ""
            )

            if tileB == tileA:
                continue
            [
                nonFlaggedNeighboursForTileB.append(tileBNeighbour)
                for tileBNeighbour in tileB.neighbours
                if not tileBNeighbour.flagged and not tileBNeighbour.revealed
            ]
            [
                tileAOnly.append(nfnftA)
                for nfnftA in nonFlaggedNeighboursForTileA
                if not nonFlaggedNeighboursForTileB.__contains__(nfnftA)
            ]
            [
                tileBOnly.append(nfnftB)
                for nfnftB in nonFlaggedNeighboursForTileB
                if not nonFlaggedNeighboursForTileA.__contains__(nfnftB)
            ]
            (
                (
                    setChanged()
                    if tileA.minesAroundRemaining - tileB.minesAroundRemaining
                    == len(tileAOnly)
                    and (
                        [t.flag() for t in tileAOnly].__contains__(True)
                        or [t.reveal() for t in tileBOnly].__contains__(True)
                    )
                    else ""
                )
                if tileA.minesAroundRemaining > tileB.minesAroundRemaining
                else (
                    (
                        setChanged()
                        if tileB.minesAroundRemaining - tileA.minesAroundRemaining
                        == len(tileBOnly)
                        and (
                            [t.flag() for t in tileBOnly].__contains__(True)
                            or [t.reveal() for t in tileAOnly].__contains__(True)
                        )
                        else ""
                    )
                    if tileA.minesAroundRemaining < tileB.minesAroundRemaining
                    else ""
                )
            )

            (
                setChanged()
                if tile.minesAroundTotal > 0
                and tile.minesAroundRemaining <= 0
                and [t.reveal() for t in tile.neighbours].__contains__(True)
                else ""
            )


sureReveal = lambda: [
    [
        (
            i.removeMines(),
            (
                (i.flagAllNeighbours(), i.removeMines(), setChanged())
                if (
                    i.getUnrevealedNeighbours() == i.minesAroundRemaining
                    and i.minesAroundTotal > 0
                    and i.minesAroundRemaining > 0
                )
                else ""
            ),
            (
                (i.revealAllNeighbours(), i.removeMines(), setChanged())
                if 0 == i.minesAroundRemaining and i.getUnrevealedNeighbours() > 0
                else ""
            ),
        )
        for i in row
        if i.revealed
    ]
    for row in grid
]

flagCount = 0


def incrementFlagCount(amount):
    global flagCount
    flagCount += amount


unrevealedCount = 0


def incrementUnrevealedCount(amount):
    global unrevealedCount
    unrevealedCount += amount


minTile = None


def setMinTile(tile):
    global minTile
    minTile = tile


def finalReveal():
    global flagCount, unrevealedCount, minTile
    # for row in grid:
    #     for tile in row:
    #         if not tile.revealed and not tile.flagged:
    #             tile.reveal()
    #             return
    [
        [
            (
                (
                    (setMinTile(tile), incrementUnrevealedCount(1))
                    if not tile.revealed and not tile.flagged
                    else ""
                ),
                (incrementFlagCount(tile.removeMines()) if tile.revealed else ""),
                (
                    [
                        n.probList.append(
                            tile.minesAroundRemaining / tile.getUnrevealedNeighbours()
                        )
                        for n in tile.neighbours
                        if not n.revealed and not n.flagged
                    ]
                    if tile.revealed and tile.minesAroundRemaining > 0
                    else ""
                ),
            )
            for tile in row
        ]
        for row in grid
    ]
    [
        [
            (
                (
                    tile.probList.append((MINE_COUNT - flagCount) / unrevealedCount)
                    if not tile.revealed and not tile.flagged
                    else ""
                ),
                (
                    (
                        [
                            tile.setProbListAtPos(i, elem / len(tile.probList))
                            for i, elem in enumerate(tile.probList)
                        ],
                        tile.setProbability(sum(tile.probList)),
                        (
                            setMinTile(tile)
                            if (tile.probability < minTile.probability)
                            or (
                                tile.probability == minTile.probability
                                and len(tile.probList) > len(minTile.probList)
                            )
                            else ""
                        ),
                    )
                    if len(tile.probList) > 0
                    else ""
                ),
            )
            for tile in row
        ]
        for row in grid
    ]
    minTile.reveal()


def setChanged():
    global changed
    changed = True


if __name__ == "__main__":
    tr = locateAllOnScreen(
        "C:/Users/joshu/Documents/GitHub/Minesweeper/minesweeper/img/topright.png",
        confidence=0.93,
        grayscale=True,
    )
    try:
        for t in tr:
            BOARD_X[1] = t.left + 20
            BOARD_Y[0] = t.top + 20
    except:
        pass
    bl = locateAllOnScreen(
        "C:/Users/joshu/Documents/GitHub/Minesweeper/minesweeper/img/botleft.png",
        confidence=0.94,
        grayscale=True,
    )
    try:
        for t in bl:
            BOARD_X[0] = t.left + 20
            BOARD_Y[1] = t.top + 20
    except:
        pass
    GRID_DIM[0] = ceil((BOARD_Y[1] - BOARD_Y[0]) / CELL_SIZE)
    GRID_DIM[1] = ceil((BOARD_X[1] - BOARD_X[0]) / CELL_SIZE)

    while not win:
        if keyboard.is_pressed("q"):  # if key 'q' is pressed
            gameOver = True
            break
        time.sleep(1)
        click(BOARD_X[0] + ((BOARD_X[1] - BOARD_X[0]) / 2), 240)
        gameOver = False
        initGrid()
        click(
            (BOARD_X[1] - BOARD_X[0]) / 2 + BOARD_X[0] + 40,
            (BOARD_Y[1] - BOARD_Y[0]) / 2 + BOARD_Y[0],
        )
        scanBoard()
        while not gameOver:
            if keyboard.is_pressed("q"):  # if key 'q' is pressed
                gameOver = True
                break
            scanTh = threading.Thread(target=scanBoard)
            if not scanTh.is_alive():
                scanTh.start()
            if win:
                print("Win")
                gameOver = True
                break
            # [
            #     (
            #         print(),
            #         [
            #             (
            #                 print(
            #                     (
            #                         str(i.minesAroundRemaining)
            #                         if i.revealed
            #                         else "F" if i.flagged else " "
            #                     ),
            #                     end=" ",
            #                 ),
            #             )
            #             for i in row
            #         ],
            #     )
            #     for row in grid
            # ]
            # print()

            changed = False
            sureTh = threading.Thread(target=sureReveal)
            setTh = threading.Thread(target=revealTilesUsingSets)
            if not sureTh.is_alive():
                sureTh = threading.Thread(target=sureReveal)
                sureTh.start()
            if not setTh.is_alive():
                setTh = threading.Thread(target=revealTilesUsingSets)
                setTh.start()
            if not sureTh.is_alive():
                sureTh = threading.Thread(target=sureReveal)
                sureTh.start()
            if not setTh.is_alive():
                setTh = threading.Thread(target=revealTilesUsingSets)
                setTh.start()

            if scanTh.is_alive():
                scanTh.join()
            if not sureTh.is_alive():
                sureTh = threading.Thread(target=sureReveal)
                sureTh.start()
            if not setTh.is_alive():
                setTh = threading.Thread(target=revealTilesUsingSets)
                setTh.start()
            [[(resetTile(i), i.removeMines()) for i in row] for row in grid]

            usableTiles, length = setTileIndexGetUsableRevealedTiles()
            revealTileWithMatrix(createMatrix(usableTiles, length))

            if not scanTh.is_alive():
                scanTh = threading.Thread(target=scanBoard)
                scanTh.start()
            if not sureTh.is_alive():
                sureTh = threading.Thread(target=sureReveal)
                sureTh.start()
            if not setTh.is_alive():
                setTh = threading.Thread(target=revealTilesUsingSets)
                setTh.start()
            if not sureTh.is_alive():
                sureTh = threading.Thread(target=sureReveal)
                sureTh.start()
            if not setTh.is_alive():
                setTh = threading.Thread(target=revealTilesUsingSets)
                setTh.start()

            flagCount, unrevealedCount = 0, 0
            finalReveal() if not changed else ""
        setTh.join()
        sureTh.join()
        scanTh.join()
        if not win:
            print("over")
        win = False
