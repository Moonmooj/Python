from turtle import update
import pygame #임포트실행

pygame.init() #초기화 하는 작업(필수요소)

#화면 크기 설정
screen_width = 480 #가로크기
screen_height = 640 #세로크기
screen = pygame.display.set_mode((screen_width, screen_height))


#화면 타이틀 설정
pygame.display.set_caption('Nado Game') #게임 이름

# 배경이미지 불러오기
background = pygame.image.load('C:/Users/82107/OneDrive/바탕 화면/내배캐과제/게임만들기/pygame_basic/background.png')

# 캐릭터(스프라이트) 불러오기
character = pygame.image.load('C:/Users/82107/OneDrive/바탕 화면/내배캐과제/게임만들기/pygame_basic/character.png')
character_size = character.get_rect().size # 이미지의 크기를 구해옴
character_width = character_size[0] # 캐릭터의 가로크기
character_height = character_size[1] # 캐릭터의 세로크기
character_x_pos = (screen_width / 2) - (character_width / 2) # 화면 가로의 절반 크기에 위치하도록 (가로)
character_y_pos = screen_height - character_height # 화면 세로크기 가장 아래에 위치하도록 (세로) - 캐릭터 세로크기 빼주기

# 이벤트 루프 ( 창이 꺼지지 않게하기위해 )
running = True # 게임이 진행중인지 확인
while running:
    for event in pygame.event.get(): # 어떤 이벤트가 발생했는지 확인
        if event.type == pygame.QUIT: # 창이 닫히는 이벤트가 발생했는지 확인
            running = False # 게임이 진행중이 아님 

    screen.blit(background, (0,0)) #배경 그리기 

    screen.blit(character, (character_x_pos, character_y_pos)) # 캐릭터 그리기

    pygame.display.update() # 게임화면을 다시 그리기 !!

# pygame 종료
pygame.quit()