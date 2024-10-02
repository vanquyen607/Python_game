import pygame


class Vehicle(pygame.sprite.Sprite):
    def __init__(self,image,x,y):
        pygame.sprite.Sprite.__init__(self)
        #Scale images
        image_scale= 45 / image.get_rect().width
        new_width = image.get_rect().width * image_scale
        new_height = image.get_rect().height *image_scale
        self.image = pygame.transform.scale(image,(new_width,new_height))
        self.rect = self.image.get_rect()
        self.rect.center = [x,y]