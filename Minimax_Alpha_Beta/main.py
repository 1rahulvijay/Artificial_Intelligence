from Commands import *
from colorama import Fore
import sys, os
import time


class Start:
    def __init__(self, size, b, x, y):
        self.Size = size
        self.Board = b
        self.X = x
        self.Y = y

    def start_board(self):
        if self.Size % 2 == 0:  # if board size is even
            z = ((self.Size - 2) / 2)
            z = int(z)
            self.Board[z][z] = '2'
            self.Board[self.Size - 1 - z][z] = '1'
            self.Board[z][self.Size - 1 - z] = '1'
            self.Board[self.Size - 1 - z][self.Size - 1 - z] = '2'

    def print_board(self):
        length = len(str(self.Size - 1))
        for y in range(self.Size):
            row = ''
            for x in range(self.Size):
                row += self.Board[y][x]
                row += ' ' * length
            print(row + ' ' + Fore.GREEN + str(y) + Fore.RESET)
        print()
        row = ''
        for x in range(self.Size):
            row += str(x).zfill(length) + ' '
        print(Fore.RED + str(row) + '\n')
        print(Fore.RESET)
# END OF START Class


# Initilization
Size = 8  # Default
Depth = 4  # Default how much depth the computer wants
Board = [['0' for x in range(Size)] for y in range(Size)]

# Driver Code
X = [-1, 0, 1, -1, 1, -1, 0, 1]
Y = [-1, -1, -1, 0, 0, 1, 1, 1]

print('|--------------------------------|Let us Play REVERSI!!|-------------------------------|')
Name = str(input('Please Enter your Name: '))

print("Choose Your Desired Option: ")
print('\n\t1: Human vs Mini-Max Algorithm' + '\n\t2: Human vs Mini-Max & Alpha-Beta Pruning'  + '\n\t3: Mini-Max vs Alpha-Beta Pruning\n')

choice = int(input('Please input your choice: '))

if 0 < choice < 4:
    depthStr = input('Select Search Depth (DEFAULT : 4): ')
    if depthStr != '':
        Depth = int(Depth)
    else:
        print('Invalid Number! ')
        sys.exit(0)

else:
    print('Invalid Number! ')
    sys.exit(0)


print("")
print("\n1: Mini-Max")
print('\n2: '+ Name)


if choice == 3:
    # Creating Objects
    start = Start(Size, Board, X, Y)
    comm = CMD(Board, Size, Depth, X, Y, choice)

    # Fire-up the beast
    start.start_board()

    # Start time
    start_time = time.time()
    min_time = 0
    alpha_time = 0
    while True:
        for p in range(2):

            start.print_board()
            player = str(p + 1)
            print("player: " + player + '\n')
            if comm.is_terminal_node(start.Board, player):
                end_time = time.time()
                print('GAME OVER!!!\n')
                ##Tree()
                print("Time Taken by Min-Max Algorithm: " + str(min_time))
                print("Time Taken by Alpha-Beta Algorithm: " + str(alpha_time))
                print("Total Time Taken to finish the game: " + str(end_time - start_time))
                print('Score Mini_Max: ' + str(comm.eval_board(Board, '1')))
                print('Score Alpha_Beta  : ' + str(comm.eval_board(Board, '2')))
                sys.exit(0)

            if player == '1':  # Mini-Max's turn
                min_time_start = time.time()
                print("Player Name : Mini_Max ")
                (x, y) = comm.ai_best_move(start.Board, player)
                if not (x == -1 and y == -1):
                    (start.Board, disk_remove) = comm.make_move(start.Board, x, y, player)
                    print('Min-Max played X Y : ' + str(x) + ' ' + str(y))
                    print('Disk Removed : ' + str(disk_remove) + '\n')
                    min_time_end = time.time()
                    min_time = min_time + (min_time_end - min_time_start)

            else:  # Alpha-Beta turn
                alpha_time_start = time.time()
                print("Player Name : Alpha Beta ")
                (x, y) = comm.ai_best_move(start.Board, player)
                if not (x == -1 and y == -1):
                    (start.Board, disk_remove) = comm.make_move(start.Board, x, y, player)
                    print('Alpha-Beta played X Y : ' + str(x) + ' ' + str(y))
                    print('Disk Removed : ' + str(disk_remove) + '\n')
                    alpha_time_end = time.time()
                    alpha_time = alpha_time + (alpha_time_end - alpha_time_start)


else:
    # Creating Objects

    start = Start(Size, Board, X, Y)
    comm = CMD(Board, Size, Depth, X, Y, choice)

    # Fire-up the beast
    start.start_board()

    while True:
        for p in range(2):
            start.print_board()
            player = str(p + 1)
            if comm.is_terminal_node(start.Board, player):
                print('Game Over!')
                print('Score User: ' + str(comm.eval_board(Board, '1')))
                print('Score : '+Name + str(comm.eval_board(Board, '2')))
                sys.exit(0)

            if player == '1':  # user's turn
                while True:
                    xy = input('Enter destination in X Y : ')
                    if xy == '':
                        sys.exit(0)
                    (x, y) = xy.split()
                    x = int(x)
                    y = int(y)
                    if comm.valid_move(start.Board, x, y, player):
                        (start.Board, disk_remove) = comm.make_move(start.Board, x, y, player)
                        print('Disk Removed : ' + str(disk_remove))
                        break
                    else:
                        print('Try Again Invalid Move!')
            else:  # AI turn
                print("Player Name : " + Name)
                (x, y) = comm.find_best_move(start.Board, player)
                if not (x == -1 and y == -1):
                    (start.Board, disk_remove) = comm.make_move(start.Board, x, y, player)
                    print('AI played X Y : ' + str(x) + ' ' + str(y))
                    print('Disk Removed : ' + str(disk_remove) + '\n')