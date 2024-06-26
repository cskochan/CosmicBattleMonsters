import sys
import pygame
import sqlite3
import random
import shutil


SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 800

DEFAULT_MONSTER_SIZE = (125, 125)
DEFAULT_SATELITE_SIZE = (150, 150)
DEFAULT_PLANET_SIZE = (200, 200)

# Monster, Planet, Tesseract, Force indexes
LIST = (1,543)
MONSTER = (1, 323)
PLANET = (324, 514)
TESSERACT = (515, 523)
FORCE = (524, 531)
TEMPLE = (532, 540)
HUMAN_ID = 1
VAMPIRE_ID = 68
MOON_ID = 324
EARTH_ID = (427, 456, 481, 500)
BLOB_ID = 514
E_TESS_ID = 515
E_FORCE_ID = 524
ENDSTATE_ID = 533
SPORE_ID = 541
CTHULHU_ID = 542
MARS_ID = 543

pygame.init()
pygame.font.init()

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
title_font = pygame.font.SysFont('timesnewroman', 70)
subtitle_font = pygame.font.SysFont('timesnewroman', 55)
button_font = pygame.font.SysFont('timesnewroman', 30)
label_font = pygame.font.SysFont('timesnewroman', 25)
user_text = ''
pygame.display.set_caption("Cosmic Battle Monsters")
bg = pygame.image.load("assets/bg.webp")

#font = pygame.font.SysFont('timesnewroman', 70)
#text = font.render("Monster Time!!", True, (255,255,255))
#textRect = text.get_rect()
#textRect.center = (600, 400)

def main():
    #create_db("cameron")
    #temp()
    main_menu()
    # homekeeping screen
    # place your bets screen
    # battle screen

class Button:
    def __init__(self, text, x, y, position = "center"):
        self.text = text
        self.x = x
        self.y = y
        self.position = position
        self.draw()

    def draw(self):
        button_text = button_font.render(self.text, False, (255,255,255))
        if self.position == "center":
            button_text_rect = button_text.get_rect(center=(self.x, self.y))
        elif self.position == "left":
            button_text_rect = button_text.get_rect(centerleft=(self.x, self.y))
        button_rect = pygame.rect.Rect((self.x, self.y),(200, 60))
        button_rect.center = (self.x, self.y)
        if self.on_click():
            pygame.draw.rect(screen, (115,115,115), button_rect, 0,5)
        else:
            pygame.draw.rect(screen, (64,64,64), button_rect, 0, 5)
        pygame.draw.rect(screen, (255,255,255), button_rect, 2, 5)
        screen.blit(button_text, button_text_rect)

    def on_click(self):
        mouse_pos = pygame.mouse.get_pos()
        left_click = pygame.mouse.get_pressed()[0]
        button_rect = pygame.rect.Rect((self.x, self.y),(200, 60))
        button_rect.center = (self.x, self.y)
        if left_click and button_rect.collidepoint(mouse_pos):
            return True    
        else:
            return False
        
class Text:
    def __init__(self, text, x, y, position = "center", size="label"):
        self.text = text
        self.x = x
        self.y = y
        self.position = position
        self.size = size
        self.draw()

    def draw(self):
        if self.size == "title":
            text = title_font.render(self.text, False, (255,255,255))
        elif self.size == "subtitle":
            text = subtitle_font.render(self.text, False, (255,255,255))
        else:
            text = label_font.render(self.text, False, (255,255,255))
        if self.position == "center":
            text_rect = text.get_rect(center=(self.x, self.y))
        elif self.position == "left":
            text_rect = text.get_rect(topleft=(self.x, self.y))
        elif self.position == "right":
            text_rect = text.get_rect(topright=(self.x, self.y))
        screen.blit(text, text_rect)

class Textfield:
    def __init__(self, text, x, y, length, position = "left", active=True):
        self.text = text
        self.x = x
        self.y = y
        self.length = length
        self.position = position
        self.active = active
        self.draw()

    def draw(self):
        color_active = pygame.Color(50,50,50)
        color_passive = pygame.Color(0,0,0)
        if self.active:
            color = color_active
        else:
            color = color_passive
        textfield = label_font.render(self.text, True, (255,255,255))
        if self.position == "center":
            text_rect = textfield.get_rect(center=(self.x, self.y))
        elif self.position == "left":
            text_rect = textfield.get_rect(topleft=(self.x, self.y))
        textfield_rect = pygame.Rect(self.x - 6, self.y - 5, self.length, 40)
        pygame.draw.rect(screen, color, textfield_rect)
        pygame.draw.rect(screen, (255,255,255), textfield_rect, 2)
        screen.blit(textfield, text_rect)

    def on_click(self):
        mouse_pos = pygame.mouse.get_pos()
        left_click = pygame.mouse.get_pressed()[0]
        textfield_rect = pygame.rect.Rect((self.x-6, self.y-5),(self.length, 40))
        if left_click and textfield_rect.collidepoint(mouse_pos):
            return True
        else:
            return False



def main_menu():
    run = True
    screen.blit(bg, (0,0))
    Text("Cosmic Battle Monsters!!", 600, 200, size="title")
    while run:
        
        newGame = Button("New Game", 600, 400)
        savedGame = Button("Load Save", 600, 500)
        

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if newGame.on_click():
                    new_game()
                elif savedGame.on_click():
                    saved_games()
        pygame.display.update()
    pygame.quit()
    sys.exit()

def new_game():
    global user_text
    fn_field_active = True
    run = True
    while run:
        screen.blit(bg, (0,0))
        Text("New Game", 600, 200, size="subtitle")
        Text("Save game as: ", 545, 400, position="right")
        filename = Textfield(user_text, 555, 400, 300, position="left", active = fn_field_active)
        submit = Button("Submit", 600, 700)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN and fn_field_active:
                if event.key == pygame.K_BACKSPACE:
                    user_text = user_text[:-1]
                elif event.key == pygame.K_RETURN:
                    create_db(user_text)
                    intro()
                else:
                    if len(user_text) <= 12:
                        user_text += event.unicode
            if event.type == pygame.MOUSEBUTTONDOWN:
                if filename.on_click():
                    fn_field_active = True
                else:
                    fn_field_active = False
                if submit.on_click():
                    create_db(user_text)
                    intro()
        pygame.display.update()
    pygame.quit()
    sys.exit()

def saved_games():
    run = True
    while run:
        screen.blit(bg, (0,0))
        Text("Existing Game", 600, 200, size="subtitle")

        Text("Load Game: ", 600, 400)
        

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                user_text += event.unicode
        pygame.display.update()
    pygame.quit()
    sys.exit()

def intro():
    print("finally playing the game")

def home_keeping():
    pass

def card_and_bet():
    pass

def battle():
    pass

def game_over():
    pass

def credits():
    pass

def button(message, pos):
    text = pygame.font.SysFont('timesnewroman', 35).render(message, True, (255,255,255))
    button = text.get_rect(center=(pos[0],pos[1]))
    #button = pygame.Rect(200,200,110,60)
    return (text, button)





def display():
    screen.blit(bg,(0,0))

    l_observer = pygame.image.load(f"Assets/Images/516.webp").convert_alpha()
    r_observer = pygame.image.load(f"Assets/Images/518.webp").convert_alpha()
    plr = pygame.image.load(f"Assets/Images/427b.webp").convert_alpha()
    pl_mon = pygame.image.load(f"Assets/Images/001.webp").convert_alpha()
    comp = pygame.image.load(f"Assets/Images/416.webp").convert_alpha()
    comp_mon = pygame.image.load(f"Assets/Images/040.webp").convert_alpha()

    plr = pygame.transform.scale(plr, DEFAULT_PLANET_SIZE)
    pl_mon = pygame.transform.scale(pl_mon, DEFAULT_MONSTER_SIZE)
    comp = pygame.transform.scale(comp, DEFAULT_PLANET_SIZE)
    comp = pygame.transform.flip(comp, True, False)
    comp_mon = pygame.transform.scale(comp_mon, DEFAULT_MONSTER_SIZE)
    comp_mon = pygame.transform.flip(comp_mon, True, False)


    screen.blit(l_observer, (300, 50))
    screen.blit(r_observer, (644, 50))
    screen.blit(plr, (100,425))
    screen.blit(pl_mon, (450, 625))
    screen.blit(comp, (900,425))
    screen.blit(comp_mon, (625,625))
    screen.blit(text, textRect)





#BEGIN TEMP
def temp():
    # static_list = [None]*3
    # conn = sqlite3.connect('static.db')
    # cur = conn.cursor()
    # cur.execute('''CREATE TABLE IF NOT EXISTS creatures
    #             (ID INT, NAME TEXT, HABITABILITY TEXT)''')
    # conn.commit()
    # for i in range(LIST[0], LIST[1]+1):
    #     static_list[0] = i
    #     cur.execute('''INSERT INTO stats VALUES (?,?,?)''', static_list)

    stats_list = [None]*44
    conn = sqlite3.connect('stats.db')
    cur = conn.cursor()
    with open("template.sql", "r") as file:
        sql_script = file.read()
    cur.executescript(sql_script)
    for i in range(LIST[0], LIST[1]+1):
        stats_list[0] = i
        if i >= TESSERACT[0]+1 and i < TESSERACT[1]+1:
            stats_list[1] = 530
            cur.execute('''INSERT INTO creatures VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
                    ''', stats_list)
            stats_list[1] = 531
            cur.execute('''INSERT INTO creatures VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
                    ''', stats_list)
            stats_list[1] = None
        else:
            cur.execute('''INSERT INTO creatures VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
                    ''', stats_list)
    
    
    hab_stat = habitability()
    cur.executemany('''UPDATE creatures SET NAME = ? WHERE ID = ?''', (name()))
    cur.executemany('''UPDATE creatures SET HABITABILITY = ? WHERE ID = ?''', (hab_stat))

    cur.execute("SELECT * FROM creatures ORDER BY ID")
    for stats in cur:
        print("Monster: ", stats)

    conn.commit()
    cur.close()
    conn.close()
#END TEMP


def create_db(new_fn):
    # stats_list = [None]*43
    # conn = sqlite3.connect('stats.db')
    # cur = conn.cursor()
    # with open("template.sql", "r") as file:
    #     sql_script = file.read()
    # cur.executescript(sql_script)
    # for i in range(LIST[0], LIST[1]+1):
    #     stats_list[0] = i
    #     cur.execute('''INSERT INTO creatures VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
    #                 ''', stats_list)
    shutil.copyfile('Assets/stats.db', f'Assets/SavedGames/{new_fn}.db')

    conn = sqlite3.connect(f'{new_fn}.db')
    cur = conn.cursor()

    
    pwr_stat = power() # save pwr_stat for HP
    hp_stat = hp(pwr_stat) # save hp_stat for MELEE_LOW, MELEE_HIGH
    defence_stat = defence(pwr_stat) # save defense_stat for ACCURACY_LOW, ACCURACY_HIGH
    melee_stat = melee_atk(hp_stat) # save melee_stat for RANGED_LOW, RANGED_HIGH

    hab_stat = []
    cur.execute("SELECT HABITABILITY, ID FROM creatures")
    for hab, id in cur:
        hab_stat.append((hab, id))

    #hab_stat = habitability() # save hab_stat for OWNER
    max_pop_stat = max_pop(pwr_stat) # save max_pop_stat for POP
    type_stat = biome_type() # save type_stat for OWNER, BIO_01 - BIO_15
    biome_stat = biome(type_stat) # save biome_stat for BIO_01 - BIO-15
    
    cur.executemany('''UPDATE creatures SET OWNER = ? WHERE ID = ?''', (owner(type_stat, hab_stat)))
    cur.executemany('''UPDATE creatures SET OWN_PERCENT = ? WHERE ID = ?''', (own_percent()))
    #cur.executemany('''UPDATE creatures SET NAME = ? WHERE ID = ?''', (name()))
    # EXTINCTION should remain as null until creature goes extinct
    cur.executemany('''UPDATE creatures SET PWR = ? WHERE ID = ?''', (pwr_stat))
    cur.executemany('''UPDATE creatures SET HP = ? WHERE ID = ?''', (hp_stat))
    cur.executemany('''UPDATE creatures SET DEF = ? WHERE ID = ?''', (defence_stat))
    cur.executemany('''UPDATE creatures SET ACCURACY_LOW = ?, ACCURACY_HIGH = ? WHERE ID = ?''', (accuracy(defence_stat)))
    cur.executemany('''UPDATE creatures SET MELEE_LOW = ?, MELEE_HIGH = ? WHERE ID = ?''', (melee_stat))
    cur.executemany('''UPDATE creatures SET RANGED_LOW = ?, RANGED_HIGH = ? WHERE ID = ?''', (ranged_atk(melee_stat)))
    cur.executemany('''UPDATE creatures SET CRIT = ? WHERE ID = ?''', (crit()))
    cur.executemany('''UPDATE creatures SET GROWTH_RATE = ? WHERE ID = ?''', (growth_rate(pwr_stat)))
    cur.execute('''UPDATE creatures SET MOTIVATION = ? WHERE ID = ?''', (0, HUMAN_ID))
    cur.execute('''UPDATE creatures SET KENNEL_TIMER = ? WHERE ID = ?''', (0, EARTH_ID[0]))
    cur.executemany('''UPDATE creatures SET KENNEL_COUNT = ? WHERE ID = ?''', (kennel_count()))
    #cur.executemany('''UPDATE creatures SET HABITABILITY = ? WHERE ID = ?''', (hab_stat))
    cur.executemany('''UPDATE creatures SET TEMPLE_PWR = ? WHERE ID = ?''', (temple_power()))
    cur.executemany('''UPDATE creatures SET MAX_POP = ? WHERE ID = ?''', (max_pop_stat))
    cur.executemany('''UPDATE creatures SET POP = ? WHERE ID = ?''', (population(max_pop_stat)))
    cur.executemany('''UPDATE creatures SET BIOME_TYPE = ? WHERE ID = ?''', (type_stat))
    for i in biome_stat:
        cur.execute('''UPDATE creatures SET BIO_01 = ? WHERE ID = ?''', (i[0][0],i[1]))
        cur.execute('''UPDATE creatures SET BIO_02 = ? WHERE ID = ?''', (i[0][1],i[1]))
        cur.execute('''UPDATE creatures SET BIO_03 = ? WHERE ID = ?''', (i[0][2],i[1]))
        cur.execute('''UPDATE creatures SET BIO_04 = ? WHERE ID = ?''', (i[0][3],i[1]))
        cur.execute('''UPDATE creatures SET BIO_05 = ? WHERE ID = ?''', (i[0][4],i[1]))
        cur.execute('''UPDATE creatures SET BIO_06 = ? WHERE ID = ?''', (i[0][5],i[1]))
        cur.execute('''UPDATE creatures SET BIO_07 = ? WHERE ID = ?''', (i[0][6],i[1]))
        cur.execute('''UPDATE creatures SET BIO_08 = ? WHERE ID = ?''', (i[0][7],i[1]))
        cur.execute('''UPDATE creatures SET BIO_09 = ? WHERE ID = ?''', (i[0][8],i[1]))
        cur.execute('''UPDATE creatures SET BIO_10 = ? WHERE ID = ?''', (i[0][9],i[1]))
        cur.execute('''UPDATE creatures SET BIO_11 = ? WHERE ID = ?''', (i[0][10],i[1]))
        cur.execute('''UPDATE creatures SET BIO_12 = ? WHERE ID = ?''', (i[0][11],i[1]))
        cur.execute('''UPDATE creatures SET BIO_13 = ? WHERE ID = ?''', (i[0][12],i[1]))
        cur.execute('''UPDATE creatures SET BIO_14 = ? WHERE ID = ?''', (i[0][13],i[1]))
        cur.execute('''UPDATE creatures SET BIO_15 = ? WHERE ID = ?''', (i[0][14],i[1]))
    cur.executemany('''UPDATE creatures SET IMAGE_HUE = ? WHERE ID = ?''', (image_hue()))
    cur.executemany('''UPDATE creatures SET TOP_MARGIN = ? WHERE ID = ?''', (top_margin()))
    # for i in range(LIST[0], 11):
    #     cur.execute('''UPDATE creatures SET IMAGE = ? WHERE ID = ?''', (image(i), i))
    # cur.execute('''UPDATE creatures SET IMAGE_ALT = ? WHERE ID = ?''', (image(HUMAN_ID, 'b'), HUMAN_ID))
    # cur.execute('''UPDATE creatures SET IMAGE_ALT = ? WHERE ID = ?''', (image(MOON_ID, 'b'), MOON_ID))
    # cur.execute('''UPDATE creatures SET IMAGE_ALT2 = ? WHERE ID = ?''', (image(MOON_ID, 'c'), MOON_ID))
    
    cur.execute("SELECT * FROM creatures ORDER BY id")
    for creature in cur:
        print("Monster: ", creature)
        

    conn.commit()
    cur.close()
    conn.close()

# BEGIN create_db() helper functions
def owner(biome, habitability):
    tup_list = []
    mon_biome = biome[:323]
    planet_biome = biome[323:]
    mon_list = [[] for _ in range(15)]
    plan_list = [[] for _ in range(15)]
    for i in mon_biome:
        mon_list[i[0]].append(i[1])
    for i in planet_biome:
        if not any((i[1] == MOON_ID, i[1] == EARTH_ID[0], i[1] == EARTH_ID[1], i[1] == EARTH_ID[2], i[1] == EARTH_ID[3])):
            for j in habitability:
                if i[1] in j:
                    plan_list[i[0]].append(i[1])
    for i in range(15):
        for j in range(len(mon_list[i])):
            if mon_list[i][j] == HUMAN_ID or mon_list[i][j] == VAMPIRE_ID:
                tup_list.append((EARTH_ID[0], mon_list[i][j]))
            else:
                tup_list.append((plan_list[i][j%len(plan_list[i])], mon_list[i][j]))
    return tup_list

def own_percent():
    tup_list = []
    for i in range(MONSTER[0], PLANET[1]+1):
        tup_list.append((1.0, i))
    for i in range(TESSERACT[0], TESSERACT[1]+1):
        tup_list.append((.5, i))
    return tup_list

def name():
    print("We Get Here")
    tup_list = []
    with open("Assets/origname.txt", "r") as file:
        for i in range(LIST[0], LIST[1]+1):
            tup_list.append((next(file).strip(), i))
    return tup_list

def power():
    tup_list = []
    for i in range(MONSTER[0], PLANET[1]+1):
        tup_list.append((random.uniform(i, (i+2) * 1.2), i))
    tup_list[0] = (1.0, 1) # Human's have set initial power
    #tup_list[426] = (426.0, 426) # Earth has set initial power
    return tup_list

def hp(power):
    tup_list = []
    for i in power: # power -> (power, id)
        tup_list.append(((i[0] + 2)*1.7, i[1]))
    return tup_list

def defence(power):
    tup_list = []
    for i in power: # power -> (power, id)
        tup_list.append(((i[0]/384, i[1])))
    return tup_list

def accuracy(defence):
    tup_list = []
    for i in defence: # defense -> (defense, id)
        tup_list.append(((i[0]/2, i[0]*2, i[1])))
    return tup_list

def melee_atk(hp):
    tup_list = []
    for i in hp: # hp -> (hp, id)
        tup_list.append((i[0]/5, i[0]/4, i[1]))
    return tup_list

def ranged_atk(melee):
    tup_list = []
    for i in melee: # melee -> (melee low, melee high, id)
        tup_list.append((.6 * i[0], .6 * i[1], i[2]))
    return tup_list

def crit():
    tup_list = []
    for i in range(MONSTER[0], PLANET[1]+1):
        tup_list.append((0.01, i))
    return tup_list

def growth_rate(power):
    tup_list= []
    for i in power: # power -> (power, id)
        tup_list.append((.16-((i[0]/450)*.16), i[1]))
    return tup_list

def kennel_count():
    tup_list = []
    for i in range(PLANET[0], PLANET[1]+1):
        tup_list.append((0, i)) # all planets start with 0 kennels
    return tup_list

def habitability():
    tup_list = []
    with open("Assets/sat_infest.txt", "r") as file:
        for i in range(PLANET[0], PLANET[1]):
            if next(file).strip() == "Inhabitable":
                tup_list.append((1, i))
    return tup_list

def temple_power():
    tup_list = []
    for i in range(PLANET[0], PLANET[1]+1):
        tup_list.append((0, i))
    return tup_list

def max_pop(power):
    tup_list = []
    for i in power: # power -> (power, id)
        if i[1] in range(MONSTER[0], MONSTER[1]+1):
            tup_list.append((5070307-(10703*int(i[0])), i[1]))
    return tup_list

def population(max_pop):
    tup_list = []
    for i in max_pop:
        if i[1] in range(MONSTER[0], MONSTER[1]+1):
            tup_list.append((int(i[0]/2), i[1]))
    return tup_list

def biome_type():
    tup_list = []
    type_list = [None]*515
    for i in range(MONSTER[0]-1, PLANET[1]+1):
        type_list[i] = i%15
    M_type = type_list[:323]
    P_type = type_list[324:]
    random.shuffle(M_type)
    random.shuffle(P_type)
    M_type[HUMAN_ID-1] = 8 # human
    M_type[VAMPIRE_ID-1] = 8 # vampire 
    P_type[EARTH_ID[0]-323] = 8 # earth
    P_type[MOON_ID-323] = 3 # moon
    print(len(M_type))
    print(len(P_type))
    print("------")
    type_list = M_type + P_type

    for i in range(len(type_list)):
        tup_list.append((type_list[i], i+1))

    return tup_list

def biome(biome):
    tup_list = []
    biome_list = [None]*15
    for i in biome:
        if i[1] <= 323:
            rng_pwr = ((i[1]//65)+2)/2
            rand_rng = .05
        else:
            rng_pwr = 1
            rand_rng = .1
        for j in range(0,15):
            if j==i[0]:
                biome_list[j] = random.uniform(.95-rand_rng, 1.0)
                #biome_list[j] = 1.0
            elif any([j==i[0]+1, j==i[0]-1, j==i[0]+6, j==i[0]-6]):
                biome_list[j] = random.uniform(.66-rand_rng, .66+rand_rng)**rng_pwr
                #biome_list[j] = .66
            elif any([j==i[0]+5, j==i[0]-5, j==i[0]+7, j==i[0]-7]):
                biome_list[j] = random.uniform(.5-rand_rng, .5+rand_rng)**rng_pwr
                #biome_list[j] = .5
            elif any([j==i[0]+2, j==i[0]-2, j==i[0]+12, j==i[0]-12]):
                biome_list[j] = random.uniform(.33-rand_rng, .33+rand_rng)**rng_pwr
                #biome_list[j] = .33
            elif any([j==i[0]+4, j==i[0]-4, j==i[0]+8, j==i[0]-8, j==i[0]+11, j==i[0]-11, j==i[0]+13, j==i[0]-13]):
                biome_list[j] = random.uniform(.15-rand_rng, .15+rand_rng)**rng_pwr
                #biome_list[j] = .15
            else:
                biome_list[j] = random.uniform(0, 0+rand_rng)
                #biome_list[j] = 0
        if i[1] <= 323:
            tup_list.append((biome_list, i[1]))
        else:
            tup_list.append((planet_percent(biome_list), i[1]))
    return tup_list

def planet_percent(list):
    n = sum(list)
    m = [0]*15
    for i in range(0,15):
        m[i] = list[i]/n
    return m
    
def image_hue():
    tup_list = []
    for i in range(MONSTER[0], PLANET[1]+1):
        tup_list.append((0, i)) # all monsters start with 0 hue shift
    return tup_list

def top_margin():
    tup_list = []
    for i in range(LIST[0], LIST[1]+1):
        tup_list.append((0, i))
    return tup_list

def image(id, alt=""):
    fn = f"Assets/Images/{id:03d}{alt}.webp"
    with open(fn, 'rb') as file:
        blobData = file.read()
    return blobData
# END create_db() helper functions






if __name__ == "__main__":
    main() 