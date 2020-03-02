# vacuum cleaner example from AIMA
# Author: Dylan Rosser

# This program will create an array representing the environment
# clean spaces will be represented by a 0
# dirty spaces will be represented by a 1
# The vacuum moves randomly. It has no memory of where
# it has been. It will stop after finding no dirt a set number of times

import numpy as np

# change to false if you want to ignore the prompts and just set variables
# or go look at the jupyter notebook
Verbose = True

if not Verbose:
    es = 4
    dirtn = 10
    start = 6


class Agent:
    def __init__(self, location, es):
        self.location = location
        self.action = 'nothing'
        self.opts = []
        self.performance = 0
        self.num_moves = 0
        self.num_cleaned = 0
        self.mv = None


    def check_if_dirty(self, env):
        if env[vacuum.location[0],vacuum.location[1]] == 1:
            self.action = 'suck'
            self.performance +=10
            env[vacuum.location[0],vacuum.location[1]] = 0
            self.num_cleaned += 1
        else:
            self.action = 'nothing'
            env = env
        return env

    def get_move_options(self):
        self.opts = ['L', 'U', 'R', 'D']
        if self.location[1] == 0: # cant move left
            i = self.opts.index('L')
            self.opts.pop(i)
        if self.location[1] == es-1: # cant move right
            i = self.opts.index('R')
            self.opts.pop(i)
        if self.location[0] == 0: # cant move up
            i = self.opts.index('U')
            self.opts.pop(i)
        if self.location[0] == es-1: # cant move down
            i = self.opts.index('D')
            self.opts.pop(i)





    def mv_left(self):
        self.location =  [self.location[0], self.location[1]-1]
        self.performance -= 1
        self.num_moves += 1

    def mv_right(self):
        self.location = [self.location[0], self.location[1]+1]
        self.performance -= 1
        self.num_moves += 1

    def mv_up(self):
        self.location = [self.location[0]-1, self.location[1]]
        self.performance -= 1
        self.num_moves += 1

    def mv_down(self):
        self.location = [self.location[0]+1, self.location[1]]
        self.performance -= 1
        self.num_moves += 1

    def show_location(self):
        e = np.full((es,es), '0')
        e[vacuum.location[0],vacuum.location[1]] = 'X'
        print(e)

    def decide_move(self): #randomly
        num_opts = len(self.opts)
        n = np.random.randint(0, num_opts)
        self.mv = self.opts[n]


if (Verbose):
    # prompt human for size of the grid environment: es = envirnment size
    while True:
        try:
            es = abs(int(input("Please enter an integer n to create an n x n environment ")))
            break
        except ValueError:
            print("Invalid entry!")

    #print(type(es))
    #grid = np.zeros([es, es], dtype=np.int)
    #print(grid)

    # getting starting location of the vacuum from human

    while True:
        try:
            start = abs(int(input("Please enter the starting posistion of the agent. This should be an integer between 1 and {} ".format(es**2))))
            if start > es**2:
                print('Starting position can not exceed {}! Setting start to default'.format(es**2))
                start = 1
            break
        except ValueError:
            print("Invalid entry!")

    #print(start)

    # get dirt from human
    while True:
        try:
            dirtn = abs(int(input("Please specify the number of dirty locations between 0 and {} ".format(es**2))))
            if dirtn > es**2:
                print("Dirty locations exceeds environment! Setting to 50%")
                dirtn = es**2/2
            break
        except ValueError:
            print("Invalid entry!")

#print(dirtn)

def encode_loc(n):
    j = (n%es+3)%es
    i = (n-j+1)%es
    return i,j

def decode_loc(i,j):
    loc = i * es + j + 1
    return loc

# initialize the environment
z = np.zeros(es*es, dtype=np.int)
#print(z)
index = list(np.arange(es*es))
#print(index)

while len(index) > es*es - dirtn:
    i = np.random.randint(0, len(index))
    n = index[i]
    z[n] = 1
    index.pop(i)

env = z.reshape(es,es)

#print(env)

x,y = encode_loc(start)


# initialize the Agent
vacuum = Agent([x,y], es)

num_nothings = 0 # count cosecutive non-suck actions

print('Starting environment: \n\n', env)
print('\nVacuum location: \n\n')
vacuum.show_location()

# it may be neccesary to increase num_nothings for a large space

while num_nothings < 10:
    env = vacuum.check_if_dirty(env)
    print('\nVacuum Action: ', vacuum.action)
    vacuum.get_move_options()
    #print(vacuum.opts)
    vacuum.decide_move()
    print('\nThe vacuum will move ', vacuum.mv)

    if vacuum.mv == 'L': vacuum.mv_left()
    elif vacuum.mv == "R": vacuum.mv_right()
    elif vacuum.mv == "U": vacuum.mv_up()
    elif vacuum.mv == "D": vacuum.mv_down()

    print('\nEnvironment: \n\n', env)
    print('\nVacuum location: \n')
    #print(vacuum.location)
    vacuum.show_location()

    if vacuum.action == 'nothing':
        num_nothings +=1
    else: num_nothings = 0

print('Performance Score: ', vacuum.performance)
print('Total number of moves: ', vacuum.num_moves)
print('Total number of sucking actions: ', vacuum.num_cleaned)

if dirtn != vacuum.num_cleaned:
    print('The vacuum stopped before cleaning all the spaces. Try decreasing the size of the environment or '
                'increasing the stopping criteria num_nothings')
else:
    print("The vacuum cleaned all the spaces")
