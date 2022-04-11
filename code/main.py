import pygame, sys, time
from Specifications import *
from Objects import Background, Ground, Wizard, Obstacle


class Game:
    def __init__(self):
        
        # initializing the game
        pygame.init()
        self.display_surface = pygame.display.set_mode((Width, Height))
        pygame.display.set_caption("The Wizard's Journey")
        self.clock = pygame.time.Clock()
        self.active = True
        
        # creating object groups
        self.all_objects = pygame.sprite.Group()
        self.collision_objects = pygame.sprite.Group()
         
        # scaling the objects
        background_height = pygame.image.load('Visuals/Display/snowymountains.png').get_height()
        self.scale_object = Height / background_height
   
        # incorporating the object groups into the game
        Background(self.all_objects, self.scale_object)
        Ground([self.all_objects, self.collision_objects], self.scale_object)
        self.wizard = Wizard(self.all_objects, self.scale_object * 2.2)

        # defining the timing of obstacles
        self.obstacle_timer = pygame.USEREVENT + 1
        pygame.time.set_timer(self.obstacle_timer, 1400)
    
        # applying text and font style to score display
        self.font = pygame.font.Font('Visuals/Font Style/MoriaCitadel.TTF', 50)
        self.score = 0
        self.score_offset = 0

        # defining the game menu
        self.menu_surface = pygame.image.load('Visuals/UI Design/menu.png').convert_alpha()
        self.menu_rectangle = self.menu_surface.get_rect(center = (Width / 2, Height / 2))

        # adding game music
        self.music = pygame.mixer.Sound('Sounds/Wizard-Theme.wav')
        self.music.play(loops= - 1)
  
    def collisions(self):
        if pygame.sprite.spritecollide(self.wizard, self.collision_objects, False, pygame.sprite.collide_mask)\
            or self.wizard.rect.top <= 0:
            for sprite in self.collision_objects.sprites():
                if sprite.object_type == 'obstacle':
                    sprite.kill()
            self.active = False
            self.wizard.kill()

    def player_score(self):
        if self.active:
            self.score = (pygame.time.get_ticks() - self.score_offset) // 1000
            y = Height / 10
        else:
            y = Height / 2 + self.menu_rectangle.height / 1.5

        score_surface = self.font.render(str(self.score), True, 'black')
        score_rectangle = score_surface.get_rect(midtop = (Width / 2, y))
        self.display_surface.blit(score_surface, score_rectangle)


    def run(self):
        last_time = time.time()
        while True:

            # Using delta time to keep track of frames
            dt = time.time() - last_time
            last_time = time.time()

            # Using event loop to define gameplay
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.active:
                        self.wizard.push()
                    else:
                        self.wizard = Wizard(self.all_objects, self.scale_object * 2.2)
                        self.active = True
                        self.score_offset = pygame.time.get_ticks()

                if event.type == self.obstacle_timer:
                    Obstacle([self.all_objects, self.collision_objects], self.scale_object * 1.9)

            # game fundamentals
            self.display_surface.fill('black')
            self.all_objects.update(dt)
            self.collisions()
            self.all_objects.draw(self.display_surface)
            self.player_score()

            if self.active:
                self.collisions()
            else:
                self.display_surface.blit(self.menu_surface, self.menu_rectangle)
            
            pygame.display.update()
            self.clock.tick(FRAMERATE)


if __name__ == '__main__':
    game = Game()
    game.run()
