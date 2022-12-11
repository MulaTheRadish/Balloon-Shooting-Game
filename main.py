#==========================================================================================
#importing necessary components
import sys
import pygame
from random import randint
import random

#initialising game and basics
pygame.init()
clock = pygame.time.Clock()
size = width, height = 852, 480
background = 255, 255, 255
screen = pygame.display.set_mode(size)
#Bedazzles the game
Font = pygame.font.SysFont("Arial", 15)
pygame.display.set_caption("Shooting Game")
icon = pygame.image.load("bullet.png")
pygame.display.set_icon(icon)
#==========================================================================================
#initialises Balloon class
class Balloon(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        #loading balloon image and creating rect to act as hitbox.
        self.image = pygame.image.load("balloon.png")
        self.rect = self.image.get_rect(center = (width // 5, height //2))
    
    #move the balloon
    def update(self):
        self.rect = self.rect.move(balloonspeed)
        #if the balloon's hitbox hits the top or the bottom, it changes direction
        if self.rect.top < 0 or self.rect.bottom > height:
            balloonspeed[1] = -balloonspeed[1]

    def pop(self):
        global popped
        global missed_shots
        
        #adds one to the popped element
        popped += 1
        #destrotys the balloon after being shot
        balloon.kill()
        #immediately loads a new balloon
        self.image = pygame.image.load("balloon.png")
        #loads balloon in the same x value, with a random y value. 
        self.rect = self.image.get_rect(center = (width // 5, randint(33, 447)))
        speeds = [[0, 7], [0, -7]]
        #randomly chooses a direction to move after being reloaded
        self.rect = self.rect.move(random.choice(speeds))
        #adds sprite to group
        balloon_group.add(self)

#balloon basics; adding balloon to sprite group, setting balloon speed
balloon = Balloon()
balloon_group = pygame.sprite.Group()
balloon_group.add(balloon)
balloonspeed = [0, 7] 
#==========================================================================================
#initialises gun class
class Gun(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        #loading gun image
        self.image = pygame.image.load("gun.png")
        self.rect = self.image.get_rect(center = (width // 5 * 4, height // 2))
        
    #moves the gun
    def update(self):
        self.rect.clamp_ip(screen.get_rect())
        #checks if W or UP key is present in held_keys array
        if pygame.K_UP in held_keys or pygame.K_w in held_keys:
            self.rect = self.rect.move(0, -4)
        #checks if S or DOWN key is present in held_keys array
        elif pygame.K_DOWN in held_keys or pygame.K_s in held_keys:
            self.rect = self.rect.move(0, 4)
    
    #creates a new bullet in the coordinates of the barrel of the gun
    def create_bullet(self):
        return Bullet(self.rect.midleft[0], self.rect.midleft[1] - 11)

#gun basics; adding gun to sprite group
gun = Gun()
gun_group = pygame.sprite.Group()
gun_group.add(gun)
#==========================================================================================
#initialises Bullet class
class Bullet(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__()
        self.image = pygame.image.load("bullet.png")
        self.rect = self.image.get_rect(center = (pos_x, pos_y))
    
    #moves bullet to the left at 10 times the y value of the balloon speed
    def update(self):
        self.rect.x -= abs(balloonspeed[1]) * 10
        #if the bullet reaches the left side of the screen, it will obliterate
        if self.rect.right <= 0:
            self.kill()
        #if the bullet hitbox overlaps the balloon hitbox, the balloon will obliterate
        if self.rect.colliderect(balloon.rect):
            #runs the pop commands which destroys and simultaneously creates a new balloon
            balloon.pop()

#bullet basics; adding bullet to sprite group
bullet_group = pygame.sprite.Group()
#==========================================================================================
#an array tracking which keys are being held down
held_keys = []
#tracks shots fired, and number of balloons popped
shots = 0
popped = 0

#runs forever loop to continually run the game.
while True:
    for event in pygame.event.get():
        #if the client presses the 'x' game will quit
        if event.type == pygame.QUIT: 
            sys.exit()
        
        #any depressed buttons will be added to the held_keys array
        if event.type == pygame.KEYDOWN:
            held_keys.append(event.key)
            #if spacebar is pressed, it will add 1 to the 'shots' counter and run create_bullet()
            if event.key == pygame.K_SPACE:
                shots += 1
                bullet_group.add(gun.create_bullet())
        #if any button lifted happens to be in the held_keys array, it will remove the button
        elif event.type == pygame.KEYUP:
            if event.key in held_keys:
                held_keys.remove(event.key)
    
    #draws objects and sprites on the screen
    screen.fill((background))
    gun_group.draw(screen)
    balloon_group.draw(screen)
    bullet_group.draw(screen)

    #creates variables used in the scoreboard
    miss = Font.render(f"Missed shots = {shots - popped}", False, (0, 0, 0))
    success = Font.render(f"Balloons popped = {popped}", False, (0, 0, 0))
    #displays the success rate of the client as a percentage
    if (popped + shots) > 0:
        success_rate = Font.render(f"Success rate = {round (popped / (shots + popped) * 100, 1)}%", False, (0, 0, 0))
    else:
        success_rate = Font.render(f"Success rate = N/A", False, (0, 0, 0)) 
    #draws the scoreboard in the top left of the screen
    screen.blit(miss, (0,0))
    screen.blit(success, (0,20))
    screen.blit(success_rate, (0, 40))
    
    #continually updates the position of the sprites
    gun.update()
    balloon.update()
    bullet_group.update()

    pygame.display.flip()
    #limits the framerate of the game so the game runs on the same time on every computer. 
    clock.tick(60)
#========================================================================================== 