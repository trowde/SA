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

formula_extra=([pygame.image.load(f'math_problem/lim/lim_q{i}.png') for i in range(1,11)]+[pygame.image.load(f'math_problem/int/integral_q{i}.png') for i in range(1,6)]
+[pygame.image.load(f'math_problem/sum/sum_q{i}.png') for i in range(1,14)]+[pygame.image.load(f'math_problem/det/det_q{i}.png') for i in range(1,8)])
formula_extra=[pygame.transform.scale(formula,(SCREEN_WIDTH/NUMBER_OF_FORMULA-30,150)) for formula in formula_extra]



#initiate
screen=pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
pygame.display.set_caption('LastWar')
#background=[pygame.image.load('level1.jpg'),pygame.image.load('level2.jpg'),pygame.image.load('level3.jpg'),pygame.image.load('level4.jpg')]
#music=['level1.mp3','level2.mp3','level3.mp3','level4.mp3']
background=[pygame.image.load(f'level{i}.jpg') for i in range(1,5)]
music=[f'level{i}.mp3' for i in range(1,5)]
pygame.mixer.music.load(music[0])
pygame.mixer.music.set_volume(1)
pygame.mixer.music.play(-1)
image=[pygame.image.load(f"player{i}.png")for i in range(1,5)]
image=[pygame.transform.scale(img,(50,50))for img in image]
for img in image:
    img.set_colorkey((255,255,255))
#font
font=pygame.font.Font(None,36)

#player
class Player(pygame.sprite.Sprite):
    number=1
    speed=3.5
    width=50
    height=50
    collider_width=10
    collider_height=10
    number_upper_limit=20
    animation_index = 0
    animation_speed = 10

    def __init__(self,x,y):
        super().__init__()
        self.position_X=x       
        self.position_Y=y
        self.rect=pygame.Rect(self.position_X-Player.collider_width/2,self.position_Y,Player.collider_width,Player.collider_height)
        self.animation_counter = 0
    def base_figure(self):
        self.animation_counter += 1
        if self.animation_counter >= Player.animation_speed:
            self.animation_counter = 0
            Player.animation_index = (Player.animation_index + 1) % len(image)
        text=f"{Player.number}"
        number_render=font.render(text,True,RED)
        screen.blit(number_render,(self.position_X-25,self.position_Y-25))
        screen.blit(image[Player.animation_index],(self.position_X-Player.width/2,self.position_Y))
    @staticmethod
    def create_derivative_figure():
        if Player.number<=Player.number_upper_limit:
            while len(Other.player_figure)>Player.number:
                 Other.player_figure.pop()
            while len(Other.player_figure)<Player.number:
                Other.player_figure.append(Player(Other.player_figure[0].position_X+random.uniform(-25,25),Other.player_figure[0].position_Y+random.uniform(0,50)))
        else:
            while len(Other.player_figure)<Player.number_upper_limit:
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
    speed=1
    width=SCREEN_WIDTH/NUMBER_OF_FORMULA
    height=150
    operator=['+','-','*','/']
    line_thickness=2
    
    #-1 stands for infinity
    formula_dict={formula_extra[0]:-1,formula_extra[1]:0,formula_extra[2]:1,formula_extra[3]:-1,formula_extra[4]:13,
    formula_extra[5]:math.e,formula_extra[6]:math.pi,formula_extra[7]:math.e**math.pi,formula_extra[8]:1,formula_extra[9]:math.pi**math.e,
    formula_extra[10]:math.pi,formula_extra[11]:math.pi*math.sqrt(2)/4,formula_extra[12]:-1,formula_extra[13]:0,formula_extra[14]:-35/12+5/math.sqrt(2)+math.pi/8,
    formula_extra[15]:6,formula_extra[16]:8,formula_extra[17]:3.75,formula_extra[18]:2.5,formula_extra[19]:1.625,formula_extra[20]:2,formula_extra[21]:1,formula_extra[22]:0.5,
    formula_extra[23]:2,formula_extra[24]:1,formula_extra[25]:5,formula_extra[26]:1,formula_extra[27]:-1,formula_extra[28]:2,formula_extra[29]:5,formula_extra[30]:10,
    formula_extra[31]:1,formula_extra[32]:8,formula_extra[33]:12,formula_extra[34]:0}
    def __init__(self,x,y,a,b):
        super().__init__()
        self.position_X=x
        self.position_Y=y
        self.value=a
        self.operator=b
        self.formula_flag=0
        self.text=f"{self.operator}{self.value}"
        self.rect=pygame.Rect(self.position_X,self.position_Y,SCREEN_WIDTH/Formula.number,Formula.height)
    def formula_move(self):
        if self.formula_flag == 0:
            pygame.draw.rect(screen, WHITE, pygame.Rect(self.position_X, self.position_Y, SCREEN_WIDTH / NUMBER_OF_FORMULA, Formula.height))
            pygame.draw.rect(screen, BLACK, pygame.Rect(self.position_X, self.position_Y, SCREEN_WIDTH / NUMBER_OF_FORMULA, Formula.height), Formula.line_thickness)
            formula_render = font.render(self.text, True, BLACK)
            screen.blit(formula_render, (self.position_X + 50, self.position_Y + 50))
        else:
            operator_text=f"{self.operator}"  
            pygame.draw.rect(screen, WHITE, pygame.Rect(self.position_X, self.position_Y, SCREEN_WIDTH / NUMBER_OF_FORMULA, Formula.height))
            pygame.draw.rect(screen, BLACK, pygame.Rect(self.position_X, self.position_Y, SCREEN_WIDTH / NUMBER_OF_FORMULA, Formula.height), Formula.line_thickness)            
            formula_render = font.render(operator_text, True, BLACK)
            screen.blit(formula_render, (self.position_X+15, self.position_Y+65))
            screen.blit(self.text, (self.position_X+30, self.position_Y))

            

    def formula_reset(self):
        self.operator=Formula.operator[random.randint(0,3)]
        if Other.play_index==0:
            self.formula_flag=0
            if self.operator=='*'or self.operator=='/':
                   self.value=random.uniform(0,3)
            else:            
                self.value=random.randint(1,10)
            self.text=f"{self.operator}{self.value:.2f}"        
        elif Other.play_index==1:
            self.formula_flag=0        
            if self.operator=='*'or self.operator=='/':
                   self.value=random.uniform(0,2)
            else:            
                self.value=random.randint(20,100)   
            self.text=f"{self.operator}{self.value:.2f}"                     
        else:
            flag=random.randint(0,1)            
            if flag==1:
                self.formula_flag=1
                self.text=random.choice(list(Formula.formula_dict.keys()))     
                self.value=Formula.formula_dict[self.text]
            else:
                self.formula_flag=0
                if self.operator=='*' or self.operator=='/':
                    self.value=random.uniform(0,3)
                else:            
                    self.value=random.randint(20,100)  
                self.text=f"{self.operator}{self.value:.2f}"  
                      
        self.position_Y=-250



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
    background_speed=1
    background_position=0
    limit_score=1
    limit_score_position_Y=0
    limit_score_flag=True
    limit_score_text=font.render(f"{limit_score}",True,RED)
    norm=0 
    play_index=0
    player_figure=[]
    music_flag=False
    player_figure.append(Player(SCREEN_WIDTH/2,SCREEN_HEIGHT-200))
    formulas=[Formula(0,-200,2,Formula.operator[0]),Formula(SCREEN_WIDTH/NUMBER_OF_FORMULA,-200,7,Formula.operator[0]),Formula(2*SCREEN_WIDTH/NUMBER_OF_FORMULA,-200,1,Formula.operator[0]),Formula(3*SCREEN_WIDTH/NUMBER_OF_FORMULA,-200,8,Formula.operator[0])]


       # formulas.append(Formula(i*SCREEN_WIDTH/NUMBER_OF_FORMULA,-100,random.randint(1,10),Formula.operator[random.randint(0,3)]))
        


    @staticmethod
    def background_move(y,play_index):
        screen.blit(background[Other.play_index],(0,y))
        screen.blit(background[Other.play_index],(0,-SCREEN_HEIGHT+y))
    @staticmethod
    def collide_caculate():
        if Other.formulas[0].position_Y+Formula.height>=Other.player_figure[0].position_Y:
            Formula.current_index+=1           
            nearest_index=0
            nearest_dis=abs((Other.player_figure[0].position_X)-(Other.formulas[0].position_X+Formula.width/2))
            for i in range(1,4):
                temp=abs((Other.player_figure[0].position_X)-(Other.formulas[i].position_X+Formula.width/2))
                if temp<nearest_dis:
                    nearest_index=i
                    nearest_dis=temp
            if Other.formulas[nearest_index].value==-1:
                game_over=True
            else:                          
                if Other.formulas[nearest_index].operator=='+':
                    Player.number=Player.number+Other.formulas[nearest_index].value
                elif Other.formulas[nearest_index].operator=='-':
                    Player.number=Player.number-Other.formulas[nearest_index].value
                elif Other.formulas[nearest_index].operator=='*':
                    Player.number=int(Player.number*Other.formulas[nearest_index].value)
                elif Other.formulas[nearest_index].operator=='/':
                    Player.number=Player.number//Other.formulas[nearest_index].value
                if Formula.current_index%5==0 and Formula.current_index!=0:
                    Other.limit_score=heap.array_max_5[4]      
                    Other.limit_score_text=font.render(f"{Other.limit_score}",True,RED)
                    heap.array_max_5=[Player.number] * 5   
                if Other.play_index<=2:
                    if Formula.current_index%5==0 and Formula.current_index!=0:
                        Other.limit_score_flag=True
                        Formula.speed=2
                        Other.background_speed=2
                        Other.play_index+=1
                        pygame.mixer.music.load(music[Other.play_index])
                        pygame.mixer.music.play(-1)                                            
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
                            if Other.formulas[i].value == 0:
                                heap.heap_insert(0)                      
                            else:
                                heap.heap_insert(heap.array_max_5[j]//Other.formulas[i].value) 
                for i in range(4):
                    Other.formulas[i].formula_reset()                                  
                heap.heapify_process()
                for i in range(5):
                    heap.array_max_5[i]=heap.get_max()
                heap.heap_clear()


    

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
        Player.create_derivative_figure()     
        Other.collide_caculate()           
        for i in range(len(Other.player_figure)):
            Other.player_figure[i].position_X=max(0,min(Other.player_figure[i].position_X,SCREEN_WIDTH))
            Other.player_figure[i].position_Y=max(SCREEN_HEIGHT/2,min(Other.player_figure[i].position_Y,SCREEN_HEIGHT-Player.height*2))
     #   for i in Other.player_figure:
          #  i.position_X+=(Other.player_figure[0].position_X-i.position_X)   
       #     i.position_Y+=(Other.player_figure[0].position_Y-i.position_Y)           
        
  
        Other.background_move(Other.background_position,Other.play_index)   
        Other.background_position+=Other.background_speed
        if Other.background_position>SCREEN_HEIGHT:
            Other.background_position=0
        
        if Other.limit_score_flag and Formula.current_index%5==0 and Formula.current_index!=0:
            pygame.draw.rect(screen,WHITE,pygame.Rect(0,Other.limit_score_position_Y,SCREEN_WIDTH,25))
            screen.blit(Other.limit_score_text,(SCREEN_WIDTH/2,Other.limit_score_position_Y))
            Other.limit_score_position_Y+=2
        if Other.limit_score_position_Y+25>=Other.player_figure[0].position_Y:
            if Other.limit_score>Player.number:
                game_over=True
                Other.limit_score_flag=False
                    
        for i in range(len(Other.player_figure)):
            Other.player_figure[i].move()
        Other.player_figure[0].base_figure()
        for i in range(1,len(Other.player_figure)):
            screen.blit(image[Player.animation_index],(Other.player_figure[i].position_X,Other.player_figure[i].position_Y))
        
#        if Player.number<=20:
#            for i in range(1,Player.number):
 #               Other.player_figure[i].move()
  #      else:
   #         for i in range(1,Player.number_upper_limit):
    #            Other.player_figure[i].move()

        for i in range(NUMBER_OF_FORMULA):
            Other.formulas[i].formula_move()
            Other.formulas[i].position_Y+=Formula.speed
        formual_num_text=font.render(f'Score:{Formula.current_index}', True, RED)  
        pygame.draw.rect(screen, WHITE, pygame.Rect(0, 450, 150,80))           
        pygame.draw.rect(screen, BLACK, pygame.Rect(0, 450, 150, 80), 2)    
        screen.blit(formual_num_text, (30,475))

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
                  pygame.mixer.music.load(music[0])
                  pygame.mixer.music.play(-1)  
                  game_over = False
              elif event.key == pygame.K_q:  # quit
                  running = False



    clock.tick(60) 
    pygame.display.update()

   
