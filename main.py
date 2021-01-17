# set up and display
import pygame
import sys
timer = pygame.time.Clock()

from pygame.locals import *
pygame.init()

pygame.display.set_caption('Pelatformer')  # game title

# game window size
window_size = (600,400)
screen = pygame.display.set_mode(window_size,0,32)


display = pygame.Surface((300, 200))    # surfaces are used to represent objects, used for the display rendering

# image loads
player_sprite = pygame.image.load('rb1.png')    # loads red ball into pygame
grass = pygame.image.load('rumput.png')     # loads grass blocks into game
dirt = pygame.image.load('tanah.png')       # loads dirt blocks into game
tile_size = grass.get_width()               # function for tile size based on the with of the view window

scrolls = [0,0]     # parallax scrolling variable

ball_jump = pygame.mixer.Sound('ball_jump.wav')
pygame.mixer.music.load("bgm.wav")
pygame.mixer.music.play(10000)
pygame.mixer.music.set_volume(0.3)         # sets BGM volume to 0.3 as originally it was really loud


# inserting the game map
# 2 represents grass blocks, 1 represents dirt blocks, 0 represents null
# there are other ways to make the map, such as by using a function that imports a .txt file
map = [['0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0'],
       ['0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0'],
       ['0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0'],
       ['0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0'],
       ['0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','2','2','2','2','0','0','0','0','0','0','0','0','0','0','0'],
       ['0','0','0','0','0','0','0','2','2','2','2','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','2','2','2','2'],
       ['0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0'],
       ['0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0'],
       ['0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0'],
       ['2','2','2','2','2','2','2','2','2','2','2','2','2','2','2','2','2','2','2','2','2','2','2','2','2','2','2','2','2','2','2'],
       ['1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1'],
       ['1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1'],
       ['1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1'],
       ['1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1'],
       ['1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1'],
       ['1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1']]

# player collision with tiles
def coll_test(rect, tiles):
    coll_list = []
    for tile in tiles:
       if rect.colliderect(tile):
           coll_list.append(tile)
    return coll_list

def move(rect, movement, tiles):
    coll_types = {'left': False, 'right': False, 'top': False, 'bottom': False}  # block collision sides
    rect.x += movement[0]
    coll_list = coll_test(rect, tiles)
    for tile in coll_list:
        if movement[0] > 0:  # [0] represents x-axis movement (left & right)
            rect.right = tile.left
            coll_types['right'] = True
        elif movement[0] < 0:
            rect.left = tile.right
            coll_types['left'] = True

    rect.y += movement[1]
    coll_list = coll_test(rect, tiles)
    for tile in coll_list:
        if movement[1] > 0:     # [1] represents y-axis movement (top & bottom)
            rect.bottom = tile.top
            coll_types['bottom'] = True
        elif movement[1] < 0:
            rect.top = tile.bottom
            coll_types['top'] = True
    return rect, coll_types

# x movement variables
movement_right = False
movement_left = False

# y movement variables
player_ymomentum = 0
airtime = 0


player_rect = pygame.Rect(50, 50, player_sprite.get_width(), player_sprite.get_height()) # player collision mask
coll_rect = pygame.Rect(100,100,100,50)
parallax_obj = [[0.15,[100,10,50,500]]]


# game loop
while True:
    # scrolling background
    display.fill((146, 234, 254))

    scrolls[0] += (player_rect.x-scrolls[0]-160)/20     # screen is 300px wide, half of that is +- 150, allows us to lock screen to player
    scrolls[1] += (player_rect.y-scrolls[1]-120)/20      # same concept
    scroll = scrolls.copy()
    scroll[0] = int(scroll[0])
    scroll[1] = int(scroll[1])
    pygame.draw.rect(display, (00, 69, 94), pygame.Rect(0, 170, 1000, 50))   # sea background drawn using rect

    y = 0
    tile_rects = []

    for row in map:
        x = 0
        for tile in row:
            if tile == '1':
                display.blit(dirt, (x * tile_size - scroll[0], y * tile_size - scroll[1]))
            if tile == '2':
                display.blit(grass, (x * tile_size - scroll[0], y * tile_size - scroll[1]))
            if tile != '0':
                tile_rects.append(pygame.Rect(x * tile_size, y * tile_size, tile_size, tile_size))
            x += 1
        y += 1

    # player movement
    p_movement = [0, 0]
    if movement_right:
        p_movement[0] += 2
    if movement_left:
        p_movement[0] -= 2
    p_movement[1] += player_ymomentum
    player_ymomentum += 0.18
    if player_ymomentum > 3:
        player_ymomentum = 3


    player_rect, collisions = move(player_rect, p_movement, tile_rects)

    # vertical momentum
    if collisions['bottom']:    # if ball collides with block after falling, ball vertical momentum = 0, airtime = 0
        airtime = 0
    else:
        airtime += 1

    # parallax
    display.blit(player_sprite,(player_rect.x-scroll[0],player_rect.y-scroll[1])) # block transfer, copies elements of one surface to another

    # event loop
    for event in pygame.event.get():
        if event.type == QUIT:     # check for window quit
            pygame.quit()          # stop game
            sys.exit()
        if event.type == KEYDOWN:  # triggered anytime key in keyboard is pressed down
            if event.key == K_z:
                pygame.mixer.music.fadeout(1000)    # if z key is pressed, music fades out at in 1000ms/1sec
            if event.key == K_x:
                pygame.mixer.music.play(10000)      # if x is pressed, music plays again
            if event.key == K_RIGHT:                # if right arrow key is pressed, ball moves right
                movement_right = True
            if event.key == K_LEFT:                 # if left arrow key is pressed, ball moves right
                movement_left = True
            if event.key == K_UP:                   # if up arrow key is pressed, ball jumps
                if airtime < 6:
                    ball_jump.play()
                    player_ymomentum = -5
        if event.type == KEYUP:          # triggered anytime key is released
            if event.key == K_RIGHT:              # if right arrow key is released, ball stops moving right
                movement_right = False
            if event.key == K_LEFT:               # if left arrow key is released, ball stops moving left
                movement_left = False


    surf = pygame.transform.scale(display, window_size)
    screen.blit(surf, (0, 0))
    pygame.display.update( )    # display update
    timer.tick(60)      # frame rate 60fps







