import sys
import pygame
import math

pygame.init()
pygame.mixer.init()

SCREEN_RES = (600,720)
BG_COLOR = (4, 128, 66)
FPS = 60
MAX_POWER = 300


DISPLAY = pygame.display.set_mode(SCREEN_RES)
pygame.display.set_caption("Bhamshu Golf")
icon = pygame.image.load("Assets/icon.ico").convert_alpha()
pygame.display.set_icon(icon)
Clock = pygame.time.Clock()
running = True


HIT_SOUND = pygame.mixer.Sound("Assets/Hit.mp3")
HIT_SOUND.set_volume(0.25)
SWING_SOUND = pygame.mixer.Sound("Assets/swing.mp3")
HOLE_SOUND = pygame.mixer.Sound("Assets/golfed.mp3")
WIN_SOUND = pygame.mixer.Sound("Assets/Win.mp3")
pygame.mixer.music.load("Assets/bg.mp3")
pygame.mixer.music.set_volume(0.35)
pygame.mixer.music.play(-1)

TIT_font = pygame.font.Font("Assets/typing.otf",26)
Play_FONT = pygame.font.Font("Assets/typing2.otf",20)
NOR_font = pygame.font.Font(None,32)

level = 0

class Player(pygame.sprite.Sprite):
    def __init__(self,init_pos : pygame.Vector2):
        super().__init__()
        self.image = pygame.image.load("Assets/ball.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.pos = init_pos
        self.rect.center = self.pos
        self.drag_start = pygame.Vector2()
        self.drag_end = pygame.Vector2()
        self.drag = pygame.Vector2()
        self.vel = pygame.Vector2()
        self.dragging = False
        self.last_hit_time = 0
        self.hit_cooldown = 100
        self.in_hole = False

    def update(self,events,flag):
        global Strokes
        self.pos += self.vel
        self.rect.center = self.pos
        self.collision_wall()
        

        if self.vel.length() < 0.25:
            self.vel = pygame.Vector2()

        self.vel *= 0.97
        if self.vel.length()> MAX_POWER:
            self.vel.scale_to_length(MAX_POWER)
        
        for event in events:
            if self.vel.length() < 8:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        self.drag_start = pygame.Vector2(event.pos)
                        self.dragging = True
                if event.type == pygame.MOUSEBUTTONUP:
                    if event.button == 1:
                        self.dragging = False
                        self.drag_end = pygame.Vector2(event.pos)
                        SWING_SOUND.play()
                        self.drag = self.drag_end - self.drag_start
                        self.vel = -self.drag * 0.1
                        Strokes += 1

        if pygame.Vector2(self.rect.center).distance_to(flag.rect.center) < 8 and self.vel.length() < 8:
            self.in_hole = True
            self.after_hole(flag)
        
    def hit(self):
        current_time = pygame.time.get_ticks()

        if self.vel.length() > 1:
            if current_time - self.last_hit_time > self.hit_cooldown:
                HIT_SOUND.play()
                self.last_hit_time = current_time


    def collision_wall(self):
        if self.rect.left <= 0:
            self.rect.left = 0
            self.pos.x = self.rect.centerx
            self.hit()
            self.vel.x *= -1

        if self.rect.right >= SCREEN_RES[0]:
            self.rect.right = SCREEN_RES[0]
            self.pos.x = self.rect.centerx
            self.hit()
            self.vel.x *= -1
        if self.rect.top <= 0:
            self.rect.top = 0
            self.pos.y = self.rect.centery
            self.hit()
            self.vel.y *= -1
        if self.rect.bottom >= SCREEN_RES[1]:
            self.rect.bottom = SCREEN_RES[1]
            self.pos.y = self.rect.centery
            self.hit()
            self.vel.y *= -1

    def draw_arrow(self, surface):
        if self.dragging:
            mouse = pygame.Vector2(pygame.mouse.get_pos())

            drag = mouse - self.drag_start

            if drag.length() > MAX_POWER:
                drag.scale_to_length(MAX_POWER)
            
            start = self.pos
            end = start - drag
            pygame.draw.line(surface, (200,100,100), start, end, 5)



    def collsion_block(self, block):
        if self.rect.colliderect(block.rect):

            dx = self.rect.centerx - block.rect.centerx
            dy = self.rect.centery - block.rect.centery

            overlap_x = (self.rect.width + block.rect.width) / 2 - abs(dx)
            overlap_y = (self.rect.height + block.rect.height) / 2 - abs(dy)

            self.hit()

            if overlap_x < overlap_y:

                if dx > 0:
                    self.pos.x += overlap_x
                else:
                    self.pos.x -= overlap_x

                self.vel.x *= -1

            else:

                if dy > 0:
                    self.pos.y += overlap_y
                else:
                    self.pos.y -= overlap_y

                self.vel.y *= -1

            
    def after_hole(self,hf):
        self.rect.center = hf.rect.center
        HOLE_SOUND.play()
        self.vel = pygame.Vector2()
    



class Block(pygame.sprite.Sprite):
    def __init__(self,pos : pygame.Vector2):
        super().__init__()
        self.image = pygame.image.load("Assets/Block.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.position = pos
        self.rect.center = self.position


class Hole_class(pygame.sprite.Sprite):
    def __init__(self,pos : pygame.Vector2):
        super().__init__()
        self.image = pygame.image.load("Assets/hole.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.center = pos


player = Player((-100,-100))
hole = Hole_class((-100,-100))

Ball = pygame.sprite.Group()
Ball.add(player)

all_sprites = pygame.sprite.Group()

Hole_sprite = pygame.sprite.Group()

Strokes = 0

def load_level():
    all_sprites.empty()
    Hole_sprite.empty()

    match level:
        case 0:
            player.in_hole = False
            Ball.empty()

            
        case 1:
            Ball.add(player)
            pygame.time.wait(200)
            player.in_hole = False
            Hole_sprite.add(hole)
            
            hole.rect.center = (300,150)
            player.pos = pygame.Vector2(300,500)
            
            all_sprites.add(
                Block((300,300)),
                Block((250,300)),
                Block((350,300))
                
                )
        
        case 2:
            Ball.add(player)
            player.in_hole = False
            Hole_sprite.add(hole)
            
            hole.rect.center = (550,650)
            player.pos = pygame.Vector2(50,50)
            
            all_sprites.add(
                Block((50,350)),
                Block((100,350)),
                Block((300,400)),
                Block((300,450)),
                Block((300,200)),
                Block((300,150))
                )

        

        case 3:
            Ball.add(player)
            player.in_hole = False
            Hole_sprite.add(hole)
            
            hole.rect.center = (100,600)
            player.pos = pygame.Vector2(500,200)
            
            all_sprites.add(
                Block((200,400)),
                Block((200,500)),
                Block((450,150)),
                Block((500,150))
                )
        
        case 4:
            Ball.add(player)
            player.in_hole = False
            Hole_sprite.add(hole)
            
            hole.rect.center = (350,100)
            player.pos = pygame.Vector2(300,450)
            
            all_sprites.add(
                Block((350,150)),
                Block((300,150)),
                Block((250,150)),
                Block((200,150)),
                Block((400,300)),
                Block((450,300))
                )

        case 5:
            Ball.add(player)
            player.in_hole = False
            Hole_sprite.add(hole)
            
            hole.rect.center = (300,600)
            player.pos = pygame.Vector2(300,100)
            
            all_sprites.add(
                Block((250,600)),
                Block((350,600)),
                Block((300,150)),
                Block((250,150)),
                Block((350,150)),
                Block((300,300))
                )
        
        case 6:
            Ball.add(player)
            player.in_hole = False
            Hole_sprite.add(hole)
            
            hole.rect.center = (300,100)
            player.pos = pygame.Vector2(100,600)
            
            all_sprites.add(
                Block((500,300)),
                Block((500,250)),
                Block((500,200)),
                Block((300,150)),
                Block((25,500)),
                Block((75,500)),
                Block((125,500)),
                Block((250,150)),
                Block((200,150))
                )


        case 7:
            Ball.add(player)
            player.in_hole = False
            Hole_sprite.add(hole)
            
            hole.rect.center = (300,100)
            player.pos = pygame.Vector2(300,600)
            
            all_sprites.add(
                Block((25,300)),
                Block((575,300)),
                Block((75,300)),
                Block((525,300)),
                Block((300,150)),
                Block((350,150)),
                Block((250,150)),
                Block((250,100)),
                Block((350,100)),
                Block((300,300))
                )

        case 8:
            Ball.add(player)
            player.in_hole = False
            Hole_sprite.add(hole)
            
            hole.rect.center = (550,50)
            player.pos = pygame.Vector2(50,550)
            
            all_sprites.add(
                Block((75,200)),
                Block((125,200)),
                Block((175,200)),
                Block((225,200)),
                Block((275,200)),
                Block((325,200)),
                Block((375,200)),
                Block((425,200)),
                Block((475,200)),
                Block((525,200)),
                Block((575,200)),
                Block((25,350)),
                Block((75,350)),
                Block((125,350)),
                Block((175,350)),
                Block((225,350)),
                Block((275,350)),
                Block((325,350)),
                Block((375,350)),
                Block((425,350)),
                Block((475,350)),
                Block((300,25)),
                Block((300,150))
                )
        case 9:
            player.in_hole = False
            WIN_SOUND.play()
            Ball.empty()


load_level()

while running:
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            running = False


    DISPLAY.fill(BG_COLOR)

    #/Game Code

    Hole_sprite.draw(DISPLAY)
    player.draw_arrow(DISPLAY)
    Ball.draw(DISPLAY)
    all_sprites.draw(DISPLAY)
    
    for block in all_sprites:
        player.collsion_block(block)
    


    if player.in_hole:
        level += 1
        load_level()

    if level != 0 and level!= 9:
        player.update(events,hole)

    if level == 0:
        text = Play_FONT.render("Press Enter to PLAY", True, (255,255,255))
        DISPLAY.blit(text, (225,300))
        
        keys = pygame.key.get_pressed()

        if keys[pygame.K_RETURN]:
                SWING_SOUND.play()
                level+=1
                load_level()

        title_ = TIT_font.render("Bhamshu Golf", True, (255,255,255))
        y = 200 + math.sin(pygame.time.get_ticks() * 0.003) * 30
        DISPLAY.blit(title_, (175, y))

    
    elif level == 9:
        end_ = TIT_font.render("Thanks For playing", True, (255,255,255))
        Score_ = NOR_font.render("Strokes: " + str(Strokes),True,(255,255,255))

        y_e = 250 + math.sin(pygame.time.get_ticks() * 0.003) * 30

        DISPLAY.blit(end_, (125,y_e))
        DISPLAY.blit(Score_,(245,375))


        keys = pygame.key.get_pressed()

        if keys[pygame.K_ESCAPE]:
            running = False

    else:
       Card = NOR_font.render("Strokes: " + str(Strokes),True,(255,255,255))
       lvl_card = NOR_font.render("Level " + str(level),True,(255,255,255))
       DISPLAY.blit(Card,(245,20))
       DISPLAY.blit(lvl_card,(265,45))


    #Game Code/

    pygame.display.flip() 
    Clock.tick(FPS)

pygame.quit()
sys.exit()