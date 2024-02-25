import curses
import random
import time
import pickle


stdscr = curses.initscr()
curses.noecho()
curses.cbreak()
stdscr.keypad(True)
stdscr.nodelay(True)
curses.curs_set(False)
curses.start_color()
# control game pages
status=0

lel=False
testing = True
food_age = 500
char = '✈'
char_food = '★'
char_enemy = '𝧜'
food_number = 10
degre = 0.9
obstacles = 0.1
maxL=curses.LINES-1;
maxC=curses.COLS-1;
score = 0
world=[]
player_l=player_c=0
food = []
enemy=[]

# style game
curses.init_pair(1,curses.COLOR_WHITE,curses.COLOR_BLACK)

# save game
def save_game():
    with open('saved_game.dat', 'wb') as f:
        pickle.dump({
            'player_l': player_l,
            'player_c': player_c,
            'score': score,
            'food': food,
            'enemy': enemy,
            'world':world
        }, f)

# load game
def load_game():
    global player_l, player_c, score, food, enemy,world
    with open('saved_game.dat', 'rb') as f:
        saved_data = pickle.load(f)
        player_l = saved_data['player_l']
        player_c = saved_data['player_c']
        score = saved_data['score']
        food = saved_data['food']
        enemy = saved_data['enemy']
        world = saved_data['world']

# game level
def level():
        stdscr.clear()
        stdscr.addstr(maxL // 2 - 8, maxC // 2 - 6, "Ease")
        stdscr.addstr(maxL // 2 - 6, maxC // 2 - 6, "Normal")
        stdscr.addstr(maxL // 2 - 4, maxC // 2 - 6, "Hard")
        stdscr.refresh()
#  welcome and guide game page
def show_welcome_screen():
    stdscr.clear()
    print(f"degre{degre}")
    stdscr.addstr(maxL // 2 - 8, maxC // 2 -8, "Welcome to the Game!")
    stdscr.addstr(maxL // 2 - 6, maxC // 2 -6, "Press 'r' to start.")
    stdscr.addstr(maxL // 2-4 , maxC // 2 - 4, "'q' to quit.")
    stdscr.addstr(maxL // 2-2 , maxC // 2 - 4, "'L' Load Game.")
    stdscr.refresh()

def random_place():
    a = random.randint(0, maxL)
    b = random.randint(0, maxC)
    while world[a][b] != ' ':  
        a = random.randint(0, maxL)
        b = random.randint(0, maxC)
    return a, b;

# Initializing the game
def init():
    global player_c, player_l,obstacles
    for i in range(-1, maxL+1):
        world.append([])
        for j in range(-1, maxC+1):
            world[i].append(' ' if random.random() > obstacles else '-') 
    for i in range(food_number):
        fl, fc=random_place()
        fa = random.randint(food_age, food_age*5)
        food.append((fl, fc, fa))
    for i in range(3):
        El, Ec=random_place()
        enemy.append((El, Ec))
    player_l, player_c=random_place()
    

# game area
def in_range(a, min, max):
    if a > max:
        return max
    if a<min:
        return min
    
    return a

# draw
def draw():
    if  lel:
        for i in range(maxL):
            for j in range(maxC):
                stdscr.addch(i,j,world[i][j])
        stdscr.addstr(0,0,f"Score: {score} \nSave Game: t\nquit Game: q\nGame Difficulty: {'Ease' if degre == 0.9 else 'Normal' if degre == 0.85 else 'Hard' }" )
        for f in food:
            fl, fc, fa= f
            stdscr.addch(fl, fc, char_food)
        for e in enemy:
            l ,c = e
            stdscr.addch(l, c, char_enemy)
        stdscr.addstr(player_l, player_c, char, curses.color_pair(1))
        stdscr.refresh()

# move character
def move(c):
    global player_l,player_c
    if c =='w' and world[player_l-1][player_c] !='-':
        player_l-=1
    elif c == 's' and world[player_l+1][player_c] !='-':
        player_l+=1
    elif c == 'a' and world[player_l][player_c-1] !='-':
        player_c-=1
    elif c == 'd' and world[player_l][player_c+1] !='-':
        player_c+=1

    player_l = in_range(player_l, 0, maxL)
    player_c = in_range(player_c, 0, maxC)
    



# random move food
def checkfood():
    global score
    for i in range(len(food)):
        fl, fc, fa=food[i]
        fa -= 1
        if fl == player_l and fc == player_c:
            score +=10
            fl, fc = random_place()
            fa = random.randint(1000, 10000)
            curses.beep()
        if fa <= 0 :
            fl, fc = random_place()
            fa = random.randint(1000, 10000)
        food[i] = (fl, fc, fa)

# move enemy
def moveenemy():
    global playing,player_c,player_l
    for i in range(len(enemy)):
        l, c = enemy[i]
        if random.random()>degre:
            if l> player_l:
                l -= 1
        if random.random()>degre:
            if c > player_c:
                c -= 1
        if random.random()>degre:
            if l < player_l:
                l += 1
        if random.random()>degre:
            if c < player_c:
                c += 1
            l += random.choice([0, 1, -1])
            c += random.choice([0, -1, 1])
            l = in_range(l ,0, maxL-1)
            c = in_range(c, 0, maxC-1)
           
            enemy[i] = (l, c)
        if l == player_l and c == player_c and  not testing:
            stdscr.clear()
            stdscr.addstr(maxL//2, maxC//2, f"YOU DIED! SORE: {score}")
            stdscr.refresh()
            time.sleep(3)
            playing = False

show_welcome_screen()

playing=True
while playing:
    try:
        c = stdscr.getkey()
    except:
        c = '';
    # move character
    if c in 'asdw':
        move(c)
    # quit game
    if c == 'q':
        playing=False;
    # start game
    if c == 'r' and status==0:
        status = 1
        level()
    # quit and save game
    if c == 't' :
        save_game()
        playing=False
    # load game
    if c == 'l' and status ==0:
        lel = True
        status = 2
        # init()
        load_game()
    #  ease game level
    if c == 'e' and status ==1:
        obstacles = 0.01
        status = 2
        food_age=500
        food_number=10
        lel=True
        init()
    # normal game level
    elif c == 'n'and status ==1:
        degre = 0.85
        obstacles = 0.03
        food_age =225
        food_number=7
        status = 2
        lel=True
        init()
    # hard gamelevel
    if c == 'h'and status ==1:
        degre = 0.8
        obstacles = 0.06
        food_age=100
        food_number=5
        status = 2
        lel=True
        init()
    checkfood();
    moveenemy(); 
    time.sleep(0.01)
    draw()
stdscr.clear()  
stdscr.addstr(maxL//2, maxC//2 , "thanks for playing!")
stdscr.refresh()
time.sleep(2)
stdscr.clear()
stdscr.refresh()