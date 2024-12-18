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
#background=[pygame.image.load('level1.jpg'),pygame.image.load('level2.jpg'),pygame.image.load('level3.jpg'),pygame.image.load('level4.jpg')]
#music=['level1.mp3','level2.mp3','level3.mp3','level4.mp3']
background=[pygame.image.load(f'level{i}.jpg') for i in range(1,5)]
music=[f'level{i}.mp3' for i in range(1,5)]
pygame.mixer.music.load(music[0])
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
    width=SCREEN_WIDTH/NUMBER_OF_FORMULA
    height=50
    operator=['+','-','*','/']
    line_thickness=2
    #-1 stands for infinity
    formula_dict={formula1:-1,formula2:0,formula3:1,formula4:13,formula5:math.e,formula6:math.pi,formula7:math.e**math.pi,formula8:1,formula9:math.pi**math.e,formula10:1/math.sqrt(math.e),formula11:math.pi,formula12:math.pi*math.sqrt(2)/4,formula13:-1,formula14:0,formula15:-35/12+5/math.sqrt(2)+math.pi/8}
    def __init__(self,x,y,a,b):
        super().__init__()
        self.position_X=x
        self.position_Y=y
        self.value=a
        self.operator=b
        self.formula_flag=1
        self.text=f"{self.operator}{self.value}"
        self.rect=pygame.Rect(self.position_X,self.position_Y,SCREEN_WIDTH/Formula.number,Formula.height)
    def formula_move(self):
        if self.formula_flag:
            pygame.draw.rect(screen,WHITE,pygame.Rect(self.position_X,self.position_Y,SCREEN_WIDTH/NUMBER_OF_FORMULA,Formula.height))
            pygame.draw.rect(screen,BLACK,pygame.Rect(self.position_X,self.position_Y,SCREEN_WIDTH/NUMBER_OF_FORMULA,Formula.height),Formula.line_thickness)
            formula_render=font.render(self.text,True,BLACK)
            screen.blit(formula_render,(self.position_X+20,self.position_Y+25))
        else:
            screen.blit(self.text,(self.position_X,self.position_Y))
            

    def formula_reset(self):
        self.operator=Formula.operator[random.randint(0,3)]
        if Other.play_index==0:
            self.formula_flag=1
            if self.operato=='*'|self.operato=='/':
                   self.value=random.uniform(0,3)
            else:            
                self.value=random.randint(1,10)
                self.text=f"{self.operator}{self.value}"        
        elif Other.play_index==1:
            self.formula_flag=0        
            if self.operato=='*'|self.operato=='/':
                   self.value=random.uniform(0,2)
            else:            
                self.value=random.randint(20,100)   
            self.text=f"{self.operator}{self.value}"                     else:
            flag=random.randint(0,1)            
            if flag:
                self.formula_flag=0
                self.text=random.choice(list(Formula.formula_dict.keys()))     
                self.value=Formula.formula_dict[self.text]
            else:
                self.formula_flag=1
            if self.operato=='*'|self.operato=='/':
                self.value=random.uniform(0,3)
            else:            
                self.value=random.randint(20,100)   
                      
         self.position_Y=-50



class heap():
        heap_size=0
        array=[]
        array_max_5=[2,7,1,8,1]
        @staticmethod
        def heapify(index):
            while 2*index+2<heap.heap_size and heap.array[index]<max(heap.array[2*index+1],heap.array[2*index+2]):
                temp=index
                if heap.array[2*index+1]>=heap.array[2*index+2]:
                 heap.array[index],heap.array[2*index+1]=heap.array[2*index+1],heap.array[index]
                 index=2*temp+1
                else:
                    heap.array[index],heap.array[2*index+2]=heap.array[2*index+2],heap.array[index]
                    index=2*temp+2  
            if 2*index+1<heap.heap_size and heap.array[index]<heap.array[2*index+1]:
                  heap.array[index],heap.array[2*index+1]=heap.array[2*index+1],heap.array[index]
        @staticmethod            
        def heapify_process():
                for i in range(heap.heap_size//2-1,-1,-1):
                    heap.heapify(i)
           
        @staticmethod
        def get_max():
             max=heap.array[0]
             heap.array[0],heap.array[heap.heap_size-1]=heap.array[heap.heap_size-1],heap.array[0]
             heap.heap_size-=1
             heap.array.pop()
             heap.heapify(0)
             return max
        @staticmethod
        def heap_insert(value):
             heap.array.append(value)
             heap.heap_size+=1
        @staticmethod
        def heap_clear():
             heap.array.clear()
             heap.heap_size=0
    
class Other(pygame.sprite.Sprite):
    background_speed=2
    background_position=0
    norm=0 
    play_index=0
    player_figure=[]
    music.flag=False
    player_figure.append(Player(SCREEN_WIDTH/2,SCREEN_HEIGHT-200))
    formulas=[Formula(0,-100,2,Formula.operator[0]),Formula(SCREEN_WIDTH/NUMBER_OF_FORMULA,-100,7,Formula.operator[0]),Formula(2*SCREEN_WIDTH/NUMBER_OF_FORMULA,-100,1,Formula.operator[0]),Formula(3*SCREEN_WIDTH/NUMBER_OF_FORMULA,-100,8,Formula.operator[0])]


       # formulas.append(Formula(i*SCREEN_WIDTH/NUMBER_OF_FORMULA,-100,random.randint(1,10),Formula.operator[random.randint(0,3)]))
        


    @staticmethod
    def background_move(y,play_index):
            screen.blit(background[3],(0,y))
            screen.blit(background[3],(0,-SCREEN_HEIGHT+y))
    @staticmethod
    def collide_caculate():
                if Other.formulas[0].position_Y+Formula.height==Other.player_figure[0].position_Y:
                    nearest_index=0
                    nearest_dis=abs((player_figure[0].position_X+Player.width/2)-(Other.formulas[0].position_X+Formula.width/2))
                    for i in range(1,4):
                            if temp=abs((player_figure[0].position_X+Player.width/2)-(Other.formulas[i].position_X+Formula.width/2))<nearest_dis:
                                nearest_index=i
                                nearest_dis=temp
                     if Other.formulas[nearest_index].operator=='+':
                        Player.number=Player.number+Other.formulas[nearest_index].value
                     elif Other.formulas[nearest_index].operator=='-':
                        Player.number=Player.number-Other.formulas[nearest_index].value
                    elif Other.formulas[nearest_index].operator=='*':
                        Player.number=int(Player.number*Other.formulas[nearest_index].value)
                    elif Other.formulas[nearest_index].operator=='/':
                        Player.number=Player.number//Other.formulas[nearest_index].value
                for i in range(4):
                    if Other.formulas[i].operator=='+':
                        for j in range(4):
                            heap.heap_insert(heap.array_max_5[j]+Other.formulas[i].value)                           
                    elif Other.formulas[i].operator=='-':
                        for j in range(4):
                            heap.heap_insert(heap.array_max_5[j]-Other.formulas[i].value) 
                    elif Other.formulas[i].operator=='*':
                       for j in range(4):
                            heap.heap_insert(int(heap.array_max_5[j]*Other.formulas[i].value)) 
                    elif Other.formulas[i].operator=='/':
                       for j in range(4):
                            heap.heap_insert(heap.array_max_5[j]//Other.formulas[i].value) 
                                  
                heap.heapify_process()
                for i in range(5):
                    heap.array_max_5[i]=heap.get_max()
                heap.clear()
                Formula.current_index+=1
                if Other.play_index<=2
                    if Formula.current_index%5==0:
                        Other.play_index+=1
                        pygame.mixer.music.load(music[Other.play_index])
                        pygame.mixer.music.play(-1)
                for j in range(4):
                    Other.formulas[j].formula_reset()
                break
            

def show_game_over():
    screen.fill(BLACK)
    game_over_text = font.render("Game Over", True, RED)
    retry_text = font.render("Press R to Retry or Q to Quit", True, WHITE)
    
    screen.blit(game_over_text, (SCREEN_WIDTH / 2 - game_over_text.get_width() / 2, SCREEN_HEIGHT / 3))
    screen.blit(retry_text, (SCREEN_WIDTH / 2 - retry_text.get_width() / 2, SCREEN_HEIGHT / 2))
    pygame.display.update()


clock = pygame.time.Clock()
running=True
game_over = False
while running:

    if game_over == False:
      Other.collide_caculate()
      formual_num_text=font.render(f'Score:{Formula.current_inde}', True, WHITE)
      screen.blit(formual_num_text, (20,20))
      Player.create_derivative_figure()
      
      Other.background_move(Other.background_position,Other.play_index)   
      if 
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
          # running=False
          game_over = True
          pygame.mixer.music.stop()  
        

      for event in pygame.event.get():
          if event.type ==pygame.QUIT:
              running=False
    else:
      show_game_over()
      for event in pygame.event.get():
          if event.type == pygame.QUIT:
              running = False
          elif event.type == pygame.KEYDOWN:
              if event.key == pygame.K_r:  # retry
                  Player.number = 1  
                  Formula.current_index = 0
                  Other.play_index = 0
                  Other.player_figure = [Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT - 200)]
                  Other.formulas = [
                      Formula(i * SCREEN_WIDTH / NUMBER_OF_FORMULA, -100, random.randint(1, 10), Formula.operator[random.randint(0, 3)])
                      for i in range(4)
                  ]
                  pygame.mixer.music.play(-1)  
                  game_over = False
              elif event.key == pygame.K_q:  # quit
                  running = False



    clock.tick(60) 
    pygame.display.update()
