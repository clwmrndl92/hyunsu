import pygame #파이 게임 모듈 임포트

import os
path = os.path.dirname(os.path.abspath(__file__)) + "\\"

pygame.init() #파이 게임 초기화

pygame.mixer.pre_init(44100,-16,2,512)
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 800
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT)) #화면 크기 설정
clock = pygame.time.Clock() 

#변수

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)


umm= pygame.image.load(path + 'umm.png') # Sprites
bba= pygame.image.load(path + 'bba.png')
current_image = umm
umm_sound = pygame.mixer.Sound(path + 'umm.wav')
bba_sound = pygame.mixer.Sound(path + 'bba.wav')

while True: #게임 루프
    screen.fill(WHITE) #단색으로 채워 화면 지우기

    #변수 업데이트

    event = pygame.event.poll() #이벤트 처리
    if event.type == pygame.QUIT:
        break
    elif event.type == pygame.MOUSEBUTTONDOWN:
        current_image = bba
        pygame.mixer.Sound.play(bba_sound)
    elif event.type == pygame.MOUSEBUTTONUP:
        current_image = umm
        pygame.mixer.Sound.play(umm_sound)

    #화면 그리기
    screen.blit(current_image,(-100,0))
    pygame.display.update() #모든 화면 그리기 업데이트
    clock.tick(30) #30 FPS (초당 프레임 수) 를 위한 딜레이 추가, 딜레이 시간이 아닌 목표로 하는 FPS 값

pygame.quit() 
