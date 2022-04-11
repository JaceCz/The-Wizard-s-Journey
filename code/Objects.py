
from random import randint, choice
import pygame, sys, time
from pygame import *
from Specifications import *

# creating the background objects in the game 

class Background(pygame.sprite.Sprite):
    def __init__(self, groups, scale_object):
        super().__init__(groups)
        background_image = pygame.image.load('Visuals/Display/snowymountains.png').convert()
        
        # defining the background image
        full_height = background_image.get_height() * scale_object
        full_width = background_image.get_width() * scale_object
        full_scaled_image = pygame.transform.scale(background_image, (full_width, full_height))
        
        self.image = pygame.Surface((full_width * 2, full_height))
        self.image.blit(full_scaled_image, (0, 0))
        self.image.blit(full_scaled_image, (full_width, 0))
        
        # defining the background position
        self.rect = self.image.get_rect(topleft = (0, 0))
        self.pos = pygame.math.Vector2(self.rect.topleft)

    def update(self, dt):
        self.pos.x -= 300 * dt
        if self.rect.centerx <= 0:
            self.pos.x = 0
        self.rect.x = round(self.pos.x)

# Defining the wizard class and its objects
class Wizard(pygame.sprite.Sprite):
    def __init__(self, groups, scale_object):
        super().__init__(groups)

        # defining wizard image
        self.import_frames(scale_object)
        self.frame_index = 0
        self.image = self.frames[self.frame_index]

       # manipulating wizard image using the rectangle surface
        self.rect = self.image.get_rect(midleft = (Width / 20, Height/ 2))
        self.pos = pygame.math.Vector2(self.rect.topleft)

        # wizard movement
        self.gravity = 450
        self.direction = 0

        # applying mask to handle wizard collisions
        self.mask = pygame.mask.from_surface(self.image)

        # defining wizard sounds
        self.wizard_sound = pygame.mixer.Sound('Sounds/Fairy-glitter.wav')
        self.wizard_sound.set_volume(0.09)


    def import_frames(self, scale_object):
        self.frames = []
        for i in range(3):
            wizard_surface = pygame.image.load(f'Visuals/wizard/witch{i}.png').convert_alpha()
            wizard_scale = pygame.transform.scale(wizard_surface, pygame.math.Vector2(wizard_surface.get_size()) * scale_object)
            self.frames.append(wizard_scale)

    def animation(self, dt):
        self.frame_index += 10 * dt
        if self.frame_index >= len(self.frames):
            self.frame_index = 0
        self.image = self.frames[int(self.frame_index)]

    def position_gravity(self, dt):
        self.direction += self.gravity * dt
        self.pos.y += self.direction * dt
        self.rect.y = round(self.pos.y)

    def push(self):
        self.direction = -350
        self.wizard_sound.play()

    def rotate(self):
        rotated_wizard = pygame.transform.rotozoom(self.image, -self.direction * 0.05, 1)
        self.image = rotated_wizard
        self.mask = pygame.mask.from_surface(self.image)

    def update(self, dt):
        self.position_gravity(dt)
        self.animation(dt)
        self.rotate()

class Ground(pygame.sprite.Sprite):
    def __init__(self, groups, scale_object):
        super().__init__(groups)
        self.object_type = 'ground'
        
        # defining ground image
        ground_surface = pygame.image.load('Visuals/Display/lava.v4.png').convert_alpha()
        self.image = pygame.transform.scale(ground_surface, pygame.math.Vector2(ground_surface.get_size()) * scale_object)
        
        # defining the the ground position
        self.rect = self.image.get_rect(bottomleft = (0, Height))
        self.pos = pygame.math.Vector2(self.rect.topleft)
        
        # applying mask to handle ground collisions
        self.mask = pygame.mask.from_surface(self.image)    

    def update(self, dt):
        self.pos.x -= 360 * dt
        if self.rect.centerx <= 0:
            self.pos.x = 0
        self.rect.x = round(self.pos.x)


class Obstacle(pygame.sprite.Sprite):
    def __init__(self, groups, scale_object):
        super().__init__(groups)
        self.object_type = 'obstacle'

        x = Width + randint(40, 100)
        
        # defining obstacle image
        orientation = choice(('up', 'down'))
        obstacle_surface = pygame.image.load(f'Visuals/obstacles/{choice((0, 1))}.png').convert_alpha()
        self.image = pygame.transform.scale(obstacle_surface, pygame.math.Vector2(obstacle_surface.get_size()) * scale_object)
        
        if orientation == 'up':
            y = Height + randint(10, 25)
            self.rect = self.image.get_rect(midbottom = (x, y))
        else:
            y = randint(-50, -10)
            self.image = pygame.transform.flip(self.image, False, True)
            self.rect = self.image.get_rect(midtop = (x, y))
        
        # defining the position of obstacles
        self.pos = pygame.math.Vector2(self.rect.topleft)

        # applying mask to handle obstacle collisions
        self.mask = pygame.mask.from_surface(self.image)

    def update(self, dt):
        self.pos.x -= 400 * dt
        self.rect.x = round(self.pos.x)
        if self.rect.right <= -100:
            self.kill()






       




        