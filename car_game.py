#Thư viện
import pygame
from pygame.locals import *
import random
import os
from pygame.sprite import Group


from Vehicle import Vehicle
from PlayerVehicle import PlayerVehicle
from Coin import Coin


pygame.init()

 
def initScreen(width, height):
    screen_size=(width, height)
    screen=pygame.display.set_mode(screen_size)
    pygame.display.set_caption("Game Đua Xe")
    return screen

def isVehicleCrash(player, verhicle_group):
    for verhicle in verhicle_group:
            if pygame.sprite.collide_rect(player,verhicle):
                return True;
    return False;

def drawRoad():
    #Vẽ địa hình cỏ
    screen.fill(green)
    #Vẽ road  -- đường chạy
    pygame.draw.rect(screen,gray,road)
    #Vẽ edge  -- biên đường
    pygame.draw.rect(screen,yellow,left_edge)
    pygame.draw.rect(screen,yellow,right_edge)

# chọn một tên bài nhạc ngẫu nhiên từ danh sách
def randomMusic(music_list):
    random_music = random.choice(music_list)
    bg_music = pygame.mixer.music.load(os.path.join("background_music", random_music))
    pygame.mixer.music.set_volume(0.8)
    pygame.mixer.music.play(loops=-1)

# Hàm di chuyển đối tượng
def moveObject(obj_group):
    for obj in obj_group:
        obj.rect.y += speed
        #remove object( chạy hết màn hình thì mất )
        if obj.rect.top >= height:
            obj.kill()

# Kích thước cửa sổ game
width=800
height=700

screen = initScreen(width, height)

gray=(100,100,100)
green=(76,208,56)
yellow=(255,232,0)
red=(200,0,0)
white=(255,255,255)

#Khởi tạo biến
gameover = False
speed = 2
score = 0
highscore = 0

#đường xe chạy
road_width=600
street_width=10 #width vach ke phan lane
street_height=50 #height vach ke phan lane

#land đường 
# Cập nhật số lượng lane và vị trí của chúng
lane_left = 150
lane_1 = 250
lane_2 = 350
lane_3 = 450
lane_4 = 550
lane_right = 650
lanes = [lane_left, lane_1, lane_2, lane_3,lane_4, lane_right]

lane_move_y=0

#road và edge
road=(100,0,road_width,height)
left_edge=(95,0,street_width,height)
right_edge=(695,0,street_width,height)

#Vị trí ban đầu của xe người chơi
player_x=250
player_y=400

#Sprite group
player_group = pygame.sprite.Group()
verhicle_group = pygame.sprite.Group()
coin_group = pygame.sprite.Group()  # Tạo một nhóm để chứa các đồng coin

#Tạo xe người chơi
player = PlayerVehicle(player_x,player_y)
player_group.add(player)

#Load xe lưu thông
image_name = ['pickup_truck.png','semi_trailer.png','taxi.png','van.png']
verhicle_image =[]
for name in image_name:
    image=pygame.image.load('images/'+ name)
    verhicle_image.append(image)
    
#load hình va chạm
crash=pygame.image.load('images/crash.png')
crash_rect = crash.get_rect()

#Âm thanh va chạm
crash_music = pygame.mixer.Sound("sound/boom.wav")

#Âm thanh gameover
gameover_music = pygame.mixer.Sound("sound/game_over.wav")

# danh sách các tên bài nhạc
music_list = ["music1.wav", "music2.wav", "music3.wav", "music4.wav", "music5.wav", "music6.wav", "music7.wav", "music8.wav"]
randomMusic(music_list)

#FPS của game
clock=pygame.time.Clock()
fps=120

#Vòng lặp xử lý game

while True:
    #Chỉnh frame hình trên giây
    clock.tick(fps)
    for event in pygame.event.get():
        if event.type == QUIT:
            exit(0)
        #Điều khiển xe 
        if event.type == KEYDOWN:
            if event.key == K_LEFT and player.rect.center[0] > min(lanes):
                player.rect.x -= 100
            if event.key == K_RIGHT and player.rect.center[0] < max(lanes):
                player.rect.x += 100
            if event.key == K_DOWN and player.rect.bottom < height-100:
                player.rect.y += 100
            if event.key == K_UP and player.rect.top > 100:
                player.rect.y -= 100       
        #Kiểm tra va chạm khi điều khiển
        gameover = isVehicleCrash(player, verhicle_group)

    #Kiểm tra va chạm khi đứng yên
    if pygame.sprite.spritecollide(player,verhicle_group,True):
        gameover = True   
        crash_rect.center = [player.rect.center[0], player.rect.top]
                
    drawRoad()
    
    # Vẽ land đường
    lane_move_y += speed * 2
    if lane_move_y >= street_height * 2:
        lane_move_y = 0
    for y in range(street_height * -2, height, street_height * 2):
        for lane in lanes[:-1]:
            pygame.draw.rect(screen, white, (lane + 45, y + lane_move_y, street_width, street_height))

    #Vẽ xe player 
    player_group.draw(screen)
    #Vẽ phương tiện giao thông
    if len(verhicle_group) < 2:
        add_verhicle = True
        for verhicle in verhicle_group:
            if verhicle.rect.top < verhicle.rect.height * 1.5 :
                add_verhicle = False
        if add_verhicle:
            lane = random.choice(lanes) 
            image = random.choice(verhicle_image)
            verhicle =Vehicle(image,lane,height / -2)
            verhicle_group.add(verhicle)
    #Cho xe công cộng chạy
    moveObject(verhicle_group)
        
    #Vẽ nhóm xe lưu thông
    verhicle_group.draw(screen)
    
    if gameover == False:
        add_coin = True
        for coin in coin_group:
            if coin.rect.top < coin.rect.height * 1.5:
                add_coin = False
        if add_coin:
            for i in range(0, 3):
                lane = random.choice(lanes)
                image = pygame.image.load('images/coin.png')
                coin = Coin(image, lane, height / -2)
                coin_group.add(coin)

    #Cho đồng coin chạy
    moveObject(coin_group)

    #Vẽ nhóm coin
    coin_group.draw(screen)  

    # Kiểm tra va chạm với player và tăng score khi nhặt được đồng coin
    
    for coin in coin_group:
        if pygame.sprite.collide_rect(player, coin):
            coin.kill()  
            score += 10  
            if (score % 50 == 0):
                speed += 1
                
    #Hiển thị điểm
    font = pygame.font.Font(pygame.font.get_default_font(),16)
    text_score = font.render(f'Score: {score}',True,white)
    text_score_rect = text_score.get_rect() #chuyển text_score thành đối tượng 
    text_score_rect.center=(50,40)
    screen.blit(text_score,text_score_rect)
    
    #Hiển thị highscore
    text_highscore = font.render(f'HScore: {highscore}',True,white)
    text_highscore_rect = text_highscore.get_rect() #chuyển text_highscore thành đối tượng 
    text_highscore_rect.center=(50,80)
    screen.blit(text_highscore,text_highscore_rect)

    
    if gameover:
        # Kiểm tra xem score hiện tại có lớn hơn highscore không
        if score > highscore:
            highscore = score
        screen.blit(crash,crash_rect) #Vẽ hiệu ứng nổ
        crash_music.play()
        #Thông báo gameover
        gameover_music.play()
        pygame.draw.rect(screen,red,(0,50,width,100)) 
        font = pygame.font.Font(pygame.font.get_default_font(),16)
        text = font.render(f'Gameover ! Play again ? (Y / N)',True,white)
        text_rect = text.get_rect() 
        text_rect.center=(width/2,100)
        screen.blit(text,text_rect)
        pygame.mixer_music.stop()
    pygame.display.update()
    while gameover:
        clock.tick(fps)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit(0)
                
            if event.type == KEYDOWN:
                if event.key == K_y:
                    #Reset game
                    pygame.mixer.music.play(loops=-1)
                    gameover = False
                    score = 0
                    speed = 2
                    verhicle_group.empty()
                    coin_group.empty()
                    player.rect.center = [player_x, player_y]
                elif event.key == K_n:
                    #exit game
                    exit(0)
                    
pygame.quit()
            


