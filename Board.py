from PlayerPos import *
from math import sqrt
from pylab import *
import time
import random


player = Players([[0 for i in range(30)] for j in range(30)], True)
playerx = 14
playery = 15
score = 0
pastpos = [playerx, playery]
monsters = []

def refresh_game():
    del monsters[:]
    global playerx
    global playery
    playerx, playery = 14, 15
    copygrid()
    player.alive = True


def copygrid():
    for monster in monsters:
        player.grid[monster[0]][monster[1]] = 7
    player.grid[playerx][playery] = 3


copygrid()


def spawn():
    c = randint(0, 6)
    if c == 0:
        monsters.append([0, 0])
    elif c == 1:
        monsters.append([0, 29])
    elif c == 2:
        monsters.append([29, 29])
    elif c == 3:
        monsters.append([29, 0])


def move(monster):
    c = int((random.random() * 100) % 6)
    if c == 5:
        if playerx - monster[0] >= playery - monster[1] > 0:
            if monster[0] + 1 == playerx and monster[1] == playery:
                player.alive = False
            monster[0] += 1
        elif playery - monster[1] >= playerx - monster[0] > 0:
            if monster[0] == playerx and monster[1] + 1 == playery:
                player.alive = False
            monster[1] += 1
        elif 0 > playery - monster[1] >= playerx - monster[0]:
            if monster[0] - 1 == playerx and monster[1] == playery:
                player.alive = False
            monster[0] -= 1
        elif 0 > playerx - monster[0] >= playery - monster[1]:
            if monster[0] == playerx and monster[1] - 1 == playery:
                player.alive = False
            monster[1] -= 1
    else:
        if c == 0 and monster[0] <= 28:
            if monster[0] + 1 == playerx and monster[1] == playery:
                player.alive = False
            monster[0] += 1
        elif c == 1 and monster[1] <= 28:
            if monster[0] == playerx and monster[1] + 1 == playery:
                player.alive = False
            monster[1] += 1
        elif c == 2 and monster[0] >= 1:
            if monster[0] - 1 == playerx and monster[1] == playery:
                player.alive = False
            monster[0] -= 1
        elif c == 3 and monster[1] >= 1:
            if monster[0] == playerx and monster[1] - 1 == playery:
                player.alive = False
            monster[1] -= 1

def anticheat(pastx, pasty, currx, curry):
    if sqrt((currx-pastx) ** 2 + (curry-pasty) ** 2) != 1:
        sys.exit("VAC Banned")


def gridEdit(i, j, val):
    global playerx
    global playery
    if (i > 28 and val[0] == 1) or (j > 28 and val[1] == 1) or (i == 0 and val[0] == -1) or (j == 0 and val[1] == -1):
        player.alive = False
    else:
        for monster in monsters:
            if monster[0] == playerx + val[0] and monster[1] == playery + val[1]:
                player.alive = False
        else:
            pastpos = [playerx, playery]
            playerx += val[0]
            playery += val[1]
            anticheat(pastpos[0], pastpos[1], playerx, playery)


def fast_play():
    score, alive = 0, True
    for p in range(100):
        while alive:
            spawn()
            for monster in monsters:
                player.grid[monster[0]][monster[1]] = 0
                move(monster)
            player.grid[playerx][playery] = 0
            gridEdit(playerx, playery, player.move_player())
            copygrid()
            score += 1
            alive = player.alive
        refresh_game()
        alive = player.alive
    print("Your score is:", score)


def slow_play():
    score, alive = 0, True

    plt.style.use('dark_background')
    plt.figure(1)
    plt.title('EfreiZ Slow Simulation')
    plt.xlabel('By Nathan Rousselot')
    plt.grid(False)
    plt.show(block=False)

    while alive:
        spawn()
        for monster in monsters:
            player.grid[monster[0]][monster[1]] = 0
            move(monster)
        player.grid[playerx][playery] = 0
        gridEdit(playerx, playery, player.move_player())
        copygrid()
        plt.imshow(player.grid, interpolation='nearest')
        plt.pause(0.1)

        score += 1
        alive = player.alive
    print("Your score is:", score)


def play(play):
    if play == 'slow':
        slow_play()
    elif play == 'fast':
        fast_play()
    else:
        print("Stop being dumb plz.")
        return (None)

# start = time.time()
play(plays())
# end = time.time()
# print(end - start)