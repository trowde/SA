import pygame
import random
import math

pygame.init()
pygame.mixer.init()


#SCREEN_SIZE
SCREEN_WIDTH=1024
SCREEN_HEIGHT=1024
SCREEN_LEFT_BOUNDARY=0
SCREEN_RIGHT_BOUNDARY=SCREEN_WIDTH
SCREEN_UP_BOUNDARY=0
SCREEN_DOWN_BOUNDARY=SCREEN_HEIGHT



NUMBER_OF_FORMULA=4
RED=(255,0,0)
WHITE=(255,255,255)
BLACK=(0,0,0)

#initiate
screen=pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
pygame.display.set_caption('group_game')
background=[pygame.image.load('level1.jpg'),pygame.image.load('level2.jpg'),pygame.image.load('level3.jpg'),pygame.image.load('level4.jpg')]
music=['level1.mp3','level2.mp3']
pygame.mixer.music.load("level1.mp3")
pygame.mixer.music.set_volume(1)
pygame.mixer.music.play(-1)
image=pygame.image.load("character.jpg")
image=pygame.transform.scale(image,(80,80))
image.set_colorkey((255,255,255))
#font
font=pygame.font.Font(None,36)


#pygame.mixer.music.load(music[play_index])
#pygame.mixer.music.play(-1)










 




#player
class Player(pygame.sprite.Sprite):
    number=1
    speed=3.5
    width=50
    height=50
    collider_width=10
    collider_height=10
    number_upper_limit=20
    def __init__(self,x,y):
        super().__init__()
        self.position_X=x       
        self.position_Y=y
        self.rect=pygame.Rect(self.position_X-Player.collider_width/2,self.position_Y,Player.collider_width,Player.collider_height)
    def base_figure(self):
        self.rect=pygame.Rect(self.position_X-Player.collider_width/2,self.position_Y,Player.collider_width,Player.collider_height)
        text=f"{Player.number}"
        number_render=font.render(text,True,(255,0,0))
        screen.blit(number_render,(self.position_X-10,self.position_Y-20))
        screen.blit(image,(self.position_X-Player.width/2,self.position_Y))
    def derivative_figure(self):
        screen.blit(image,(self.position_X-Player.width/2,self.position_Y))
    @staticmethod
    def create_derivative_figure():
        if Player.number<=Player.number_upper_limit:
            while len(Other.player_figure)>Player.number:
                Other.player_figure.pop()
            while len(Other.player_figure)<Player.number:
                Other.player_figure.append(Player(Other.player_figure[0].position_X+random.uniform(-25,25),Other.player_figure[0].position_Y+random.uniform(0,50)))
        else:
            while len(Other.player_figure)<Player.number:
                Other.player_figure.append(Player(Other.player_figure[0].position_X+random.uniform(-25,25),Other.player_figure[0].position_Y+random.uniform(0,50)))
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

class Formula(pygame.sprite.Sprite):
    current_index=0
    number=4
    speed=2
    width=20
    height=20
    operator=['+','-','*','/']
    height=50
    line_thickness=2
    def __init__(self,x,y,a,b):
        super().__init__()
        self.position_X=x
        self.position_Y=y
        self.value=a
        self.operator=b
        self.text=f"{self.operator}{self.value}"
        self.rect=pygame.Rect(self.position_X,self.position_Y,SCREEN_WIDTH/Formula.number,Formula.height)
    def formula_move(self):
        pygame.draw.rect(screen,WHITE,pygame.Rect(self.position_X,self.position_Y,SCREEN_WIDTH/NUMBER_OF_FORMULA,Formula.height))
        pygame.draw.rect(screen,BLACK,pygame.Rect(self.position_X,self.position_Y,SCREEN_WIDTH/NUMBER_OF_FORMULA,Formula.height),Formula.line_thickness)
        formula_render=font.render(self.text,True,BLACK)
        screen.blit(formula_render,(self.position_X+20,self.position_Y+25))
        self.rect=pygame.Rect(self.position_X,self.position_Y,SCREEN_WIDTH/Formula.number,Formula.height)

    def formula_reset(self):
        self.operator=Formula.operator[random.randint(0,3)]
        self.value=random.randint(1,10)
        self.position_Y=-50
        self.text=f"{self.operator}{self.value}"


    
class Other(pygame.sprite.Sprite):
    background_speed=2
    background_position=0
    norm=0 
    play_index=0
    player_figure=[]
    formulas=[]
    player_figure.append(Player(SCREEN_WIDTH/2,SCREEN_HEIGHT-200))


    for i in range(4):
        formulas.append(Formula(i*SCREEN_WIDTH/NUMBER_OF_FORMULA,-100,random.randint(1,10),Formula.operator[random.randint(0,3)]))


    @staticmethod
    def background_move(y,play_index):
            screen.blit(background[3],(0,y))
            screen.blit(background[3],(0,-SCREEN_HEIGHT+y))
    @staticmethod
    def background_alter(y,play_index):
         screen.blit(background[play_index-1],(0,-SCREEN_HEIGHT+y))
         screen.blit(background[play_index],(0,-2*SCREEN_HEIGHT+y))
    @staticmethod
    def collide_caculate():
        for i in range(NUMBER_OF_FORMULA):
            if Other.player_figure[0].rect.colliderect(Other.formulas[i].rect):
                if Other.formulas[i].operator=='+':
                    Player.number=int(Player.number+Other.formulas[i].value)
                elif Other.formulas[i].operator=='-':
                    Player.number=int(Player.number-Other.formulas[i].value)
                elif Other.formulas[i].operator=='*':
                    Player.number=int(Player.number*Other.formulas[i].value)
                elif Other.formulas[i].operator=='/':
                    Player.number=int(Player.number/Other.formulas[i].value)
                Formula.current_index+=1
                if Other.play_index<=2:
                    if Formula.current_index>=5:
                        Formula.current_index-=5
                        Other.play_index+=1
                for j in range(4):
                    Other.formulas[j].formula_reset()
                break


clock = pygame.time.Clock()
running=True
while running:


    Other.collide_caculate()
    Player.create_derivative_figure()
    Other.background_move(Other.background_position,Other.play_index)   
    Other.background_position+=Other.background_speed
    if Other.background_position>SCREEN_HEIGHT:
        Other.background_position=0
    
    Other.player_figure[0].base_figure()
    Other.player_figure[0].move()
    if Player.number<=20:
        for i in range(1,Player.number):
            Other.player_figure[i].derivative_figure()
            Other.player_figure[i].move()
    else:
        for i in range(1,Player.number_upper_limit):
            Other.player_figure[i].derivative_figure()
            Other.player_figure[i].move()

    for i in range(NUMBER_OF_FORMULA):
        Other.formulas[i].formula_move()
        Other.formulas[i].position_Y+=Formula.speed


    if Player.number<=0:
        running=False


    for event in pygame.event.get():
        if event.type ==pygame.QUIT:
            running=False

   
    clock.tick(60) 
    pygame.display.update()


   
    



    





















      #  if self.position_X+self.width<SCREEN_LEFT_BOUNDARY:
     #       self.position_X=SCREEN_RIGHT_BOUNDARY
    #self.position_X > SCREEN_RIGHT_BOUNDARY:  
    # self.position_X=SCREEN_LEFT_BOUNDARY-self.width
   # self.position_X < SCREEN_LEFT_BOUNDARY: 
  #  screen.blit(self.image, (self.position_X + SCREEN_WIDTH, self.position_Y))
 #   elif self.position_X + self.width > SCREEN_RIGHT_BOUNDARY:  
#    screen.blit(self.image, (self.position_X - SCREEN_WIDTH, self.position_Y))


#background move&alter
    #if (Formula.current_index>0&play_index>0)|(play_index==0&Formula.current_index<5):

    #else: 
         #other.background_alter(Other.background_position,play_index)
#formula move    

    

#player move

   # for i in range(len(player_figure)):
    ##    Player.draw_figure(player_figure[i].position_X,player_figure[i].position_Y)


