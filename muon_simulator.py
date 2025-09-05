import pygame
import random
import numpy as np
import sys
import time

WIDTH,HEIGHT=800,600                                           
screen=pygame.display.set_mode((WIDTH,HEIGHT))                 
clock=pygame.time.Clock()                                      
all_sprites=pygame.sprite.Group()                              
pygame.font.init()    

size_cell=(80,60)
                                         

def TAC(f,x_1,x_2,y_1,y_2):
    x=random.uniform(x_1,x_2)
    y=random.uniform(y_1,y_2)
    while y>f(x):
        x=random.uniform(x_1,x_2)
        y=random.uniform(y_1,y_2)
    return x

def cos2(x):
    return (np.cos(x))**2

def expo(x):
    return np.exp(-x/100)

class Muon(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image=pygame.image.load("muon.png").convert()
        self.image.set_colorkey((255,255,255))
        self.rect=self.image.get_rect()        
        theta=TAC(cos2,np.pi/2,-np.pi/2,0,1)
        self.rect.center=(random.uniform(40,760),0)
        self.speed=(10*np.sin(theta),10*np.cos(theta))
    def update(self,muons):
        self.rect.x+=self.speed[0]
        self.rect.y+=self.speed[1]
        if self.rect.center[1]>HEIGHT+10:
            all_sprites.remove(self)
        return
        
class Scotch(pygame.sprite.Sprite):
    def __init__(self,x,y):
        super().__init__()
        self.image=pygame.image.load("scotch.png").convert()
        self.image.set_colorkey((255,255,255))
        self.rect=self.image.get_rect()        
        self.rect.center=(x,y)
    def update(self,muons):
        return

class Cell(pygame.sprite.Sprite):
    def __init__(self,x,y):
        super().__init__()
        self.image_off=pygame.image.load("light_off.png").convert()
        self.image_on=pygame.image.load("light_on.png").convert()
        self.image_off.set_colorkey((255,255,255))
        self.image_on.set_colorkey((255,255,255))
        self.image=self.image_off
        self.rect=self.image.get_rect()        
        self.rect.center=(x,y)
    def update(self,muons):
        for muon in muons:
            if self.rect.colliderect(muon.rect):
                self.image=self.image_on
                break
            self.image=self.image_off   
        return

def staggered(all_sprites):
    all_sprites.empty()
    for i in range(10):
        for j in range(10):
            if (i+j)%2==0:
                all_sprites.add(Scotch(size_cell[0]/2+i*size_cell[0],size_cell[1]+j*size_cell[1]))
            else:
                all_sprites.add(Cell(size_cell[0]/2+i*size_cell[0],size_cell[1]+j*size_cell[1]))
    
def ordered(all_sprites):
    all_sprites.empty()
    for i in range(10):
        for j in range(10):
            if i%2==0:
                all_sprites.add(Scotch(size_cell[0]/2+i*size_cell[0],size_cell[1]+j*size_cell[1]))
            else:
                all_sprites.add(Cell(size_cell[0]/2+i*size_cell[0],size_cell[1]+j*size_cell[1]))
    

staggered(all_sprites)
#ordered(all_sprites)
muons=[]        
frame_count=0
new_frame_count=0
muon_count=0
start_time=time.time()
while True:
    for event in pygame.event.get():
            if event.type==pygame.QUIT:
                pygame.quit()
                sys.exit()
                
    if frame_count>=new_frame_count:
        muon=Muon()
        muons.append(muon)
        all_sprites.add(muon)
        frame_count=0
        new_frame_count=TAC(expo,0,200,0,1)
        muon_count+=1
    frame_count+=1
    
    screen.fill((255,255,255))
    all_sprites.draw(screen)

    all_sprites.update(muons)
    
    remaining_muons=[]
    for muon in muons:
        if 0<=muon.rect.center[0]<=800 and 0<=muon.rect.center[1]<=600:
            remaining_muons.append(muon)
            
    muons=remaining_muons
    
    font=pygame.font.SysFont(None,30)
    text=font.render(f"MUONS: {muon_count} - TIME: {round((time.time()-start_time),2)} s",True,(0,0,0))
    
    
    screen.blit(text,(10,10))            
    
    pygame.display.flip()
    clock.tick(60)
    
