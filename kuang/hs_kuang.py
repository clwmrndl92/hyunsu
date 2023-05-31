import pygame as pg
import sys
import random
import os
path = os.path.dirname(os.path.abspath(__file__)) + "\\"

# 초기화
pg.init()
pg.font.init()
game_font = pg.font.SysFont('MalgunGothic', 50)
button_font = pg.font.SysFont('HY목각파임B', 30)
clock = pg.time.Clock() 

# 화면 설정
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 750
screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

COLOR_mario_green = (8,162,75)
COLOR_mario_yellow = (251,181,31)
COLOR_white = (255,255,255)
# 소리 설정
pg.mixer.pre_init(44100,-16,2,512)
background_sound = pg.mixer.music.load(path + 'Mario_Athletic_BGM.mp3')
# pg.mixer.music.set_volume(0.5)

kuang_sound = pg.mixer.Sound(path + 'kung.mp3')
kuang_ground_sound = pg.mixer.Sound(path + 'ground2.mp3')
kuang_ground_sound.set_volume(0.2)
kuang_dead_sound = pg.mixer.Sound(path + 'stomp.wav')

jump_sound = pg.mixer.Sound(path + 'jump2.wav')
jump_sound.set_volume(0.2)

over_sound = pg.mixer.Sound(path + 'Mario_dies.wav')
down_sound = pg.mixer.Sound(path + 'Power_down.wav')
reward_sound = pg.mixer.Sound(path + 'reward.wav')

# bba_sound = pg.mixer.Sound('bba.wav')

# 타이머
pg.time.set_timer(pg.USEREVENT, 800)
pg.time.set_timer(pg.USEREVENT+1, 3000)
pg.time.set_timer(pg.USEREVENT+2, 400)
pg.time.set_timer(pg.USEREVENT+3, 5000)
pg.time.set_timer(pg.USEREVENT+4, 400)

# 배경 이미지 로드
background = pg.transform.scale(pg.image.load(path + 'background.png'),(SCREEN_WIDTH,SCREEN_HEIGHT))
ground_height = 70
ground = pg.transform.scale(pg.image.load(path + 'ground.jpg'),(SCREEN_WIDTH,ground_height))
ground_pos = (0,SCREEN_HEIGHT - ground_height)
kuang_size = (150, 170)
hk1= pg.transform.scale(pg.image.load(path + 'hk1.png'), kuang_size)
collider = pg.image.load(path + 'collider.png')
hk2= pg.transform.scale(pg.image.load(path + 'hk2.png'), kuang_size)
reward_size = (900, 750)
reward_img = pg.transform.scale(pg.image.load(path + 'reward.jpg'), reward_size)
reward_heart_img = pg.transform.scale(pg.image.load(path + 'reward_heart.png'), reward_size)
# reward_heart_ratio = (0.426, 0.563)
reward_heart_ratio = (0.426, 0.663)
reward_pos = (SCREEN_WIDTH/2 - reward_size[0]/2, 0)

# 점수
kuang_score = 0
life = 1
game_over = False

def __main__():
    global kuang_score, game_over, life
    pos = (SCREEN_WIDTH/2 - kuang_size[0]/2,SCREEN_HEIGHT/2 - kuang_size[1]/2)
    start_img2 = pg.transform.scale(pg.image.load(path + 'arrow.png'), (100,150))
    while True:
        kuang_score = 0
        life = 1
        game_over = False
        pg.mixer.music.play(loops=-1)
        start_img = hk1
        start = False
        arrow = True
        # 시작씬
        while True: 
            # 이벤트
            event = pg.event.poll()
            
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
                mpos = pg.mouse.get_pos()
                if mpos[0] > pos[0] and mpos[0] < pos[0] + kuang_size[0] and mpos[1] > pos[1] and mpos[1] < pos[1] + kuang_size[1]: 
                    start = True
            if event.type == pg.USEREVENT + 2:  
                arrow = not arrow

            screen.blit(background,(0,0))
            screen.blit(start_img,pos)
            if arrow:
                screen.blit(start_img2,(450,150))
            pg.display.update()

            clock.tick(30) 
            if start:
                kuang_sound.play()
                start_img = hk2
                screen.blit(background,(0,0))
                screen.blit(start_img,pos)
                pg.display.update()
                break

        pg.time.wait(1000) 
        # 스프라이트 그룹
        player = Player()
        player_Group = pg.sprite.Group()
        player_Group.add(player)
        
        kuang_sound.set_volume(0.5)
        kuang_Group = pg.sprite.Group()
        kuang_Group.add(Kuang(player))

        # 게임 루프
        while True: 
            # 이벤트
            event = pg.event.poll()
            
            
            if not game_over:
                if event.type == pg.QUIT:
                    pg.quit()
                    sys.exit()
                if event.type == pg.USEREVENT:
                    kuang_Group.add(Kuang(player))

                kuang_Group.update()
                player_Group.update()
            else:
                break
            # 화면 그리기
            screen.blit(background,(0,0))

            kuang_Group.draw(screen)
            player_Group.draw(screen)
            screen.blit(ground, ground_pos)
            
            g = 255 - kuang_score*2
            if g < 0: g = 0
            b = 255 - kuang_score
            if b < 0: b = 0

            score_text_surface = game_font.render(str(kuang_score), True, (255, g, b))
            score_text_rect = score_text_surface.get_rect()
            score_text_rect.center = (30, 30)
            screen.blit(score_text_surface, score_text_rect)
            
            pg.display.update()

            clock.tick(30) 

        last_sceen_sprites = []
        re_btn = Button(text="다시하기", pos=(SCREEN_WIDTH/2- 100, SCREEN_HEIGHT/2-30), size=(200,60), color=COLOR_mario_green, font_color=COLOR_mario_yellow)
        reward_btn = Button(text="!!특전 보기!!", pos=(SCREEN_WIDTH/2-100, SCREEN_HEIGHT/2-30 + 100), size=(200,60), color=COLOR_mario_green, font_color=COLOR_mario_yellow)
        last_sceen_sprites.append(re_btn)
        timer = 0
        reward = False
        heart_Group = pg.sprite.Group()
        # heart_Group.add(Heart(reward_pos))
        pg.mixer.music.stop()
        over_sound.play()
        # 게임 오버 씬
        while True: 
            event = pg.event.poll()
            
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            
            if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
                mpos = pg.mouse.get_pos()
                if re_btn.isOnMouse(mpos):
                    pg.mixer.music.stop()
                    
                    kuang_Group.empty()
                    player_Group.empty()
                    for sprite in last_sceen_sprites:
                        sprite.kill()
                    break
                if not reward and reward_btn.isOnMouse(mpos):
                    reward_sound.play()
                    reward = True
            if event.type == pg.USEREVENT+4 and reward:
                heart_Group.add(Heart(reward_pos))
            
            if reward:
                timer += 1
                if timer == 50:
                    timer = 0
                    reward = False
                    heart_Group.empty()

            screen.blit(background,(0,0))

            kuang_Group.draw(screen)
            player_Group.draw(screen)
            screen.blit(ground, ground_pos)
            re_btn.draw()
            if kuang_score >= 100:
                reward_btn.draw()

            if reward:
                heart_Group.update()
                screen.blit(reward_img, reward_pos)
                heart_Group.draw(screen)
            
            pg.display.update()

            clock.tick(30) 


class Heart(pg.sprite.Sprite):
    def __init__(self,pos):
        pg.sprite.Sprite.__init__(self)
        self.init_image = reward_heart_img
        self.image = self.init_image
        self.rect = self.image.get_rect()
        self.size = reward_size
        self.sizeup = 0
        self.maxup = 10
        self.sizedelta = 300
        self.pos = pos
        self.init_pos = pos
        self.prev_heart_pos = (int(self.size[0] * reward_heart_ratio[0]), int(self.size[1]  * reward_heart_ratio[1]))

    def update(self):
        self.image = pg.transform.scale(self.init_image, self.size)
        self.sizeup += 1
        self.size = (reward_size[0] + self.sizeup*self.sizedelta, reward_size[1] + self.sizeup*self.sizedelta)
        heart_pos = (int(self.size[0] * reward_heart_ratio[0]), int(self.size[1]  * reward_heart_ratio[1]))
        delta_pos = (heart_pos[0] - self.prev_heart_pos[0], heart_pos[1] - self.prev_heart_pos[1])
        # self.prev_heart_pos = heart_pos
        self.pos = (self.init_pos[0]- delta_pos[0],self.init_pos[1] - delta_pos[1])
        self.rect.x = self.pos[0] + 120
        self.rect.y = self.pos[1] + 230
        if self.sizeup > self.maxup:
            self.kill()

class Button(pg.sprite.Sprite):
    def __init__(self, image = None, size=(100,100), pos=(SCREEN_WIDTH/2, SCREEN_HEIGHT/2), text = "button", color = (0, 0, 0), font_color = COLOR_white):
        pg.sprite.Sprite.__init__(self)

        self.size = size
        self.pos = pos
        self.text = text
        self.color = color
        self.font_color = font_color

        
        self.rect = pg.Rect(self.pos, self.size)
        self.image = pg.Surface(self.size)
        self.image.fill(self.color)
        
        self.text_surface = button_font.render(str(self.text), True, self.color)
        self.text_rect = self.text_surface.get_rect()
        self.text_rect.center = (self.pos[0] + self.size[0]/2, self.pos[1] + self.size[1]/2)

        self.clicked = False    

    def isOnMouse(self, mouse_pos):
        if mouse_pos[0] > self.pos[0] and mouse_pos[0] < self.pos[0] + self.size[0] and mouse_pos[1] > self.pos[1] and mouse_pos[1] < self.pos[1] + self.size[1]: 
            return True

    def draw(self):
        screen.blit(self.image, self.pos)
        self.text_surface = button_font.render(str(self.text), True, self.font_color)
        self.text_rect = self.text_surface.get_rect()
        self.text_rect.center = (self.pos[0] + self.size[0]/2, self.pos[1] + self.size[1]/2)
        screen.blit(self.text_surface , self.text_rect)

#플레이어 클래스
class Player(pg.sprite.Sprite):
    def __init__(self):
        pg.sprite.Sprite.__init__(self)

        self.size = (100,100)
        self.size2 = (150,150)
        self.picture = pg.image.load(path + 'player2.png')
        self.init_image = pg.transform.scale(self.picture, self.size)
        self.invin_image = pg.transform.scale(pg.image.load(path + 'player_invin.png'), self.size2)
        self.cur_image = self.init_image
        self.image = pg.transform.rotate(self.init_image, 0)
        self.mask = pg.mask.from_surface(self.image)
        self.speed = 15
        self.x_speed = 0
        self.y_speed = 0
        self.jump_power = -40
        self.gravity = 4
    
        self.rect = self.image.get_rect()
        self.init_pos = (SCREEN_WIDTH / 2, ground_pos[1] - self.size[1])
        self.rect.topleft = self.init_pos
        self.pos = list(self.init_pos)
        self.pos[0] = self.rect.x
        self.pos[1] = self.rect.y
        self.rotate = 0
        self.jumping = False
        self.free_fall = False
        self.dead = False
        self.invin = False
        self.timer = 0
        self.timer2 = 0

    def update(self):
        global life, game_over
        if not self.dead:
            key = pg.key.get_pressed()

            if key[pg.K_SPACE]:
                if not self.jumping:
                    self.y_speed = self.jump_power
                    self.jumping = True

                    jump_sound.play()
            if key[pg.K_LEFT]:
                self.x_speed = -self.speed
            if key[pg.K_RIGHT]:
                self.x_speed = self.speed
            
            self.pos[0] += self.x_speed
            self.pos[1] += self.y_speed

            if self.invin:
                if self.timer == 60:
                    self.cur_image = self.init_image
                    self.invin = False
                    self.timer = 0
                    self.timer2 = 0
                if self.timer2 == 15:
                    if self.cur_image == self.invin_image:
                        self.cur_image = self.init_image
                    else:
                        self.cur_image = self.invin_image
                    self.timer2 = 0
                self.timer += 1
                self.timer2 += 1
                self.image = self.cur_image

            if self.jumping:
                if self.x_speed < 0:
                    self.rotate = (self.rotate+20)%360
                else:
                    self.rotate = (self.rotate-20)%360
                self.image = pg.transform.rotate(self.cur_image, self.rotate)
            if self.jumping or self.free_fall:
                self.y_speed += self.gravity

            if self.pos[1] > self.init_pos[1]:
                self.jumping = False
                self.free_fall = False
                self.y_speed = 0
                self.pos[1] = self.init_pos[1]
                self.image = pg.transform.rotate(self.cur_image, 0)
            if self.pos[0] < 0:
                self.pos[0] = 0
            elif self.pos[0] > SCREEN_WIDTH- self.size[0]:
                self.pos[0] = SCREEN_WIDTH - self.size[0]
        else:
            if self.pos[1] > ground_pos[1] + 10:
                if life == 0:
                    self.kill()
                    game_over = True
                else:
                    life -= 1
                    self.invin = True
                    self.pos = list(self.init_pos)
                    self.dead = False
                    self.cur_image = self.invin_image
                    self.init_image = pg.transform.scale(self.picture, self.size2)
                    self.size = self.size2
                    self.init_pos = (SCREEN_WIDTH / 2, ground_pos[1] - self.size[1])
                    self.mask = pg.mask.from_surface(self.init_image)
                    down_sound.play()
            # self.rect.x = self.pos[0]
        self.rect.x = self.pos[0] + self.cur_image.get_width() / 2 - self.image.get_width() / 2
        self.rect.y = self.pos[1] + self.cur_image.get_height() / 2 - self.image.get_height() / 2

        self.x_speed = 0
    
    def stop(self, stop_pos_x = None, stop_pos_y = None):
        self.jumping = False
        self.image = pg.transform.rotate(self.init_image, 0)
        if stop_pos_x:
            self.x_speed = 0
            self.pos[0] = stop_pos_x
        if stop_pos_y:
            self.y_speed = 0
            self.pos[1] = stop_pos_y


        
# 쿵쿵 클래스
class Kuang(pg.sprite.Sprite):
    def __init__(self, player):
        pg.sprite.Sprite.__init__(self)
        self.player = player

        self.size = kuang_size
        self.hk1= hk1
        self.hk2= hk2
        
        self.image = self.hk1
        self.mask = pg.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.init_pos = (random.randrange(0, SCREEN_WIDTH -self.size[0]),random.randrange(0, 100))
        self.rect.topleft = self.init_pos
        self.pos = list(self.init_pos)
        self.speed = 2
        self.accel = 2
        self.is_accel = False
        self.dist = 70
        self.ground_pos = ground_pos[1] - self.size[1]
        self.dead = False
        self.player_daed = False

        self.collider_top = RectCollider(self, (20, 0), (self.size[0]-40, 10))
        self.collider_bottom = RectCollider(self, (30, self.size[1] - 10), (self.size[0]-60, 10))
        self.collider_left = RectCollider(self, (0, 10), (10, self.size[1] - 20))
        self.collider_right = RectCollider(self, (self.size[1] - 10, 10), (10, self.size[1] - 20))

    def update(self):
        global kuang_score
        if self.pos[1] < self.ground_pos:
            # 가속
            if self.pos[1] > self.init_pos[1] + self.dist:
                self.is_accel = True
                self.speed += self.accel
                self.image = self.hk2
            self.pos[1] += self.speed
            if self.pos[1] >= self.ground_pos:
                self.pos[1] = self.ground_pos
            if self.pos[1] > self.ground_pos-50:
                kuang_ground_sound.play()
        else:
            self.pos[1] += 1

        # self.collider_bottom.update()
        if self.player.dead and self.player_daed:
            self.player.pos[1] = self.pos[1] + self.size[1]
        elif not self.player.invin:
            if self.collider_top.isCollision(self.player) and self.player.pos[1] + self.player.size[1] < self.pos[1] + 50:
                self.player.stop(stop_pos_y = self.pos[1] - self.player.size[1])
                self.player.y_speed = self.player.jump_power /2
                self.dead = True
                kuang_sound.play()
                kuang_dead_sound.play()
                kuang_score += 1
            else:
                self.player.free_fall = True
            if self.collider_left.isCollision(self.player):
                self.player.stop(stop_pos_x = self.pos[0] - self.player.size[0])
            elif self.collider_right.isCollision(self.player):
                self.player.stop(stop_pos_x = self.pos[0] + self.size[0])
            elif self.collider_bottom.isCollision(self.player):
                self.player.stop(stop_pos_y = self.pos[1] + self.size[1])
                if self.is_accel:
                    self.player.dead = True
                    self.player_daed = True

        
        if self.dead:
            self.pos[1] += self.speed * 2
            if self.pos[1] > SCREEN_HEIGHT + 10:
                self.kill()

        self.rect.y = self.pos[1]
        self.collider_top.update()
        self.collider_left.update()
        self.collider_right.update()
        self.collider_bottom.update()

class  RectCollider(pg.sprite.Sprite):
    def __init__(self,  parent, offset, size):
        pg.sprite.Sprite.__init__(self)
        self.parent = parent
        self.offset = offset
        self.size = size

        self.image = pg.transform.scale(collider, self.size)
        self.mask = pg.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect.topleft = (self.parent.pos[0] + self.offset[0] ,self.parent.pos[1] + self.offset[1]) 
    
    def update(self):
        self.rect.topleft = (self.parent.pos[0] + self.offset[0] ,self.parent.pos[1] + self.offset[1]) 
    


    def isCollision(self, object):
        return pg.sprite.collide_mask(self, object)
    


__main__()
