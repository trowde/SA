import pygame
import random
import math

pygame.init()
#pygame.mixer.init()


#SCREEN_SIZE
SCREEN_WIDTH=1024
SCREEN_HEIGHT=1024
SCREEN_LEFT_BOUNDARY=0
SCREEN_RIGHT_BOUNDARY=SCREEN_WIDTH
SCREEN_UP_BOUNDARY=0
SCREEN_DOWN_BOUNDARY=SCREEN_HEIGHT

NUMBER_OF_FORMULA=4
RED=(255,0,0)

#initiate
screen=pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
pygame.display.set_caption('group_game')
background=[pygame.image.load('level1.jpg'),pygame.image.load('level2.jpg'),pygame.image.load('level3.jpg')]
music=['level1.mp3','level2.mp3']
play_index=0
#level1_music=pygame.music.load("level1.mp3")
image=pygame.image.load("player123.png")
image.set_colorkey((255,255,255))
#font
font=pygame.font.Font(None,36)


#pygame.mixer.music.load(music[play_index])
#pygame.mixer.music.play(-1)

class player_figure():

    @staticmethod
    def create(x,y):
        screen.blit(image, (x+25, y+25)) 

#player.initiate
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.position_X=SCREEN_WIDTH/2       
        self.position_Y=SCREEN_HEIGHT-200
        #self.image=pygame.image.load('player.png')
        self.width=50
        self.height=50
        self.speed=3.5
        self.number=1
        self.rect=pygame.Rect(self.position_X+25,self.position_Y-25,0,0)
    def draw_player(self,x,y,num):
        text=f"{self.number}"
        number_render=font.render(text,True,(255,0,0))
        screen.blit(number_render,(x+20,y-25))
        self.rect=pygame.Rect(x,y,50,50)
        #for i in range(self.number):
        #player_figure.create(x,y)
        #pygame.draw.rect(screen,RED,(x+10,y+10,5,20))

    def move(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.position_X-=self.speed;
        if keys[pygame.K_RIGHT]:
            self.position_X+=self.speed;
        if keys[pygame.K_UP]:
            self.position_Y-=self.speed;
        if keys[pygame.K_DOWN]:
            self.position_Y+=self.speed;

        #if self.position_X+self.width<SCREEN_LEFT_BOUNDARY:
         #   self.position_X=SCREEN_RIGHT_BOUNDARY
        #if self.position_X > SCREEN_RIGHT_BOUNDARY:  
         #   self.position_X=SCREEN_LEFT_BOUNDARY-self.width
        #if self.position_X < SCREEN_LEFT_BOUNDARY: 
          #  screen.blit(self.image, (self.position_X + SCREEN_WIDTH, self.position_Y))
       # elif self.position_X + self.width > SCREEN_RIGHT_BOUNDARY:  
           # screen.blit(self.image, (self.position_X - SCREEN_WIDTH, self.position_Y))

class Formula(pygame.sprite.Sprite):
    current_index=0
    number=4
    speed=2
    width=20
    height=20
    operator=['+','-','*','/']
    def __init__(self,x,y,a,b):
        super().__init__()
        self.position_X=x
        self.position_Y=y
        self.value=a
        self.operator=b
        self.text=f"{self.operator}{self.value}"
        self.rect=pygame.Rect(x,self.position_Y,125,50)
    def formula_reset(self):
        self.operator=Formula.operator[random.randint(0,3)]
        self.value=random.randint(1,10)
        self.position_Y=-50
        self.text=f"{self.operator}{self.value}"
    @staticmethod
    def formula_move(x,y,text,formula):
        pygame.draw.rect(screen,(255,0,0),pygame.Rect(x,y,125,50),2)
        formula_render=font.render(text,True,(255,0,0))
        screen.blit(formula_render,(x+20,y+25))
        formula.rect=pygame.Rect(x,y,125,50)

    




class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()



class Other(pygame.sprite.Sprite):
    background_speed=2
    background_position=0
    norm=0 
    @staticmethod
    def background_move(y,play_index):
            screen.blit(background[play_index],(0,y))
            screen.blit(background[play_index],(0,-1000+y))
    @staticmethod
    def background_alter(y,play_index):
         screen.blit(background[play_index-1],(0,y))
         screen.blit(background[play_index],(0,-1000+y))



player=Player()
other=Other()
formulas=[]
for i in range(4):
    formulas.append(Formula(i*SCREEN_WIDTH/NUMBER_OF_FORMULA,-50,random.randint(1,10),Formula.operator[random.randint(0,3)]))

clock = pygame.time.Clock()
running=True
while running:


    for i in range(4):
        if player.rect.colliderect(formulas[i].rect):
            if formulas[i].operator=='+':
                player.number+=formulas[i].value
            elif formulas[i].operator=='-':
                player.number-=formulas[i].value
            elif formulas[i].operator=='*':
                player.number*=formulas[i].value
            elif formulas[i].operator=='/':
                player.number/=formulas[i].value
            Formula.current_index+=1
            if play_index<=2:
                if Formula.current_index>=5:
                    Formula.current_index-=5
                    play_index+=1
            for j in range(4):
                formulas[j].formula_reset()
            break
    if Formula.current_index>0|(play_index==0):
         Other.background_move(Other.background_position,play_index)    
    else: 
         other.background_alter(Other.background_position,play_index)
    Other.background_position+=Other.background_speed
    if Other.background_position>1000:
        Other.background_position=0

    
    for i in range(NUMBER_OF_FORMULA):
        Formula.formula_move(formulas[i].position_X,formulas[i].position_Y,formulas[i].text,formulas[i])
        formulas[i].position_Y+=Formula.speed
    


    #player_figure.create(250,500)
    player.draw_player(player.position_X,player.position_Y,player.number)
    player.move()
    if player.number<=0:
        running=False
    for event in pygame.event.get():
        if event.type ==pygame.QUIT:
            running=False

   
    clock.tick(60) 
    pygame.display.update()