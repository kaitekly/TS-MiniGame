import pygame
import random

'//////////////////////////////'
pygame.init()
clock = pygame.time.Clock()
FPS = 60
'/////////'

class Main():
    def __init__(self):
        self.SCREEN_SIZE = 1080,720
        self.screen = pygame.display.set_mode(self.SCREEN_SIZE)
        self.BLACK = (0,0,0)
        self.score = 0

        'Background'
        self.image = pygame.image.load('images/Ocean.png')
        self.imageE = pygame.image.load('images/Ocean2.png')
        self.image = pygame.transform.scale(self.image,self.SCREEN_SIZE)
        self.imageE = pygame.transform.scale(self.imageE,self.SCREEN_SIZE)

        self.iman = 0
    def draw(self):
        if self.iman == 0:
            pygame.Surface.blit(self.screen,self.image,(0,0))
        else:
            pygame.Surface.blit(self.screen,self.imageE,(0,0))

class Sub():
    def __init__(self):
        div2 = lambda n : n/2
        self.pos = [div2(i) for i in main.SCREEN_SIZE]

        self.size = (100,100)
        self.images = [pygame.transform.scale(pygame.image.load('images/subR.png').convert_alpha(),self.size),pygame.transform.scale(pygame.image.load('images/subL.png').convert_alpha(),self.size)]
        self.image_masks = [pygame.mask.from_surface(self.images[0]),pygame.mask.from_surface(self.images[1])]
        self.imagei = 0
        self.speedx = 10
        self.speedy = 0.5
        
    def move(self,keys):
        if keys[pygame.K_d] and self.pos[0]<main.SCREEN_SIZE[0]-self.size[0]:
            self.pos[0]+=self.speedx
            self.pos[1]+=self.speedy

            self.imagei = 0
            
        elif keys[pygame.K_a] and self.pos[0]>0:
            self.pos[0]-=self.speedx
            self.pos[1]+=self.speedy
            self.imagei = 1
            
        else:
            self.pos[1]-=self.speedy
            
    def draw(self):
        pygame.Surface.blit(main.screen,self.images[self.imagei],self.pos)

class Oxygen_Level():
    def __init__(self):
        self.pos1 = (main.SCREEN_SIZE[0]-100,main.SCREEN_SIZE[1]-50)
        self.pos2 = (main.SCREEN_SIZE[0]-100,main.SCREEN_SIZE[1]-100)
        self.pos3 = (main.SCREEN_SIZE[0]-100,main.SCREEN_SIZE[1]-150)
        self.pos4 = (main.SCREEN_SIZE[0]-100,main.SCREEN_SIZE[1]-200)

        self.size = (80,40)

        self.max = 1000
        self.total = 1000
        

        self.BLUE = (0,0,204)
        self.GREEN = (0,204,0)
        self.ORANGE = (204, 102, 0)
        self.RED = (204,0,0)
        self.BLACK = (0,0,0)
        
        self.colors = {'blue':(0,0,255),'green':(0,255,0),'orange':(255, 165, 0),'red':(255,0,0)}

        self.current_color = 'red'
        
    def draw(self):
        if self.total>750:
            self.current_color = 'blue'
        elif self.total>500:
            self.current_color = 'green'
        elif self.total>250:
            self.current_color = 'orange'
        elif self.total>0:
            self.current_color = 'red'       
        
        if self.total>0:
            pygame.draw.rect(main.screen,self.colors[self.current_color],(self.pos1,self.size))
            pygame.draw.rect(main.screen,self.BLACK,(self.pos1,self.size),2)
        if self.total>250:
            pygame.draw.rect(main.screen,self.colors[self.current_color],(self.pos2,self.size))
            pygame.draw.rect(main.screen,self.BLACK,(self.pos2,self.size),2)
        if self.total>500:
            pygame.draw.rect(main.screen,self.colors[self.current_color],(self.pos3,self.size))
            pygame.draw.rect(main.screen,self.BLACK,(self.pos3,self.size),2)
        if self.total>750:
            pygame.draw.rect(main.screen,self.colors[self.current_color],(self.pos4,self.size))
            pygame.draw.rect(main.screen,self.BLACK,(self.pos4,self.size),2)
            
    def update(self,run):
        self.total-=1
        self.draw()
        if self.total < 0:
            return not run
        else:
            return run

class Oxygen_Tanks():
    def __init__(self):
        self.size = (100,100)
        self.image = pygame.transform.scale(pygame.image.load('images/o2_tank.png'),self.size).convert_alpha()
        self.image_mask = pygame.mask.from_surface(self.image)

        self.speed = 2
        self.max_tanks = 1

        self.tanks_pos = []

    def spawn_tank(self,pos):
        self.tanks_pos.append([pos,main.SCREEN_SIZE[1]])

    def draw(self):
        for i in self.tanks_pos:
            pygame.Surface.blit(main.screen,self.image,i)

    def update(self,score):
        for i in self.tanks_pos:
            i[1]-=1
            if i[1]<-100:
                self.tanks_pos.remove(i)
            if self.image_mask.overlap(sub.image_masks[sub.imagei],(i[0]-sub.pos[0],i[1]-sub.pos[1])):
                o2_meter.total = o2_meter.max
                self.tanks_pos.remove(i)
                score+=100
        if len(self.tanks_pos) < self.max_tanks:
            self.spawn_tank(random.randint(0,main.SCREEN_SIZE[0]))

        self.draw()
        return score

class Controller_minigame():
    def __init__(self):
        self.textcount = 0
        self.WHITE = (255,255,255)
        self.BLACK = (0,0,0)

        self.font = pygame.font.SysFont('lucidasans',60)
        self.textw = self.font.render('PLEASE RECONNECT CONTROLLER!',True,self.WHITE)
        self.textb = self.font.render('PLEASE RECONNECT CONTROLLER!',True,self.BLACK)
                
        self.controller = pygame.image.load('images/controller.png').convert_alpha()
        self.c_pos = (main.SCREEN_SIZE[0]//2)-250,(main.SCREEN_SIZE[1]//2)-250

        self.usb = pygame.transform.scale(pygame.image.load('images/usb.png'),(40,330)).convert_alpha()
        self.usb_mask = pygame.mask.from_surface(self.usb)
        self.usb_pos = [0,main.SCREEN_SIZE[1]-200]

        self.usb_max = [0,main.SCREEN_SIZE[0]]
        self.speed = 40

        self.go_left = False

        self.arrow = pygame.transform.scale(pygame.image.load('images/arrow.png'),(50,50)).convert_alpha()
        self.arrow_mask = pygame.mask.from_surface(self.arrow)
        self.arrow_pos = ((main.SCREEN_SIZE[0]/2)-25,400)

        self.tryconnect_b = False
        
    def move_usb(self):
        if self.usb_pos[0]<self.usb_max[1] and not self.go_left:
            self.usb_pos[0]+=self.speed
        else:
            self.go_left = True
            self.usb_pos[0]-=self.speed
            if self.usb_pos[0]<self.usb_max[0]:
                self.go_left = False
            
    def tryconnect(self):
        self.usb_pos[1]-=1
        if self.usb_mask.overlap(self.arrow_mask,(self.arrow_pos[0]-self.usb_pos[0],self.arrow_pos[1]-self.usb_pos[1])):
            self.tryconnect_b = False
            self.usb_pos = [0,main.SCREEN_SIZE[1]-200]
            main.iman = 0
            main.score+=2000
            return False
        elif self.usb_pos[1]<400:
            self.tryconnect_b = False
            self.usb_pos = [0,main.SCREEN_SIZE[1]-200]
        return True
        
    def draw(self):
        self.textcount+=1
        pygame.Surface.blit(main.screen,self.arrow,self.arrow_pos)
        pygame.Surface.blit(main.screen,self.usb,self.usb_pos)
        pygame.Surface.blit(main.screen,self.controller,self.c_pos)
        
        if self.textcount<10:
            main.screen.blit(self.textw,(20,100))
            main.iman = 2
        elif self.textcount>10:
            main.screen.blit(self.textb,(20,100))
            main.iman = 0
            
        if self.textcount == 20:
            self.textcount-=20
    def update(self,keys):
        self.draw()
        if not keys[pygame.K_SPACE] and not self.tryconnect_b:
            self.move_usb()
        else:
            self.tryconnect_b = True
            return self.tryconnect()
        return True

class GameEvents():
    def __init__(self):
        self.tick = 0

    def check_events(self):
        if self.tick == 400:
            self.tick = 0
            luck = random.randint(0,1)
            if luck == 1:
                return True
            
    def update(self):
        self.tick+=1

        return self.check_events()

#-=-=--=-=-=-=-=-=-=-=-=-=-=-=-==-=--=-=-=-=-=-=-=-=-=-=-=-=-=-=-=#\

main = Main()


running = False
in_menu = True

died = pygame.transform.scale(pygame.image.load('images/died.png'),main.SCREEN_SIZE)
font = pygame.font.SysFont('lucidasans',30)
text1 = font.render('Controls:',True,(255,255,255))
text2 = font.render('A,D,SPACE & ESC to leave',True,(255,255,255))
text3 = font.render('good luck finding the titanic :)',True,(255,255,255))
text4 = font.render('~made by kajetk~',True,(255,255,255))
while in_menu:
    stop_run_time = 0
    main.score = 0
    file = open("hiscore.txt", "r")
    hiscore = file.readline()
    hiscore = int(hiscore)
    file.close()
    
    text5 = font.render('hiscore: '+str(hiscore),True,(255,255,255))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            in_menu = False
    keys = pygame.key.get_pressed()
    if keys[pygame.K_SPACE]:
        stop_run_time = 60
        running=True
        sub = Sub()
        o2_meter = Oxygen_Level()
        o2_tanks = Oxygen_Tanks()
        reconect_game = Controller_minigame()

        gameevent = GameEvents()
        reconect = False
    if keys[pygame.K_ESCAPE]:
        in_menu = False
    main.draw()
    main.screen.blit(text1,(200,100))
    main.screen.blit(text2,(200,150))
    main.screen.blit(text3,(200,200))
    main.screen.blit(text4,(200,250))
    main.screen.blit(text5,(450,500))
    while running or stop_run_time>0:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                
        keys = pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE]:
            running=False
        ###^EVENTS^###
        main.score+=1

        #ENDBE#
        main.draw()
        sub.draw()
        main.score = o2_tanks.update(main.score)

        running = o2_meter.update(running)

        
        if reconect:
            reconect = reconect_game.update(keys)
            main.score+=3
        else:
            sub.move(keys)
            reconect = gameevent.update()

        DrawScore = font.render('score: '+str(main.score),True,(255,255,255))
        main.screen.blit(DrawScore,(500,50))
        #ENDEL#
        clock.tick(FPS)
        pygame.display.flip()
        if running == False:
            main.iman = 0
            stop_run_time-=1
            main.screen.blit(died,(0,0))
            clock.tick(FPS)
            pygame.display.flip()
            if main.score>hiscore:
                file = open('hiscore.txt','w')
                file.write(str(main.score))
                file.close
            
            
    clock.tick(FPS)
    pygame.display.flip()
pygame.quit()
