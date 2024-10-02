import pygame

class Coin(pygame.sprite.Sprite):
    def __init__(self, image, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(image,(30,30))  # Thay đổi 'images/coin.png' thành đường dẫn thích hợp
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
